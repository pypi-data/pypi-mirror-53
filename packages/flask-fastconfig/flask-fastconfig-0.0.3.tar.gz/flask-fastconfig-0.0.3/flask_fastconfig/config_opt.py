class BaseOptError(Exception):
    pass


class DefaultValueError(BaseOptError):
    pass


class ChoicesValueError(BaseOptError):
    pass


class ValueTypeError(BaseOptError):
    pass


class BaseOpt(object):

    def __init__(self, default, type, help=None, required=False,
                 secret=False, choices=None, app_config=None):
        self.default = default
        self.help = help
        self.required = required
        self.secret = secret
        self.choices = choices
        self.type = type
        self.app_config = app_config
        self._check()

    def _check(self):
        if self.choices is not None:
            if not isinstance(self.choices, list):
                raise ChoicesValueError()

            for choice in self.choices:
                if not isinstance(choice, self.type):
                    raise ChoicesValueError()

        if self.default is not None:
            if not isinstance(self.default, self.type):
                raise DefaultValueError()

            if self.choices and self.default not in self.choices:
                raise DefaultValueError()

    def get_deafult(self):
        return self.fromat(self.default)

    def fromat(self, value):
        try:
            return self._fromat(value)
        except:
            raise ValueTypeError()

    def _fromat(self, value):
        return self.type(value)


class StrOpt(BaseOpt):

    def __init__(self, default, help=None, required=False,
                 secret=False, choices=None, app_config=None):
        super(StrOpt, self).__init__(default, str, help, required,
                                     secret, choices, app_config)


class IntOpt(BaseOpt):
    def __init__(self, default, help=None, required=False,
                 secret=False, choices=None, app_config=None):
        super(IntOpt, self).__init__(default, int, help, required,
                                     secret, choices, app_config)


class BooleanOpt(BaseOpt):
    def __init__(self, default, help=None, required=False,
                 secret=False, choices=None, app_config=None):
        super(BooleanOpt, self).__init__(default, bool, help, required,
                                         secret, choices, app_config)

    def _fromat(self, value):
        if value in ['True', 'true']:
            return True
        elif value in ['False', 'false']:
            return False


class ListOpt(BaseOpt):
    def __init__(self, default, help=None, required=False,
                 secret=False, choices=None, app_config=None):
        super(ListOpt, self).__init__(default, list, help, required,
                                      secret, choices, app_config)

    def _fromat(self, value):
        return value.split(',')


class FloatOpt(BaseOpt):
    def __init__(self, default, help=None, required=False,
                 secret=False, choices=None, app_config=None):
        super(FloatOpt, self).__init__(default, float, help, required,
                                       secret, choices, app_config)
