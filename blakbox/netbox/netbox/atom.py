from .globals import inspect
from .log import NBOXlogger

def NBOXprivate(func):
    def wrapper(*args, **kwargs):
        caller = inspect.stack()[1].frame.f_globals.get("__name__")
        if not caller.startswith("netbox."):
            NBOXlogger.warning(f"Internal Method, cannot call `{func.__name__}`.")
            return
        return func(*args, **kwargs)
    return wrapper

class NBOXatom:
    def __init__(self) -> None:
        self._mask: int = 0
        self._type: int = 0
        self._uid: int = id(self)

    @property
    def mask(self) -> int:
        return self._mask
    
    @property
    def type(self) -> int:
        return self._type
    
    @property
    def uid(self) -> int:
        return self._uid

    def set_flag(self, flag: int) -> None:
        if flag < 0 or not isinstance(flag, int): return
        self._mask |= flag

    def get_flag(self, flag: int) -> bool:
        if flag < 0 or not isinstance(flag, int): return
        return ((self._mask & flag) == flag)

    def rem_flag(self, flag: int) -> None:
        if flag < 0 or not isinstance(flag, int): return
        self._mask &= ~flag

