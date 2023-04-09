from config import ConfigurationSet, config_from_python

from .configs import base, env


__all__ = [
    'Settings'
]


Settings = ConfigurationSet(
    config_from_python(base, separator='__'),
    config_from_python(env, separator='__'),
)
