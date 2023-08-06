# -*- coding: utf-8 -*-
"""
module distribute.py
--------------------
Training procedure distribution strategy.
Encapsulates the tensor flow distributed strategy methods.
"""
import tensorflow as tf
import numpy as np
from blinker import signal
from flow.config.config import Config
from flow.learner import DefaultLearner
from flow.dataset import Dataset
import time


class DistrubutedStrategyManager(object):
    """ Wrapper for distribution strategies.
    """
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self, strategy_type="mirrored"):
        """
        Strategy wrapper initialization.
        :param strategy_type: the strategy name. Allowed values: 'mirrored'
        """
        if not hasattr(self, "strategy"):
            self.config = Config()
            self.strategy_type = strategy_type
            self.visible_devices = self.get_available_gpus()
            if self.strategy_type.lower() == "mirrored":
                # If the list of devices is not specified in the
                # `tf.distribute.MirroredStrategy` constructor, it will be auto-detected.
                self.strategy = tf.distribute.MirroredStrategy()
            else:
                raise ValueError("Strategy type not recognized.")

    def scope(self):
        return self.strategy.scope()

    @staticmethod
    def get_available_gpus():
        """
        Get the name of all available gpus.
        :return: a list of all available gpus.
        """
        from tensorflow.python.client import device_lib
        all_devices = device_lib.list_local_devices()
        gpus = [x.name for x in all_devices if x.device_type == "GPU"]
        return gpus

