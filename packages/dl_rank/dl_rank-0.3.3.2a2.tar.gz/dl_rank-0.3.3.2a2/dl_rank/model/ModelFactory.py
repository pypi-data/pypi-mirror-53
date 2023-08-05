import tensorflow as tf
import logging
from .wide_and_deep import wdl
from .xcross import xcross
from .xdeepfm import xdeepfm
from .dcn import dcn
from .deepfm_v2 import deepfm as deepfm_v2
from .deepfm import deepfm
from .wide_deep_traditional_attention import wide_and_deep as wide_and_deep_traditional_attention



class modelFactory(object):
    model_dict = {'wdl': wdl, 'xcross': xcross, 'dcn': dcn, 'xdeepfm': xdeepfm, 'deepfm': deepfm,
                  'deepfm_v2': deepfm_v2, 'wide_and_deep_traditional_attention': wide_and_deep_traditional_attention}
    @staticmethod
    def build(train_conf, model_conf, mode):
        model_type = train_conf['model_type']
        Model = modelFactory.model_dict[model_type](model_conf, mode)
        return Model

    @staticmethod
    def register(model):
        name = model.name
        if name in modelFactory.model_dict:
            print('name: {} has been used'.format(name))
        else:
            modelFactory.model_dict.update({name: model})


