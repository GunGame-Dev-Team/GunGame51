# Declare all config *.py files located in the "core.cfg.files" directory
__all__ = ['gg_en_config', 'gg_default_addons', 'gg_map_vote']

for addon in __all__:
    # Load and execute all configs in the "core.cfg.files" directory
    __import__('gungame51.core.cfg.files.%s' %addon, fromlist=['core.cfg.files']).load()