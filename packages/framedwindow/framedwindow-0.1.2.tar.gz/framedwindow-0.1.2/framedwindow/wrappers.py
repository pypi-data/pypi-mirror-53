class FrameRegistry:
    objects = {
        "master": None

    }

    def __new__(cls, *args, **kwargs):
        """ Create as a singleton. """
        if not hasattr(cls, "instance"):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __setitem__(self, key, value):
        self.objects[key] = value

    def __getitem__(self, item):
        if item in self.objects:
            return self.objects[item]
        else:
            return False

    def register_ob(self, name, obj):
        self.objects[name] = obj

    def pull(self, obj):
        return self.objects[obj]


_registry_ob = FrameRegistry()


def register(f):
    def wr_regis(*args, **kwargs):
        _registry_ob.register_ob(f.__name__, f)
        x = f(*args, **kwargs)
        return x
    return wr_regis


def pull(o):
    r = _registry_ob.pull(o)
    return r


### wrapper - put around a simple function using print or input and execute it inside of a curses wrapped window.
### Works only for little things iwth print, input at the moment, will expand later

def framed(f):
    import framedwindow

    @register
    def compile_obj_wrap(*args, **kwargs):
        w = framedwindow.FramedWindow()
        print = w.cprint
        input = w.colored_prompt
        x = f(*args, **kwargs)
        w.decompile()
        return x
    return compile_obj_wrap


def safe_exec(f):
    import framedwindow
    @register
    def safe_exec_wrap(*args, **kwargs):
        x = f(*args, **kwargs)
        try:
            framedwindow.curses.endwin()
        finally:
            return x

    return safe_exec_wrap

