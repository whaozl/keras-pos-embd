import unittest
import os
import tempfile
import random
import keras
import numpy as np
from keras_pos_embd import PositionEmbedding


class TestPosEmbd(unittest.TestCase):

    def test_index(self):
        indices = np.asarray([[-4, 10]])
        weights = np.random.random((21, 2))
        weights[6, :] = np.asarray([0.25, 0.1])
        weights[20, :] = np.asarray([0.6, -0.2])
        model = keras.models.Sequential()
        model.add(PositionEmbedding(
            input_dim=10,
            output_dim=2,
            input_shape=(None,),
            weights=[weights],
            name='Pos-Embd',
        ))
        model.compile('adam', keras.losses.mae, [keras.metrics.mae])
        model_path = os.path.join(tempfile.gettempdir(), 'keras_self_att_test_save_load_%f.h5' % random.random())
        model.save(model_path)
        model = keras.models.load_model(model_path, custom_objects=PositionEmbedding.get_custom_objects())
        model.summary()
        predicts = model.predict(indices)
        expected = np.asarray([[
            [0.25, 0.1],
            [0.6, -0.2],
        ]])
        self.assertTrue(np.allclose(expected, predicts))

    def test_mask_zero(self):
        indices = np.asarray([[-4, 10, 100]])
        weights = np.random.random((21, 2))
        weights[6, :] = np.asarray([0.25, 0.1])
        weights[20, :] = np.asarray([0.6, -0.2])
        model = keras.models.Sequential()
        model.add(PositionEmbedding(
            input_dim=10,
            output_dim=2,
            mask_zero=100,
            input_shape=(None,),
            weights=[weights],
            name='Pos-Embd',
        ))
        model.build()
        model.compile('adam', keras.losses.mae, [keras.metrics.mae])
        model_path = os.path.join(tempfile.gettempdir(), 'keras_self_att_test_save_load_%f.h5' % random.random())
        model.save(model_path)
        model = keras.models.load_model(model_path, custom_objects=PositionEmbedding.get_custom_objects())
        model.summary()
        predicts = model.predict(indices)
        expected = np.asarray([[
            [0.25, 0.1],
            [0.6, -0.2],
            [0.6, -0.2],
        ]])
        self.assertTrue(np.allclose(expected, predicts))
