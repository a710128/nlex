class Package:
    def __init_subclass__(cls, name=None, require=None):
        if name is None:
            name = cls.__name__
        if require is None:
            require = []
        type.__setattr__(cls, "NAME", name)
        type.__setattr__(cls, "REQ", require)

    def init(self, instance : 'Nlex'):
        pass