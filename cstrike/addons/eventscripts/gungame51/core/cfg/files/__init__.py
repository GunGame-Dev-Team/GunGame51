from gungame51.core.cfg import __configs__

# Declare all config *.py files located in the "core.cfg.files" directory
__all__ = ['gg_en_config', 'gg_default_addons', 'gg_map_vote']

for config in __all__:
    # Load and execute all configs in the "core.cfg.files" directory
    __configs__.load(config)