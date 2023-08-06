import sys

import numpy as np

from kts.environment.file_system import get_mode

SEED = 31337
np.random.seed(SEED)
SEEDS = np.random.randint(100, size=10)

storage_path = "../storage/"
# root_dir = '../'
index_prefix = "__kts__index_"
preview_call = 0
memory_limit = 4 * (1024**3)  # 4 Gb
mode = "local"
GOAL = "MAXIMIZE"
MAX_LEN_SOURCE = 100

# cache_mode = 'disk_and_ram'  # "disk", "disk_and_ram", "ram"
# cache_policy = 'everything'  # "everything", "service"

cache_mode, cache_policy, root_dir = get_mode()

LB_DF_NAME = "__leaderboard"

service_names = [LB_DF_NAME]


if cache_mode in ["disk", "disk_and_ram"]:
    sys.path.insert(0, root_dir)
    try:
        import kts_config as user_config
        from kts_config import *
    except:
        pass

# So dumb. I know.
# TODO: implement all this ... with pathlib
if not storage_path.endswith("/"):
    storage_path += "/"
