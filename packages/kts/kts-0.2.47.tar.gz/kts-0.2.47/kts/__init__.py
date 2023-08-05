import os
import sys
sys.path.insert(0, '.')


# from .environment import get_mode
# get_mode()
from . import config
from .feature.decorators import preview, register, deregister, dropper, selector, helper
from .feature import stl
from .feature.storage import feature_list as features
from .feature import helper_list as helpers
from .feature.storage import FeatureSet
from .validation.experiment import experiment_list as experiments
from .validation import Validator
from .modelling import model
from .storage.dataframe import link
from .storage import cache
from .storage.dataframe import DataFrame as KTDF
from .storage.caching import save, load, ls, remove, rm
from .validation.leaderboard import leaderboard
lb = leaderboard
from . import zoo
from .ensembling import stack
# from .submission import submit
from . import eda
from .feature import selection

# import mprop
#
# @property
# def __version__(kts):
#     ans = os.popen(f'{sys.executable} -m pip show kts').read().split()
#     return [ans[i + 1] for i in range(len(ans)) if 'version' in ans[i].lower()][0]
#
# mprop.init()