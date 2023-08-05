import inspect

from argument.custom_action import CustomAction


class Argument(object):
    """
    Decorator to create a command line argument
    """
    arguments = []

    def __init__(self, method=None, help=None, **_):
        self.help = help
        self.method = method
        # if method is None the decorator has parameters
        if method is not None:
            self.args = tuple(['--' + method.__name__])

            self.kwargs = {
                'action': CustomAction,
                'method': method,
                'help': help
            }
            parameters = inspect.signature(method).parameters
            # nargs = number of arguments in method
            self.kwargs['nargs'] = len(parameters)
            if parameters:
                self.kwargs['metavar'] = list(parameters.values())[0].name

            self.arguments.append(self)

    def __call__(self, *args, **kwargs):
        # if method is None the decorator has parameters and the first argument is the method
        if self.method is None:
            self.method = list(args)[0]
            self.__init__(**vars(self))
            return self
        return self.method(*args, **kwargs)
