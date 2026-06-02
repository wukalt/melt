import sys
from types import FunctionType
from typing import Any


def find_function(handlers, function_name: str) -> FunctionType | None:
    for handler_name in handlers.keys():
        if handler_name == function_name:
            return handlers[handler_name].get("handler")

    raise KeyError(function_name)


def generate_auto_switch(switches_names, function_name: str, index: int = 1) -> str:
    if function_name[0:index] in switches_names:
        index += 1
        return generate_auto_switch(switches_names, function_name, index)

    switches_names.append(function_name[0:index])
    return f"-{function_name[0:index]}"


class Melt:
    def __init__(self) -> None:
        self.filename: str = sys.argv.pop(0)
        self.switches_names: list[str] = []
        self.handlers: dict[str, dict[str, Any]] = {}

    def __call__(self) -> Any:
        from_index = 0

        if "--help" in sys.argv:
            show_help(self)
            exit(code=0)

        for arg in sys.argv:
            if arg in self.handlers:
                handler = find_function(self.handlers, arg)

                if handler is None:
                    raise Exception("invalid function (function is None)")

                function_args_count = len(handler.__annotations__)
                into = from_index + function_args_count

                # Escape the command or switch index
                from_index += 1
                into += 1

                handler(*sys.argv[from_index:into])
                from_index += function_args_count

    def command(self, flag: bool = True):
        def execute(func: FunctionType):
            self.handlers[func.__name__] = {"handler": func, "is_switch": False}

            def wrapper(*args, **kwds):
                result = func(*args, **kwds)
                return result

            return wrapper

        return execute

    def switch(self, flag: bool = True):
        def execute(func: FunctionType):
            name = generate_auto_switch(self.switches_names, func.__name__)
            self.handlers[name] = {"handler": func, "is_switch": True}

            def wrapper(*args, **kwds):
                result = func(*args, **kwds)
                return result

            return wrapper

        return execute


def show_help(melt_obj: Melt):
    print(f"Help table of -> {melt_obj.filename}:")
    print("".join("=" for _ in range(100)))

    for func_name in melt_obj.handlers.keys():
        handler = find_function(melt_obj.handlers, func_name)

        fmt = "\t{} -> {}".format(
            func_name.ljust(40),
            "there is no help for this command"
            if handler.__doc__ is None
            else handler.__doc__,
        )

        print(fmt)
