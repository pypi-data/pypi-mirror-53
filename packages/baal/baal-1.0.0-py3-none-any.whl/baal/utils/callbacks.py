# this code is taken from keras/keras/callbacks.py and adopted to our
# implementation of models in pytorch.
import os
import time
import warnings
from collections import deque

import numpy as np
import torch


class CallbackList(object):
    """Container abstracting a list of callbacks.
    Args:
        callbacks (list): List of `Callback` instances.
        queue_length (int): Queue length for keeping
            running statistics over callback execution time.
    """

    def __init__(self, callbacks=None, queue_length=10):
        callbacks = callbacks or []
        self.callbacks = [c for c in callbacks]
        self.queue_length = queue_length

    def append(self, callback):
        self.callbacks.append(callback)

    def set_params(self, params):
        for callback in self.callbacks:
            callback.set_params(params)

    def set_trainer(self, model):
        for callback in self.callbacks:
            callback.set_trainer(model)

    def set_optimizer(self, optimizer):
        for callback in self.callbacks:
            callback.set_optimizer(optimizer)

    def on_epoch_begin(self, epoch, logs=None):
        """Called at the start of an epoch.
        Args:
            epoch (int): index of epoch.
            logs (dict()): dictionary of logs.
        """
        logs = logs or {}
        for callback in self.callbacks:
            callback.on_epoch_begin(epoch, logs)
        self._delta_t_batch = 0.0
        self._delta_ts_batch_begin = deque([], maxlen=self.queue_length)
        self._delta_ts_batch_end = deque([], maxlen=self.queue_length)

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch.
        Args:
            epoch (int): index of epoch.
            logs (dict()): dictionary of logs.
        """
        logs = logs or {}
        for callback in self.callbacks:
            callback.on_epoch_end(epoch, logs)

    def on_batch_begin(self, batch, logs=None):
        """Called right before processing a batch.
        Args:
            batch (int): index of batch within the current epoch.
            logs (dict()): dictionary of logs.
        """
        logs = logs or {}
        t_before_callbacks = time.time()
        for callback in self.callbacks:
            callback.on_batch_begin(batch, logs)
        self._delta_ts_batch_begin.append(time.time() - t_before_callbacks)
        delta_t_median = np.median(self._delta_ts_batch_begin)
        if (
            self._delta_t_batch > 0.0
            and delta_t_median > 0.95 * self._delta_t_batch
            and delta_t_median > 0.1
        ):
            warnings.warn(
                "Method on_batch_begin() is slow compared "
                "to the batch update (%f). Check your callbacks." % delta_t_median
            )
        self._t_enter_batch = time.time()

    def on_batch_end(self, batch, logs=None):
        """Called at the end of a batch.
        Args:
            batch (int): index of batch within the current epoch.
            logs (dict()): dictionary of logs.
        """
        logs = logs or {}
        if not hasattr(self, "_t_enter_batch"):
            self._t_enter_batch = time.time()
        self._delta_t_batch = time.time() - self._t_enter_batch
        t_before_callbacks = time.time()
        for callback in self.callbacks:
            callback.on_batch_end(batch, logs)
        self._delta_ts_batch_end.append(time.time() - t_before_callbacks)
        delta_t_median = np.median(self._delta_ts_batch_end)
        if self._delta_t_batch > 0.0 and (
            delta_t_median > 0.95 * self._delta_t_batch and delta_t_median > 0.1
        ):
            warnings.warn(
                "Method on_batch_end() is slow compared "
                "to the batch update (%f). Check your callbacks." % delta_t_median
            )

    def on_train_begin(self, logs=None):
        """Called at the beginning of training.
        Args:
            logs (dict()): dictionary of logs.
        """
        logs = logs or {}
        for callback in self.callbacks:
            callback.on_train_begin(logs)

    def on_train_end(self, logs=None):
        """Called at the end of training.
        Args:
            logs(dict()): dictionary of logs.
        """
        logs = logs or {}
        for callback in self.callbacks:
            callback.on_train_end(logs)

    def __iter__(self):
        return iter(self.callbacks)


class Callback(object):
    """
    Abstract base class used to build new callbacks.
    """

    def __init__(self):
        pass

    def set_params(self, params):
        self.params = params

    def set_trainer(self, model):
        self.trainer = model

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def on_epoch_begin(self, epoch, logs=None):
        pass

    def on_epoch_end(self, epoch, logs=None):
        pass

    def on_batch_begin(self, batch, logs=None):
        pass

    def on_batch_end(self, batch, logs=None):
        pass

    def on_train_begin(self, logs=None):
        pass

    def on_train_end(self, logs=None):
        pass


class ModelCheckPoints(Callback):
    """
    To save model checkpoints during training.
    """

    def __init__(
        self, ckp_path, active_set, model, optim, save_fr=5, max_save=5, verbose=0,
        key='val'
    ):
        """
        For time being it is meant to only save the check points which are better.
        Also the complete checkpoints will be saved. The option to save only the
        weights could be added up on necessity.
        Args:
            ckp_path (str): the directory where the checkpoints will be saved.
            active_set (torch.Dataset): the active dataset
            model (nn.Module): torch model
            optim (nn.Module): torch optimizer
            save_fr (int): the frequency of saving the checkpoints based on epochs.
            max_save (int): maximum number of checkpoints to keep in the directory.
            verbose (int {0, 1}): turn on printing the changes.
            key (str): Key in logs to look at.
        """
        self.model = model
        self.optim = optim
        self.active_set = active_set
        self.ckp_path = ckp_path
        self.save_fr = save_fr
        self.max_sav = max_save
        self.verbose = verbose
        self.key = key
        self.epoch = 0
        self.best_loss = float("inf")

        super(ModelCheckPoints, self).__init__()

    def on_train_begin(self, logs=None):
        files = os.listdir(self.ckp_path)
        if len(files) > 0:
            files.sort(
                key=lambda file: os.path.getmtime(os.path.join(self.ckp_path, file))
            )
            ckp_path = os.path.join(self.ckp_path, files[-1])
            ckp = torch.load(ckp_path)
            self.model.load_state_dict(ckp['state_dict'])
            self.active_set._labelled = ckp['labeled_data']
            if logs is not None:
                logs['epoch'] = ckp['epoch']
                logs['is_best'] = ckp['is_best']
            self.optim.load_state_dict(ckp['optimizer'])

            if self.verbose:
                print("=>> loading from checkpoint epoch")

        elif self.verbose:
            print(" no checkpoints is saved")

    def on_epoch_end(self, epoch, logs=None):
        is_best = False
        if self.best_loss > float(logs.get(self.key)):
            self.best_loss = float(logs.get(self.key))
            is_best = True

        if epoch % self.save_fr == 0 and is_best:
            ckp = logs
            ckp['state_dict'] = self.model.state_dict()
            ckp['optimizer'] = self.optim.state_dict()
            ckp['is_best'] = is_best
            file_name = os.path.join(self.ckp_path, 'model_{}.pth'.format(logs[self.key]))
            torch.save(ckp, file_name)

            if self.verbose > 0:
                print("=> saving checkpoint")

            if len(os.listdir(self.ckp_path)) > self.max_sav:
                files = os.listdir(self.ckp_path)
                files.sort(
                    key=lambda file: os.path.getmtime(os.path.join(self.ckp_path, file))
                )
                os.remove(os.path.join(self.ckp_path, files[0]))

                if self.verbose > 0:
                    print(files[0], "is removed.")
