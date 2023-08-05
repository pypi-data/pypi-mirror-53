import configparser
from flask_fastconfig import config_opt as opt


CONF = None


class ConfigOpts(object):

    def __init__(self, app, file_path, encoding="utf-8"):
        self.app = app
        self._cfg_ = configparser.ConfigParser()
        self._groups_ = {}
        self._app_config_ = {}
        self.read_config(file_path, encoding)
        self.setup()

    def read_config(self, file_path, encoding="utf-8"):
        global CONF
        self._cfg_.read(file_path, encoding)
        ConfigGroup.__cfg__ = self._cfg_
        CONF = self

    def get_app_config(self):
        return self._app_config_

    def setup(self):
        sections = self._cfg_.sections()
        for section in sections:
            opt_group = getattr(self, section, None)
            if not opt_group:
                self.app.logger.warning("Cannot find section: %s" % section)
                continue

            opts = self._cfg_.options(section)
            for opt in opts:
                value = getattr(opt_group, opt, None)
                if value is None:
                    self.app.logger.warning("Cannot find option: %s" % opt)
                    continue

                opt_obj = opt_group.get_opt_obj(opt)
                if opt_obj.app_config:
                    self._app_config_[opt_obj.app_config] = value

    def __getattribute__(self, item):
        groups = super(ConfigOpts, self).__getattribute__('_groups_')
        value = super(ConfigOpts, self).__getattribute__(item)
        try:
            if issubclass(value, ConfigGroup):

                if item in groups:
                    return groups.get(item)

                group_obj = value()
                groups[item] = group_obj
                return group_obj
        except:
            pass

        return value


class ConfigGroup(object):
    __cfg__ = None

    def __init__(self):
        self._opts_ = {}

    def get_opt_obj(self, name):
        return super(ConfigGroup, self).__getattribute__(name)

    def __getattribute__(self, name):
        opts = super(ConfigGroup, self).__getattribute__("_opts_")
        value = super(ConfigGroup, self).__getattribute__(name)

        try:
            opt_flag = isinstance(value, opt.BaseOpt)
        except:
            opt_flag = False

        if opt_flag:
            if name in opts:
                return opts[name]

            try:
                config_value = self.__cfg__.get(self.__class__.__name__, name)
                value = value.fromat(config_value)
                opts[name] = value

            except opt.ValueTypeError as e:
                raise e

            except:
                value = value.get_deafult()
                opts[name] = value

        return value
