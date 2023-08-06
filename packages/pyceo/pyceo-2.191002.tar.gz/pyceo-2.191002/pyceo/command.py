import textwrap


__all__ = ("Command", "HELP_COMMANDS", "get_doc")

HELP_COMMANDS = ("help", "h")


def get_doc(func):
    """Extract and dedent the __doc__ of a function.

    Unlike `textwrap.dedent()` it also works when the first line
    is not indented.
    """
    doc = func.__doc__
    if not doc:
        return ""

    # doc has only one line
    if "\n" not in doc:
        return doc

    # Only Python core devs write __doc__ like this
    if doc.startswith(("\n", "\\\n")):
        return textwrap.dedent(doc)

    # First line is not indented
    first, rest = doc.split("\n", 1)
    return first + "\n" + textwrap.dedent(rest)


class Command(object):
    """
    """

    manager = None

    def __init__(self, func, group=None, help="", name=None):
        self.func = func

        if not name:
            name = func.__name__
            if group:
                name = f"{group}:{name}"
        self.name = name

        self.description = (get_doc(func) or help).strip()
        self.help = help or self.description.split("\n", 1)[0]

        # @param or @option decorators could have already been executed
        # to the bare function
        self.params = getattr(func, "params", [])
        self.options = getattr(func, "options", {})

    def __call__(self, *args, **opts):
        try:
            return self.func(*args, **opts)
        except KeyboardInterrupt:
            print()

    def _filter_options(self, opts):
        parsed_opts = {}

        for key, value in opts.items():
            _option = self.options.get(key)
            if not _option:
                continue
            if _option.type is not None:
                try:
                    value = _option.type(value)
                except (TypeError, ValueError):
                    self.manager.show_error(f"Wrong argument for `{key}`")
                    raise
            parsed_opts[key] = value

        return parsed_opts

    def run(self, *args, **opts):
        for key in opts:
            if key.lstrip("-") in HELP_COMMANDS:
                self.show_help()
                return

        len_args = len(args)
        len_params = len(self.params)
        if len_args != len_params:
            if len_args > len_params:
                self.manager.show_error("Too many arguments")
            else:
                self.manager.show_error("Missing arguments")
            self.show_help()
            return

        try:
            opts = self._filter_options(opts)
        except (TypeError, ValueError):
            return

        return self(*args, **opts)

    def show_help(self):
        self.manager.show_help_command(self)
