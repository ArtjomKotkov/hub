from config import ConfigurationSet, config_from_python

from configs import base


__all__ = [
    'Settings'
]


Settings = ConfigurationSet(
    config_from_python(base, separator='__')
)
