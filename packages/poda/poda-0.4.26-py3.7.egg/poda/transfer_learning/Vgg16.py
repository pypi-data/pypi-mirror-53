import tensorflow as tf
from poda.layers.merge import *
from poda.layers.dense import *
from poda.layers.activation import *
from poda.layers.regularizer import *
from poda.layers.convolutional import *

class VGG16(object):
    def __init__(self, input_tensor, num_blocks=5, classes=1000, batch_normalizations = True, num_depthwise_layers=None, num_dense_layers=1, num_hidden_units=4096, activation_denses='relu', dropout_rates=None, regularizers=None, scopes=None):
        """[summary]
        
        Arguments:
            object {[type]} -- [description]
            input_tensor {[type]} -- [description]
        
        Keyword Arguments:
            classes {int} -- [description] (default: {1000})
            batch_normalization {bool} -- [description] (default: {True})
        """
        self.input_tensor = input_tensor
        self.num_block = num_blocks
        self.classes = classes
        self.batch_normalization = batch_normalizations
        self.num_depthwise_layer = num_depthwise_layers
        self.num_dense_layer = num_dense_layers
        self.num_hidden_unit = num_hidden_units
        self.activation_dense = activation_denses
        self.dropout_rate = dropout_rates
        self.regularizer = regularizers
        self.scope = scopes

    def vgg_block(self, input_tensor, num_block=5, batch_normalization=True):
        with tf.compat.v1.variable_scope(self.scope, 'vgg_16', [input_tensor]):
            with tf.compat.v1.variable_scope('Block_1'):
                conv_1 = convolution_2d(input_tensor=input_tensor, number_filters=64, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_2 = convolution_2d(input_tensor=conv_1, number_filters=64, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_3 = max_pool_2d(input_tensor=conv_2, pool_sizes=(2,2), stride_sizes=(2,2), paddings='valid', names=None)
            with tf.compat.v1.variable_scope('Block_2'):
                conv_4 = convolution_2d(input_tensor=conv_3, number_filters=128, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_5 = convolution_2d(input_tensor=conv_4, number_filters=128, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_6 = max_pool_2d(input_tensor=conv_5, pool_sizes=(2,2), stride_sizes=(2,2), paddings='valid', names=None)
            with tf.compat.v1.variable_scope('Block_3'):
                conv_7 = convolution_2d(input_tensor=conv_6, number_filters=256, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_8 = convolution_2d(input_tensor=conv_7, number_filters=256, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_9 = convolution_2d(input_tensor=conv_8, number_filters=256, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_10 = max_pool_2d(input_tensor=conv_9, pool_sizes=(2,2), stride_sizes=(2,2), paddings='valid', names=None)
            with tf.compat.v1.variable_scope('Block_4'):
                conv_11 = convolution_2d(input_tensor=conv_10, number_filters=512, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_12 = convolution_2d(input_tensor=conv_11, number_filters=512, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_13 = convolution_2d(input_tensor=conv_12, number_filters=512, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_14 = max_pool_2d(input_tensor=conv_13, pool_sizes=(2,2), stride_sizes=(2,2), paddings='valid', names=None)
            with tf.compat.v1.variable_scope('Block_5'):
                conv_15 = convolution_2d(input_tensor=conv_14, number_filters=512, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_16 = convolution_2d(input_tensor=conv_15, number_filters=512, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_17 = convolution_2d(input_tensor=conv_16, number_filters=512, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=batch_normalization, dropout_rates=None, names=None)
                conv_18 = max_pool_2d(input_tensor=conv_17, pool_sizes=(2,2), stride_sizes=(2,2), paddings='valid', names=None)

        if num_block==1:
            vgg_16 = conv_3
        elif num_block==2:
            vgg_16 = conv_6
        elif num_block==3:
            vgg_16 = conv_10
        elif num_block==4:
            vgg_16 = conv_14
        elif num_block==5:
            vgg_16 = conv_18
        else:
            vgg_16 = conv_18

        return vgg_16

    def create_model(self):
        number_filter = self.input_tensor.get_shape().as_list()[-1]

        vgg_base = self.vgg_block(input_tensor=self.input_tensor, num_block=self.num_block, batch_normalization=self.batch_normalization)

        base_var_list = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)
        
        with tf.compat.v1.variable_scope(self.scope, 'vgg_16', [vgg_base]):
            if self.num_depthwise_layer!=None or self.num_depthwise_layer>0:
                for j in range(0,self.num_depthwise_layer):
                    ##### FIX THIS TOMORROW
                    vgg_base = depthwise_convolution_2d(input_tensor=vgg_base, number_filters=number_filter, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', dropout_rates=None, names=None)
            else:
                flatten_layer = flatten(input_tensor=vgg_base, names='flatten')
                for i in range(0, self.num_dense_layer):
                    vgg_base = dense(input_tensor=flatten_layer, hidden_units=self.num_hidden_unit, activations=self.activation_dense, regularizers=self.regularizer, scale=self.dropout_rate)

            
            last_layer = flatten(input_tensor=vgg_base, names='flatten')

            full_var_list = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)

            non_logit = dense(input_tensor=last_layer, hidden_units=self.classes, names='output')

            if self.classes > 2:
                output = softmax(input_tensor=non_logit, names='output')
            else:
                output = sigmoid(input_tensor=non_logit, names='output')

        return non_logit, output, base_var_list, full_var_list