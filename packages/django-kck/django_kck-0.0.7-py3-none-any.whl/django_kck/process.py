import datetime
import logging

from django_kck.hints import HintsManager

logger = logging.getLogger(__name__)


class BaseProcess(object):
    cache = None
    key_base = None

    def __init__(self, cache, key_base):
        self.cache = cache
        self.key_base = key_base

    def run(self, hints=None):
        return


class IntervalRefreshProcess(BaseProcess):
    interval = datetime.timedelta(seconds=60)
    domain_key = None

    def run(self, hints=None):
        hints = hints or HintsManager(self.cache)
        domain = self.domain(hints=hints)
        if domain:
            for key in domain:
                cache_entry = hints.get(key, prime_on_cache_miss=True)
                if datetime.datetime.utcnow() - cache_entry['modified'] >= self.interval:
                    self.cache.refresh(key, queued=True, hints=hints)

    def domain(self, hints=None):
        hints = hints or HintsManager(self.cache)
        if self.domain_key:
            try:
                return hints.get(self.domain_key)['value']
            except KeyError:
                logger.warning(
                    'IntervalRefreshProcess({}) - attempt to fetch domain key {} failed'
                        .format(self.key_base, self.domain_key))
        return None
