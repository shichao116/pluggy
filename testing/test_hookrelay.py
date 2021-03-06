import pytest
from pluggy import PluginValidationError, HookimplMarker, HookspecMarker


hookspec = HookspecMarker("example")
hookimpl = HookimplMarker("example")


def test_happypath(pm):
    class Api(object):
        @hookspec
        def hello(self, arg):
            "api hook 1"

    pm.add_hookspecs(Api)
    hook = pm.hook
    assert hasattr(hook, 'hello')
    assert repr(hook.hello).find("hello") != -1

    class Plugin(object):
        @hookimpl
        def hello(self, arg):
            return arg + 1

    plugin = Plugin()
    pm.register(plugin)
    l = hook.hello(arg=3)
    assert l == [4]
    assert not hasattr(hook, 'world')
    pm.unregister(plugin)
    assert hook.hello(arg=3) == []


def test_argmismatch(pm):
    class Api(object):
        @hookspec
        def hello(self, arg):
            "api hook 1"

    pm.add_hookspecs(Api)

    class Plugin(object):
        @hookimpl
        def hello(self, argwrong):
            pass

    with pytest.raises(PluginValidationError) as exc:
        pm.register(Plugin())

    assert "argwrong" in str(exc.value)


def test_only_kwargs(pm):
    class Api(object):
        @hookspec
        def hello(self, arg):
            "api hook 1"

    pm.add_hookspecs(Api)
    pytest.raises(TypeError, lambda: pm.hook.hello(3))


def test_firstresult_definition(pm):
    class Api(object):
        @hookspec(firstresult=True)
        def hello(self, arg):
            "api hook 1"

    pm.add_hookspecs(Api)

    class Plugin(object):
        @hookimpl
        def hello(self, arg):
            return arg + 1

    pm.register(Plugin())
    res = pm.hook.hello(arg=3)
    assert res == 4
