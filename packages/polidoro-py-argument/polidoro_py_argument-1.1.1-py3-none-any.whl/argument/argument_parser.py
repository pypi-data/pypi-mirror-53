import argparse
import inspect

from argument.argument import Argument
from argument.command import Command


def get_class_that_defined_object(object):
    if inspect.ismethod(object):
        for cls in inspect.getmro(object.__self__.__class__):
            if cls.__dict__.get(object.__name__) is object:
                return cls
        object = object.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(object):
        cls = getattr(inspect.getmodule(object),
                      object.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(object, '__objclass__', None)


class ArgumentParser(argparse.ArgumentParser):
    """
    An argparse.ArgumentParser wrapper to create the arguments and run the methods
    """

    parsers = {}

    def __new__(cls, *args, id=None, **kwargs):
        # to create only one ArgumentParses with the same ID
        if id not in ArgumentParser.parsers:
            return object.__new__(cls)
        return ArgumentParser.parsers[id]

    def __init__(self, *args, version=None, id=None, **kwargs):
        # Only initialize if is a new parser
        if id not in ArgumentParser.parsers:
            kwargs.setdefault('argument_default', argparse.SUPPRESS)
            self.subparsers = None

            super(ArgumentParser, self).__init__(*args, **kwargs)
            if version:
                self.add_argument('-v', '--version', action='version', version='%(prog)s ' + version)

            self.parsers[id] = self

    def parse_args(self, *args, **kwargs):
        # Add arguments for each @Argument
        for arg in Argument.arguments:
            parser = self.get_final_parser(arg.kwargs['method'], argument=True)
            parser.add_argument(*arg.args, **arg.kwargs)

        # Add subparser for each @Command
        for cmd in Command.commands:
            parser = self.get_final_parser(cmd)

            parser.set_defaults(method=cmd)
            positional_arguments = []
            keyword_arguments = []
            for p in inspect.signature(cmd).parameters.values():
                if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                    if p.default == inspect._empty:
                        positional_arguments.append(p)
                    else:
                        keyword_arguments.append(p)
            if positional_arguments:
                # Add positional arguments if there is any positional argument and nargs = number of arguments in method
                parser.add_argument('arguments', nargs=len(positional_arguments))

            if keyword_arguments:
                # Add optional arguments for each keyword argument
                for ka in keyword_arguments:
                    parser.add_argument('--%s' % ka.name)

        namespace = super(ArgumentParser, self).parse_args(*args, **kwargs)
        namespace_dict = vars(namespace)
        method = namespace_dict.pop('method', None)
        if method is not None:
            namespace_args = namespace_dict.pop('arguments', [])
            method(*namespace_args, **namespace_dict)
            exit(0)

        return namespace

    def add_subparsers(self, **kwargs):
        """ Add subparsers if not exists """
        if self.subparsers is None:
            metavar = kwargs.get('metavar', 'command')
            required = kwargs.get('required', True)
            self.subparsers = super(ArgumentParser, self).add_subparsers(
                metavar=metavar,
                required=required,
                **kwargs
            )

        return self.subparsers

    def get_final_parser(self, target, argument=False):
        """ Return the final parser creating subparsers if needed """
        final_parser = self
        clazz = get_class_that_defined_object(target)
        full_name = [target]
        while clazz:
            full_name.append(clazz)
            clazz = get_class_that_defined_object(clazz)

        # If is an argument, remove the first name and create subprsers for the others names
        if argument:
            full_name.pop(0)

        # Create or recover the final parser
        for trgt in reversed(full_name):
            parser_name = trgt.__name__.lower()
            if parser_name in ArgumentParser.parsers:
                final_parser = ArgumentParser.parsers[parser_name]
            else:
                subparsers = final_parser.add_subparsers()
                final_parser = subparsers.add_parser(parser_name, id=parser_name, help=getattr(trgt, 'help', ''))
        return final_parser


