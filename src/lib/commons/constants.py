import os

ANPR_CONFIGS = os.environ.get("ANPR_CONFIGS", "configs")
OPEN_ALPR_CONFIG = os.environ.get("OPEN_ALPR_CONFIG", "/usr/share/openalpr/config/alprd.defaults.conf")
OPEN_ALPR_RUNTIME = os.environ.get("OPEN_ALPR_RUNTIME", "/usr/share/openalpr/runtime_data")