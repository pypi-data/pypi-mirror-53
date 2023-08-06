from typing import Dict, Optional, Any, Callable


class ClassRegistry(Dict[str, Callable]):
    """
    Subclass of ``dict`` to map names to classes, with customizable checks
    and a custom metaclass for easy auto-registration of classes.
    """

    def check_key(self, key: str) -> None:
        """
        Perform checks on a given key. Does nothing by default;
        is available for easy customization of the registry.

        Does not return any meaningful value; not raising an exception should
        be considered a successful check.

        :param str key: Key of a class being registered.
        """

    def check_value(self, value: Callable) -> None:
        """
        Perform checks on a given class. Does nothing by default;
        is available for easy customization of the registry.

        Does not return any meaningful value; not raising an exception should
        be considered a successful check.

        :param Callable value: A class being registered.
        """

    def check(self, key: str, value: Callable) -> None:
        """
        Called before any registration; performs optional checks and raises
        exceptions. The default implementation calls :meth:`check_key`,
        raising :exc:`KeyError` for any exceptions raised by this method,
        then calls :meth:`check_value`, raising :exc:`ValueError` for any
        exceptions raised by this method.

        Does not return any meaningful value; not raising an exception should
        be considered a successful check.

        :param str key: Key of a class being registered.
        :param Callable value: Class being registered.
        :raises KeyError: When :meth:`check_key` raises any exception.
        :raises ValueError: When :meth:`check_value` raises any exception.
        """
        try:
            self.check_key(key)
        except KeyError:
            raise
        except Exception as e:
            raise KeyError(str(e))

        try:
            self.check_value(value)
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(str(e))

    def register(self, key: str, value: Callable) -> None:
        """
        Register a new class. Alias to ``registry[key] = value``.

        :param str key: Key to register the class under.
        :param Callable value: Class to register.
        """
        self[key] = value

    def unregister(self, key: str) -> None:
        """
        Unregister a class. Alias to ``del registry[key]``.

        :param str key: Key of a registered class.
        """
        del self[key]

    def __setitem__(self, key: str, value: Callable) -> None:
        self.check(key, value)
        super().__setitem__(key, value)

    def _repr_pretty_(self, p: Any, cycle: bool) -> None:
        # IPython's pretty printing
        if cycle:
            p.text('{}(...)'.format(self.__class__.__name__))
        else:
            p.text('{}('.format(self.__class__.__name__))
            p.pretty(dict(self))
            p.text(')')

    @property
    def metaclass(self) -> type:
        """
        A custom metaclass which performs auto-registration of any subclass.
        """
        class RegistryMetaclass(type):

            def __new__(cls,
                        name: str,
                        *args: Any,
                        register: bool = True,
                        key: Optional[str] = None,
                        **kwargs: Any) -> type:
                newclass = super().__new__(cls, name, *args, **kwargs)
                if register:
                    self.register(key or name, newclass)
                return newclass

        return RegistryMetaclass
