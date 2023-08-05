import os
import warnings
from importlib import import_module
from types import ModuleType
from typing import *

from dataclasses import field
from typing_inspect import get_origin, get_args

from ._decorations import *

T = TypeVar('T')
@deserialize_with(ConstructorDataType.String, post_init='_check_class')
class DynamicClass(Generic[T]):
    """
    A helper class which accepts a string class path and imports it.
    Stores both class path and the loaded class.
    
    This class is the generic over `T` - super-class.
    If used inside `dataclasses_config.Config` class,
    it would also check that the loaded class is the subclass of `T`.
    
    Raises:
        ImportError: Raised in case of missing module or class in that module.
        TypeError: Raised in case of loaded class not matching the super-class.
    
    Warnings:
        ImportWarning: Sent if the inheritance check is called without specifying the base class.
    
    """
    
    class_path: str
    """`str`. Full class path which could be used for import."""
    
    cls: Type[T] = field(init=False)
    """`Type[T]`. An imported and loaded class."""
    
    def __init__(self, class_path: str):
        self.class_path = class_path
        module_name, _sep, class_name = self.class_path.rpartition('.')
        if (not _sep):
            raise ImportError(f"Cannot import class '{self.class_path}'")
        
        mod: ModuleType = import_module(module_name)
        try:
            self.cls = getattr(mod, class_name)
        except AttributeError:
            raise ImportError(f"Cannot import name {class_name!r} from {module_name!r} ({mod.__file__})")
        return
    
    def _check_class(self, tp: Type['DynamicClass[T]'], *args, **kwargs):
        
        base = get_origin(tp)
        type_args = get_args(tp)
        if (base is None):
            warnings.warn(ImportWarning(f"Type {tp} should be parametrized, but it is not."))
            return
        
        expected_parent = type_args[0]
        if (not issubclass(self.cls, expected_parent)):
            raise TypeError(f"{self.cls!r} is not a subclass of {expected_parent!r} (from {tp!r}).")
    
    def __repr__(self):
        return f'{type(self).__name__}({self.cls!r})'
del T

@deserialize_with(ConstructorDataType.String)
class Path(str):
    r"""
    A helper class which converts any string-like path to the absolute path.
    
    It is a subclass of `str`, and thus any string operations and methods are available here.
    Useful while reading configuration.
    Automatically converted to the absolute path when used inside `dataclasses_config.Config`.
    
    Examples:
        ```python
        Path('.')               
        # Something like:
        #   '/home/user/project/test'
        #   'C:\\Users\\user\\Projects\\Test'
        
        Path('my_lib', 'mod.py')
        # Something like:
        #   '/home/user/project/test/my_lib/mod.py'
        #   'C:\\Users\\user\\Projects\\Test\\my_lib\\mod.py'
        
        ```
    """
    
    def __new__(cls, *args, **kwargs):
        return os.path.abspath(os.path.join(*args))

@deserialize_with(ConstructorDataType.String)
class RelPath(str):
    """
    A helper class which represents relative path.
    A method `dataclasses_config.RelPath.apply()` converts this this object to the `dataclasses_config.Path` with the given root.
    
    It is a subclass of `str`, and thus any string operations and methods are available here.
    Useful while reading configuration.
    Automatically converted to the absolute path when used inside `dataclasses_config.Config`.
    """
    
    def apply(self, root: Path, **kwargs) -> Path:
        r"""
        Converts this this object to the `dataclasses_config.Path` with the given root.
        
        Args:
            root: `dataclasses_config.Path`.
            **kwargs: Optional.
                If presented, then the resulting Path is then formatted using the `str.format_map()` method.
        
        Returns:
            `dataclasses_config.Path`
        
        Examples:
            ```python
            RelPath('mod.py').apply('.')                                     
            # Something like:
            #   '/home/user/project/test/mod.py'
            #   'C:\\Users\\user\\Projects\\Test\\mod.py'
            
            RelPath('{module_name}/mod.py').apply('my_lib')                  
            # Something like:
            #   '/home/user/project/test/my_lib/{module_name}/mod.py'
            #   'C:\\Users\\user\\Projects\\Test\\my_lib\\{module_name}\\mod.py'
            
            RelPath('{module_name}/mod.py').apply('my_lib', module_name=bin) 
            # Something like:
            #   '/home/user/project/test/my_lib/bin/mod.py'
            #   'C:\\Users\\user\\Projects\\Test\\my_lib\\bin\\mod.py'
            ```
        """
        
        p = Path(root, self)
        if (kwargs):
            p = Path(p.format_map(kwargs))
        return p
    
    @property
    def as_path(self) -> Path:
        """
        Transforms the `RelPath` object to the absolute `dataclasses_config.Path`.
        Returns:
            `dataclasses_config.Path`
        """
        
        return Path(self)

__all__ = \
[
    'DynamicClass',
    'Path',
    'RelPath',
]
