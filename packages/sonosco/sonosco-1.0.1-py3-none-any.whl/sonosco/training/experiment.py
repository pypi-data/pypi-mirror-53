import os
import os.path as path
import datetime
import torch
import logging
import numpy as np
import sonosco.common.path_utils as path_utils
import sonosco.common.utils as utils

from random import random
from typing import TypeVar
from .trainer import ModelTrainer
from .callbacks.model_checkpoint import ModelCheckpoint
from .tb_callbacks import TensorBoardCallback
from sonosco.serialization import Serializer

from time import time

LOGGER = logging.getLogger(__name__)

Experiment = TypeVar("Experiment")


class Experiment:
    """
    Generates a folder where all experiments will be stored an then a named experiment with current
    timestamp and provided name. Automatically starts logging the console output and creates a copy
    of the currently executed code in the experiment folder. The experiment's subfolder paths are provided
    to the outside as member variables. It also allows adding of more subfolders conveniently.

    Args:
        experiment_name (string): name of the exerpiment to be created
        logger: python logger from logging package
        seed: experiment seed
        experiments_path (string): location where all experiments will be stored, default is './experiments'
        config: configurations from which to initialize the experiment object
        sub_directories: iterable of strings with the names of subdirectories
        exclude_dirs: iterable of strings with names of directories which should be excluded from being copied
        exclude_files: iterables of strings with names of files which should be excluded from copying
    """
    def __init__(self,
                 experiment_name,
                 logger: logging.Logger = LOGGER,
                 seed: int = None,
                 experiments_path=None,
                 config: dict = None,
                 sub_directories=("plots", "logs", "code", "checkpoints"),
                 exclude_dirs=('__pycache__', '.git', 'experiments'),
                 exclude_files=('.pyc',)):
        self.config = config
        self.name = self._set_experiment_name(experiment_name)
        # Path to current experiment
        self.experiment_path = path.join(self._set_experiments_dir(experiments_path), self.name)
        if seed is not None:
            self._set_seed(seed)
        self.__trainer: ModelTrainer = None
        self.logger = logger

        self.logs_path = path.join(self.experiment_path, "logs")
        self.plots_path = path.join(self.experiment_path, "plots")
        self.checkpoints_path = path.join(self.experiment_path, "checkpoints")
        self.code_path = path.join(self.experiment_path, "code")
        self._sub_directories = sub_directories

        self._exclude_dirs = exclude_dirs
        self._exclude_files = exclude_files

        self._serializer = Serializer()

        self._init_directories()
        self._copy_sourcecode()
        self._set_logging()

    @staticmethod
    def _set_experiments_dir(experiments_path: str) -> str:
        """
        Set experiment directory.

        Args:
            experiments_path: experiment path

        Returns: Path to the experiments folder

        """
        if experiments_path is not None:
            return experiments_path

        local_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        local_path = local_path if local_path != '' else './'
        return path.join(local_path, "experiments")

    @staticmethod
    def _set_experiment_name(experiment_name: str) -> str:
        """
        Set experiment name.

        Args:
            experiment_name: experiment name

        Returns: timestamped experiment name

        """
        date_time = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d_%H:%M:%S')
        return f"{date_time}_{experiment_name}"

    @staticmethod
    def _set_seed(seed: int) -> None:
        """
        Set experiment seed.

        Args:
            seed: seed

        """
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        np.random.seed(seed)
        random.seed(seed)

    def _set_logging(self) -> None:
        """
        Set logging to be forwarded to the logs folder inside of the experiment.
        """
        utils.add_log_file(path.join(self.logs_path, "logs"), self.logger)

    def _init_directories(self) -> None:
        """
        Create all basic directories.
        """
        path_utils.try_create_directory(self.experiment_path)
        for sub_dir_name in self._sub_directories:
            self.add_directory(sub_dir_name)

    def _add_member(self, key: str, value: str) -> None:
        """
        Add a member variable named 'key' with value 'value' to the experiment instance.
        """
        self.__dict__[key] = value

    def _copy_sourcecode(self) -> None:
        """
        Copy code from execution directory in experiment code directory.
        """
        sources_path = os.path.dirname(os.path.dirname(__file__))
        sources_path = sources_path if sources_path != '' else './'
        utils.copy_code(sources_path, self.code_path,
                        exclude_dirs=self._exclude_dirs,
                        exclude_files=self._exclude_files)

    def add_directory(self, dir_name: str) -> None:
        """
        Add a sub-directory to the experiment. The directory will be automatically
        created and provided to the outside as a member variable.

        Args:
            dir_name: directory name
        """
        # store in sub-dir list
        if dir_name not in self._sub_directories:
            self._sub_directories.append(dir_name)
        # add as member
        dir_path = path.join(self.experiment_path, dir_name)
        self._add_member(dir_name, dir_path)
        # create directory
        path_utils.try_create_directory(dir_path)

    def setup_model_trainer(self, trainer: ModelTrainer, checkpoints: bool = True, tensorboard: bool = True) -> None:
        """
        Setup a model_trainer object with specified parameters, by default with checkpoint
        callback and tensorboard callback. Add this model trainer to the model trainers dictionary.

        Args:
            trainer: model trainer object
            checkpoints: flag for saving model checkpoints after each epoch
            tensorboard: flag for creating visualization in tensorboard
        """
        self.__trainer = trainer

        if checkpoints:
            self.__trainer.add_callback(ModelCheckpoint(output_path=self.checkpoints_path, config=self.config))
        if tensorboard:
            self.__trainer.add_callback(TensorBoardCallback(log_dir=self.plots_path))

    def start(self) -> None:
        """
        Starts model trainer.
        """
        if self.__trainer is None:
            raise ValueError("Model trainer is None.")

        # TODO: add serialization after training is finished
        self.__trainer.start_training()
        self._serializer.serialize(self.__trainer, os.path.join(self.checkpoints_path, 'trainer_no_callback'),
                                   config=self.config)
        self._serializer.serialize(self.__trainer.model, os.path.join(self.checkpoints_path, 'model_no_callback'),
                                   config=self.config)
        LOGGER.info(f'Model serialization done')

    def stop(self) -> None:
        """
        Stops model trainer.
        """
        if self.__trainer is None:
            raise ValueError("Model trainer is None.")
        self.__trainer.stop_training()
        self._serializer.serialize(self.__trainer, os.path.join(self.checkpoints_path, 'trainer_no_callback'),
                                   config=self.config)
        self._serializer.serialize(self.__trainer.model, os.path.join(self.checkpoints_path, 'model_no_callback'),
                                   config=self.config)

    @staticmethod
    def add_file(folder_path: str, filename: str, content: str) -> None:
        """
        Adds a file with provided content to folder. Convenience function.
        """
        with open(path.join(folder_path, filename), 'w') as text_file:
            text_file.write(content)

    @staticmethod
    def create(config: dict, logger: logging.Logger) -> Experiment:
        """
        :param config: dict - specify a .yaml config with one or more parameters: name, seed,
        experiment_path, sub_dirs, exclude_dirs, exclude_files and read it in as a dictionary.
        :param logger: logger
        :return: Experiment with configuration specified in config dictionary
        """
        name = config.get('experiment_name', 'experiment')
        experiment_path = config.get('experiment_path', None)
        seed = config.get('global_seed', None)
        return Experiment(name, logger, seed, experiment_path, config)
