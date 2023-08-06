# -*- coding: utf-8 -*-
"""
Created on Fri May 17 15:04:04 2019

@author: quentin.chateiller
"""

# Initializing
#from . import core
#core.checkConfig()

import os
with open(os.path.join(os.path.dirname(__file__), 'version')) as version_file:
    __version__ = version_file.read().strip()
del os

from . import core
core.checkConfig()

from .core._drivers import DriverManager
drivers = DriverManager()
del DriverManager

core.devices.index = core.devices.loadIndex()

devices = core.devices.DeviceManager()

from .core.gui import gui
from .core._report import report
from .core.recorder_old.recorder import Recorder, Recorder_V2




    