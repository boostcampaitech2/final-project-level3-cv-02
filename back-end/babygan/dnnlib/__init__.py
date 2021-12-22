# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

from . import submission
from .submission.run_context import RunContext

from .submission.submit import SubmitTarget
from .submission.submit import PathType
from .submission.submit import SubmitConfig
from .submission.submit import get_path_from_template
from .submission.submit import submit_run

from .util import EasyDict

from . import tflib 
from .tflib import autosummary
from .tflib import network
from .tflib import optimizer
from .tflib import tfutil
from .tflib.tfutil import *
from .tflib.network import Network

from .tflib.optimizer import Optimizer


submit_config: SubmitConfig = None # Package level variable for SubmitConfig which is only valid when inside the run function.
