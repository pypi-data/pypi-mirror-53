from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext


__version__ = '0.2.3'

logger = logging.getLogger(__name__)

class Extension(ext.Extension):

    dist_name = 'Mopidy-Lagukan'
    ext_name = 'lagukan'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['autostart'] = config.Boolean()
        return schema

    def setup(self, registry):
        from .frontend import LagukanFrontend
        registry.add('frontend', LagukanFrontend)
        registry.add('http:static', {
            'name': self.ext_name,
            'path': os.path.join(os.path.dirname(__file__), 'static'),
        })

    def get_command(self):
        from .commands import LagukanCommand
        return LagukanCommand()
