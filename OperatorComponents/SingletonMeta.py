class SingletonMeta(type):
    """
    A metaclass for creating Singleton classes. Ensures only one instance of a Singleton class is created.

    :param _instances: a dictionary which is a vital part in ensuring that only one instance of the classes which
    use SingletonMeta as metaclass will be created
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Controls the instantiation of Singleton classes. Returns the same instance for a class every time it's called.
        if an instance of the class does not exist, it creates one in instances

        :param cls: The instance being instanced.
        :param args: Positional arguments for the class constructor.
        :param kwargs: Positional Keyword arguments for the class constructor.
        :returns: An instance of the Singleton class.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]