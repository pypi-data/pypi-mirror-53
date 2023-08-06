# -*- coding: utf-8 -*-
"""
module model.py
--------------------
Definition of the machine learning model for the task.
"""
import tensorflow as tf
import numpy as np
from blinker import signal
from ..config.config import Config
from .distributed_learner import DistributedLearner
from ..dataset import Dataset
from .distributed_strategy_manager import DistrubutedStrategyManager
from .distributed_dataset import DistributedDataset
from ..callbacks import before_session_initialization, on_validate_begin, on_epoch_begin
import time


class Inputs(object):
    def __init__(self):
        pass


class Outputs(object):
    def __init__(self):
        pass


class Model(object):
    """ Project main class.
    """
    def __init__(self, inputs_config, config: Config=None):
        """
        Main module initialization.
        :param inputs_config: inputs shapes, types and names definitions. **keys**: name, output_types, output_shapes
                              **format**:
                              {
                                names: (tuple of strings. variable names),
                                output_types: (tuple of tf.Dtype. foreach variable),
                                output_shapes= (tuple of tf.TensorShape. foreach variable)
                              }
        :type inputs_config: dict
        :param config: a configuration object.
        :type config: Config
        """
        self.distributed_strategy = DistrubutedStrategyManager()
        self.config = config
        self._inputs_config = inputs_config

        self.inputs = Inputs()
        # set in _ get_model
        self.outputs = Outputs()

        self._loss_metrics_and_updates = None
        self._loss_and_metrics = None

        with self.distributed_strategy.scope():
            _is_training_phase, _assign_true, _assign_false = self._learning_phase_init()
            self._is_training_phase = _is_training_phase
            self._phase_to_true = _assign_true
            self._phase_to_false = _assign_false

        self._built = False
        self._is_session_initialized = False

    def _learning_phase_init(self):
        with tf.variable_scope("learning_phase", reuse=tf.AUTO_REUSE):
            _is_training_phase = tf.get_variable(
                name="is_training_phase",
                dtype=tf.bool,
                initializer=False,
                trainable=False,
            )
            _assign_true = tf.assign(_is_training_phase, True)
            _assign_false = tf.assign(_is_training_phase, False)
            return _is_training_phase, _assign_true, _assign_false

    @property
    def is_training_phase(self):
        """
        Getter for the current set training phase flag.
        :return: True: if the model is set to behave according to the training phase.
                 False: for evaluation and prediction behavior.
        """
        sess = tf.get_default_session()
        is_training = sess.run(self._is_training_phase)
        return is_training

    @is_training_phase.setter
    def is_training_phase(self, value):
        """
        Setter for the current set training phase flag.
        :param value: a boolean indication the new current flag.
                      True: if the model is set to behave according to the training phase.
                      False: for evaluation and prediction behavior.
        """
        sess = tf.get_default_session()
        # if session was not initialized yet
        # then initialize the is_learning_phase variable
        # assing the new phase value to the variable
        if value is True:
            sess.run(self._phase_to_true)
        else:
            sess.run(self._phase_to_false)

    def _fill_inputs(self, inputs):
        """
        Fills the inputs attributes within the inputs_config and dataset next_elements.
        """
        # for each variable name and tensor
        for tensor_name, tensor in zip(self._inputs_config["names"], inputs):
            setattr(self.inputs, tensor_name, tensor)

    def get_model_spec(self, *args, **kwargs):
        """
        Model's layers definitions.
        """
        pass

    def get_loss_and_metrics(self, inputs, outputs) -> (list, list):
        raise NotImplementedError()

    def get_losses(self, inputs, outputs):
        raise NotImplementedError()

    def get_optimizer(self):
        raise NotImplementedError()

    def fit(self, train_dataset: Dataset, valid_dataset: Dataset=None, resume=False, learner=DistributedLearner):

        # ensures train and valid datasets callbacks are disconected
        from ..callbacks import before_session_initialization, on_validate_begin, on_epoch_begin
        on_epoch_begin.disconnect(train_dataset.initialize_iterator)
        before_session_initialization.disconnect(train_dataset.get_iterator_initializer)

        if valid_dataset is not None:
            on_validate_begin.disconnect(valid_dataset.initialize_iterator)
            before_session_initialization.disconnect(valid_dataset.get_iterator_initializer)

        # builds the distributed dataset wrapper
        distributed_ds = DistributedDataset(
            partitions={
                "train": train_dataset,
                "valid": valid_dataset
            },
            inputs_config=self._inputs_config,
            config=self.config
        )
        self._build(distributed_ds)

        _learner = learner(self, self._loss_metrics_and_updates, distributed_ds, resume=resume)
        _learner.fit()

    def _build(self, dataset:DistributedDataset):
        """builds the model tensor graph."""
        if self._built:
            return

        _inputs = dataset.get_next()
        with self.distributed_strategy.scope():
            model_outputs, loss_and_metrics, update_op = self.distributed_strategy.strategy.experimental_run_v2(
                self._build_fn, args=_inputs
            )

            # traking loss metrics and updates nodes (tensors/operations)
            _loss_metrics_and_updates = dict()
            for key, value in loss_and_metrics.items():
                _loss_metrics_and_updates[key] = self.distributed_strategy.strategy.reduce(
                    tf.distribute.ReduceOp.SUM,
                    value,
                    axis=None
                )
                _loss_metrics_and_updates["update_op"] = update_op
            self._loss_metrics_and_updates = _loss_metrics_and_updates

            # filling the model's output attributes
            for key, value in model_outputs.items():
                out = self.distributed_strategy.strategy.reduce(
                    tf.distribute.ReduceOp.SUM,
                    value,
                    axis=None
                )
                setattr(self.outputs, key, out)

            # filling the model's input attributes
            self._fill_inputs(_inputs)

            self._built = True

    def _build_fn(self, *inputs):
        model_outputs = self.get_model_spec(inputs)
        losses, metrics = self.get_loss_and_metrics(inputs, model_outputs)
        outputs = self._prepare_outputs(losses, metrics)
        optimizer = self.get_optimizer()
        global_step = tf.train.get_or_create_global_step()
        train_op = optimizer.minimize(outputs["loss"], global_step=global_step)

        return model_outputs, outputs, train_op

    def _initialize_session(self):
        """Default session initialization function."""
        if not self._is_session_initialized:
            # tf global variables initialization (session variables initialization)
            sess = tf.get_default_session()
            sess.run(tf.global_variables_initializer())
            self._is_session_initialized = True

    def _prepare_outputs(self, losses, metrics, step="train"):
        """Builds the outputs dictionary that is used during the model fitting."""
        batch_size = int(self.config.get("flow.batch_size", 1))

        # with self.distributed_strategy.scope():
        outputs = dict()
        outputs["loss"] = tf.add_n(losses, name="loss")

        for m in losses:
            name = m.name.split(":")[0]
            if name not in outputs:
                if step == "train" and not name.startswith("valid_"):
                    outputs[name] = m
                elif step is not "train":
                    outputs[name] = m

        for m in metrics:
            name = m.name.split(":")[0]
            if name not in outputs:
                if step == "train" and not name.startswith("valid_"):
                    outputs[name] = m
                elif step is not "train":
                    outputs[name] = m
        return outputs

    def evaluate(self, dataset: DistributedDataset, partition="valid"):
        """
        Returns the loss value & metrics values for the model in test mode.
        Computation is done in batches.
        """
        # loads model if it is not initialized.
        if not self._built:
            self._build(dataset)

        model_path = self.config.get("flow.PREMODEL", None)
        if not self._is_session_initialized:
            self.load(tf.train.latest_checkpoint(model_path))
            self._is_session_initialized = True

        # dataset iterator initialization
        dataset.initialize_iterator(self, partition)

        # ensures that learning_pahse is False
        self.is_training_phase = False

        # prepare validation outputs
        if self._loss_and_metrics is None:
            outs = {key:value for key, value in self._loss_metrics_and_updates.items() if key is not "update_op"}
            self._loss_and_metrics = outs

        # builds a dictionary containing a key for each step output.
        # The outputs of each learning step is stored on this dictionary.
        accumulators = dict()
        for output_name in self._loss_and_metrics.keys():
            accumulators[output_name] = list()

        batch_size = int(self.config.get("FLOW.BATCH_SIZE", 1))
        sess = tf.get_default_session()
        try:
            while True:
                ret = sess.run(
                    fetches=self._loss_and_metrics
                )
                # accumulate outputs
                for key, val in ret.items():
                    accumulators[key].append(val * batch_size)

        except tf.errors.OutOfRangeError:
            pass

        results = dict()
        for output_name, output_vals in accumulators.items():
            size = len(output_vals)
            results[output_name] = np.sum(output_vals) / (size * batch_size)

        return results

    def load(self, path):
        """
        Loads a saved model.
        :param path: the saved model path.
        """
        with self.distributed_strategy.scope():
            sess = tf.get_default_session()
            saver = tf.train.Saver()
            print("restoring model....")
            saver.restore(
                sess,
                path
            )

    def predict(self, dataset: DistributedDataset, outputs, partition="test", **kwargs):
        """
        Predicts the asked tensors using the model.
        This method loads a pre-trained model and its weights if the model was not initialized yeat.
        :param dataset: dataset to be used for predictions.
        :param outputs: model tensor's and it names to be predicted.
        :param partition: the dataset partition name to be predicted.
        :param feed_dict: feedable placeholders dict.
        :param kwargs: named parameters dictionary.
        :return: a dictionary containing the asked tensors predictions as values,
                 associated to the asked names as keys.
        """

        model_path = self.config.get("flow.PREMODEL", None)
        if not self._is_session_initialized:
            self.load(tf.train.latest_checkpoint(model_path))
            self._is_session_initialized = True

        sess = tf.get_default_session()
        # dataset iterator initialization
        dataset.initialize_iterator(self, partition)
        self.is_training_phase = False

        # predict
        feed_dict = kwargs.get("feed_dict", None)
        try:
            while True:
                results = sess.run(fetches=outputs, feed_dict=feed_dict)
                yield results
        except tf.errors.OutOfRangeError:
            raise StopIteration()
