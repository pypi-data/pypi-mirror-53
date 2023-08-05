# -*- coding: utf-8 -*-
from six.moves.configparser import ConfigParser
import os
from six.moves import StringIO
from six import BytesIO
from six import ensure_str
from pkgutil import get_data
from six.moves.configparser import SafeConfigParser, NoSectionError, NoOptionError


class Config(object):
    """A ConfigParser wrapper to support defaults when calling instance
    methods, and also tied to a single section"""

    SECTION = 'silkyy'

    def __init__(self, values=None, extra_sources=()):
        if values is None:
            sources = self._getsources()
            self.cp = ConfigParser()
            if __package__:
                default_config = ensure_str(get_data(__package__, 'default.conf'))
                self._load_config_file(StringIO(default_config))
            for source in sources:
                if os.path.exists(source):
                    self._load_config_file(open(source))
        else:
            self.cp = SafeConfigParser(values)
            self.cp.add_section(self.SECTION)

    def _load_config_file(self, fp):
        config = StringIO()
        config.write('[' + self.SECTION + ']' + os.linesep)
        config.write(fp.read())
        config.seek(0, os.SEEK_SET)

        self.cp.readfp(config)

    def _getsources(self):
        sources = ['conf/silkyy.conf']
        return sources

    def get(self, option, default=None):
        env_key = 'SILKYY_' + option.replace('.', '_').upper()
        try:
            return os.getenv(env_key) or self.cp.get(self.SECTION, option)
        except (NoSectionError, NoOptionError):
            if default is not None:
                return default
            raise

    def _get(self, option, conv, default=None):
        return conv(self.get(option, default))

    def getint(self, option, default=None):
        return self._get(option, int, default)

    def getboolean(self, option, default=None):
        return self._get(option, str2bool, default)

    def getfloat(self, option, default=None):
        return self._get(option, float, default)

    def items(self, section, default=None):
        try:
            return self.cp.items(section)
        except (NoSectionError, NoOptionError):
            if default is not None:
                return default
            raise
