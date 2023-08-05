import inspect
import logging
import importlib
import pickle
import datetime

from .hints import HintsManager
from .exceptions import EmptyQuerysetError
from .models import DataProduct, RefreshQueue

from django.conf import settings
from django.db.models import Q

logger = logging.getLogger(__name__)

_cache_instance = None

CACHE_ENTRY_FIELDS = ['key', 'value', 'primer_name', 'version', 'modified', 'soft_expire', 'hard_expire']
KEYSEP = '/'


class KeyParameterMismatch(Exception):
    pass


class UnregisteredPrimer(Exception):
    pass


class Primer(object):

    prime_on_cache_miss = False
    key_base = None
    key = None
    soft_expire_seconds = None
    hard_expire_seconds = None
    hooks = None
    parameters = None

    def __init__(self, key):
        self.key = key

    @property
    def soft_expire(self):
        if self.soft_expire_seconds:
            return datetime.datetime.utcnow() + datetime.timedelta(seconds=self.soft_expire_seconds)
        return None

    @property
    def hard_expire(self):
        if self.hard_expire_seconds:
            return datetime.datetime.utcnow() + datetime.timedelta(seconds=self.hard_expire_seconds)
        return None

    @classmethod
    def register_all_primers(cls, cache_instance):
        logger.debug('Primer.register_all_primers() entered')
        for installed_app_module_as_string in settings.INSTALLED_APPS:
            logger.debug(f'Primer.register_all_primers() - examining module: {installed_app_module_as_string}')
            primers_module_as_string = f'{installed_app_module_as_string}.primers'
            try:
                primers_module = importlib.import_module(primers_module_as_string)
            except ModuleNotFoundError:
                continue

            for name, pcls in inspect.getmembers(primers_module):
                if pcls == Primer or not type(pcls) == type or not issubclass(pcls, Primer):
                    continue
                logger.debug(f'Primer.register_all_primers() - registering {pcls.__name__}')
                pcls.register(cache_instance)

    @classmethod
    def register(cls, cache_instance):
        cache_instance.register_primer(cls)

    def compute(self):
        return None

    def prime(self, cache=None, hints=None):
        cache = cache or Cache.get_instance()
        hints = hints or HintsManager(cache)

        if self.has_hook('pre-prime'):
            self.do_hooks('pre-prime', hints=hints)

        new_value = self.compute()
        cache_entry = cache.cache_entry(
            key=self.key,
            value=new_value,
            primer_name=self.key_base,
            soft_expire=self.soft_expire,
            hard_expire=self.hard_expire)

        if self.has_hook('post-prime'):
            hints.set_hint_key(cache_entry)
            self.do_hooks('post-prime', hints=hints)

        cache.set(**cache_entry)

        return cache_entry

    def do_hooks(self, hook_type, *args, **kwargs):
        if not self.hooks or hook_type not in self.hooks:
            return
        if callable(self.hooks[hook_type]):
            self.hooks[hook_type](*args, **kwargs)
            return
        try:
            for hook in self.hooks[hook_type]:
                try:
                    hook(*args, **kwargs)
                except TypeError:
                    logger.warning(f'hook {hook_type} iterable returned uncallable object')
        except TypeError:
            logger.warning(f'hook {hook_type} is defined, but is neither callable nor iterable')

    @classmethod
    def has_hook(cls, hook_type):
        if not cls.hooks or hook_type not in cls.hooks:
            return False
        return True

    def parameter_dict(self):
        if KEYSEP not in self.key:
            return {}
        parts = self.key.split(KEYSEP)[1:]
        if len(parts) != len(self.parameters):
            raise KeyParameterMismatch(self.key)
        parameters = {}
        for n, p in enumerate(self.parameters):
            parameters[p.name] = p.from_str(parts[n])
        return parameters


class Cache(object):

    _primers = {}

    @classmethod
    def key_base(cls, key):
        if KEYSEP in key:
            return key.split(KEYSEP)[0]
        return key

    @classmethod
    def get_instance(cls, new_instance=False):
        global _cache_instance
        if not _cache_instance or new_instance:
            logger.info('initializing new cache')
            _cache_instance = cls()
        return _cache_instance

    def __init__(self):
        Primer.register_all_primers(self)

    def run_processes(self):

        for key_base, primer_cls in self._primers.items():
            if hasattr(primer_cls, 'processes'):
                for process_cls in primer_cls.processes:
                    process_cls(self, key_base).run()

    def build_key(self, key_base, **kwargs):
        primer_cls = self.primer(key_base)
        if not primer_cls.parameters:
            return key_base
        parts = [key_base]
        for p in self.primer(key_base).parameters:
            parts.append(p.to_str(kwargs[p.name]))
        return KEYSEP.join(parts)

    def register_primer(self, primer_cls):
        self._primers[primer_cls.key_base] = primer_cls

    def primer(self, key):
        keybase = self.key_base(key)
        if keybase in self._primers and issubclass(self._primers[keybase], Primer):
            return self._primers[keybase]
        return None

    def get(self, key, prime_on_cache_miss=None):

        current_time = datetime.datetime.utcnow()

        # try to return cached version
        queryset = DataProduct.objects.filter(
            Q(key=key) & (Q(hard_expire=None) | Q(hard_expire__gt=current_time)))

        try:
            cache_entry = self.cache_entry(queryset=queryset, key=key)

            # if soft expire is defined and in the past, request a refresh
            if cache_entry['soft_expire'] and cache_entry['soft_expire'] < datetime.datetime.utcnow():
                self.refresh(key, queued=True)

            return cache_entry

        # try to prime
        except (DataProduct.DoesNotExist, EmptyQuerysetError):

            # if a primer does not exist, raise KeyError
            primer_cls = self.primer(key)
            if not primer_cls:
                raise KeyError(key)

            # if prime_on_cache_miss is True on primer or in param to this method, then prime
            if (primer_cls.prime_on_cache_miss and prime_on_cache_miss is not False) or prime_on_cache_miss:
                return primer_cls(key).prime(cache=self)

            # failing all else, raise KeyError
            raise KeyError(key)

    def set(self, key, value, primer_name=None, modified=None, version=None, soft_expire=None, hard_expire=None, hints=None):
        params = dict(
            key=key,
            value=value,
            primer_name=primer_name,
            soft_expire=soft_expire,
            hard_expire=hard_expire,
            modified=modified if modified else datetime.datetime.utcnow())
        if version:
            params['version'] = version
        logger.info(f'set() - params: {params}')
        primer_obj = None
        hints = hints or HintsManager(self)
        primer_cls = self.primer(key)
        if primer_cls:
            primer_obj = primer_cls(key)
            if primer_cls.has_hook('pre-set') or primer_cls.has_hook('post-set'):
                try:
                    cache_entry = self.get(key)
                    hints.set_hint_key(cache_entry)
                except KeyError:
                    pass
                primer_obj.do_hooks('pre-set', hints=hints, **params)

        data_product = DataProduct(**params)
        data_product.save()
        cache_entry = self.cache_entry(data_product=data_product)

        if primer_cls and primer_cls.has_hook('post-set'):
            primer_obj.do_hooks('post-set', hints=hints, **params)

        return cache_entry

    def cache_entry(self, data_product=None, queryset=None, key=None, value=None, primer_name=None,
                    version=None, soft_expire=None, hard_expire=None, modified=None):
        if queryset is not None:
            ret = queryset.values(*CACHE_ENTRY_FIELDS)
            if ret:
                return ret[0]
            raise EmptyQuerysetError(key)

        if data_product:
            rec = {}
            for fld in CACHE_ENTRY_FIELDS:
                rec[fld] = getattr(data_product, fld)
            return rec

        ret = dict(key=key, value=value, primer_name=primer_name,
                   soft_expire=soft_expire, hard_expire=hard_expire)
        ret['modified'] = modified if modified else datetime.datetime.utcnow()
        if version:
            ret['version'] = version
        return ret

    def is_set(self, key):
        try:
            cache_entry = self.get(key)
            return True
        except KeyError:
            return False

    def refresh(self, key, queued=True, hints=None):
        # refresh non-queued requests immediately
        if not queued:
            primer_class = self.primer(key)
            try:
                primer_obj = primer_class(key)
            except TypeError:
                raise UnregisteredPrimer(key)

            return primer_obj.prime(hints=hints)

        # save a refresh request
        new_refresh_queue_entry = RefreshQueue(
            key=key,
            primer_name=Cache.key_base(key),
            hints=hints.to_dict() if hints else None)
        new_refresh_queue_entry.save()

    def refresh_requests(self, claimant=None, primer_names=None):
        queryset = RefreshQueue.objects
        if primer_names:
            queryset = queryset.filter(primer_name__in=primer_names)
        if claimant:
            queryset = queryset.filter(claimant=claimant)
        return queryset

    def claim_refresh_requests(self, claimant, max_requests=None, primer_names=None):

        # build a queryset of refresh requests
        queryset = RefreshQueue.objects
        if primer_names:
            queryset = queryset.filter(primer_name__in=primer_names)
        ordered_queryset = queryset.order_by('requested')

        # build the key list
        key_list = []
        for rec in ordered_queryset.values('key'):
            if rec['key'] in key_list:
                continue
            key_list.append(rec['key'])
            if max_requests and len(key_list) >= max_requests:
                break

        # claim the refresh requests
        queryset.filter(key__in=key_list).filter(claimant=None).update(claimant=claimant, claimed=datetime.datetime.utcnow())

    def perform_claimed_refreshes(self, claimant):
        queryset = RefreshQueue.objects.filter(claimant=claimant).order_by('key')
        current_key = None
        current_hints = None
        for refresh_queue_entry in queryset:
            if current_key is None:
                current_hints = HintsManager(self)
                current_key = refresh_queue_entry.key
            elif current_key != refresh_queue_entry.key:
                self.refresh(current_key, hints=current_hints, queued=False)
                current_hints = HintsManager(self)
                current_key = refresh_queue_entry.key
            if refresh_queue_entry.hints:
                current_hints.import_from_dict(refresh_queue_entry.hints)
        if current_key:
            self.refresh(current_key, hints=current_hints, queued=False)
