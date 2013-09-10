

def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider


def can_be_overridden():
    def overrider(method):
        return method
    return overrider
