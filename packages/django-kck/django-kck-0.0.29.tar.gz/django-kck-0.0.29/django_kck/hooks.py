class UncallableHook(Exception):
    pass


class BaseHook(object):
    hook_type = None
    callable = None

    def __init__(self, callable=None):
        if callable:
            self.callable = callable

    def run(self, *args, **kwargs):
        if self.callable:
            try:
                self.callable(*args, **kwargs)
            except TypeError:
                raise UncallableHook()

    def run_if_type_matches(self, hook_type, *args, **kwargs):
        if hook_type != self.hook_type:
            return
        self.run(*args, **kwargs)


class PreSetHook(BaseHook):
    hook_type = 'pre-set'


class PostSetHook(BaseHook):
    hook_type = 'post-set'


class PrePrimeHook(BaseHook):
    hook_type = 'pre-prime'


class PostPrimeHook(BaseHook):
    hook_type = 'post-prime'


