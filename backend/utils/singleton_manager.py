class SingletonManager:
    _instances = {}

    @classmethod
    def get_instance(cls, class_type, *args, **kwargs):
        class_name = class_type.__name__
        if class_name not in cls._instances:
            cls._instances[class_name] = class_type(*args, **kwargs)
        return cls._instances[class_name]

    @classmethod
    async def close_all(cls):
        for instance in cls._instances.values():
            if hasattr(instance, 'close'):
                await instance.close()
        cls._instances.clear()
