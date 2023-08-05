import tensorflow as tf
from poda.layers.merge import *
from poda.layers.dense import *
from poda.layers.merge import *
from poda.layers.activation import *
from poda.layers.regularizer import *
from poda.layers.convolutional import *


class InceptionResnetV2(object):
    def __init__(self, input_tensor, n_inception_a=5, n_inception_b=10, n_inception_c=5, classes=1000, batch_normalizations = True, dropout_rates=None, regularizers=None, scopes=None):
        """[summary]
        
        Arguments:
            num_classes {[type]} -- [description]
        
        Keyword Arguments:
            input_tensor {[type]} -- [description] (default: {None})
            input_shape {tuple} -- [description] (default: {(None, 300, 300, 3)})
            learning_rate {float} -- [description] (default: {0.0001})
            batch_normalizations {bool} -- [description] (default: {True})
        """
        self.input_tensor = input_tensor
        self.classes = classes
        self.n_inception_a = n_inception_a
        self.n_inception_b = n_inception_b
        self.n_inception_c = n_inception_c
        self.batch_normalizations = batch_normalizations
        self.dropout_rate = dropout_rates
        self.regularizer = regularizers
        self.scope = scopes

    # Stem Block
    def stem_block(self, input_tensor, batch_normalization=True):
        """[summary]
        
        Arguments:
            input_tensor {[type]} -- [description]
        
        Keyword Arguments:
            batch_normalization {bool} -- [description] (default: {True})
            scope {[type]} -- [description] (default: {None})
            reuse {[type]} -- [description] (default: {None})
        """
        with tf.compat.v1.variable_scope(self.scope, 'StemBlock', [input_tensor]):
            conv_1 = convolution_2d(input_tensor=input_tensor, number_filters=32, kernel_sizes=(3,3), paddings='VALID', stride_sizes=(2, 2), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='0_3x3')
            conv_2 = convolution_2d(input_tensor=conv_1, number_filters=32, kernel_sizes=(3,3), paddings='VALID', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='0_3x3')
            conv_3 = convolution_2d(input_tensor=conv_2, number_filters=64, kernel_sizes=(3,3), paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='0_3x3')
            with tf.compat.v1.variable_scope('Branch_0'):
                max_pool_1 = max_pool_2d(input_tensor=conv_3, pool_sizes=(3,3), stride_sizes=(2,2), paddingss='VALID', names='0a_3x3')
            with tf.compat.v1.variable_scope('Branch_1'):
                conv_4 = convolution_2d(input_tensor=conv_3, number_filters=96, kernel_sizes=(3,3), paddings='VALID', stride_sizes=(2,2), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='0b_3x3')
            
            with tf.compat.v1.variable_scope('Concatenate_1'):
                concat_1 = concatenate(list_tensor=[conv_4,max_pool_1], axis=-1, names='conv_3x3_maxpool_3x3')

            with tf.compat.v1.variable_scope('Branch_3'):
                conv_5 = convolution_2d(input_tensor=concat_1, number_filters=64, kernel_sizes=(1,1), paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='0a_1x1')
                conv_6 = convolution_2d(input_tensor=conv_5, number_filters=96, kernel_sizes=(3,3), paddings='VALID', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='1a_3x3')
            with tf.compat.v1.variable_scope('Branch_4'):
                conv_7 = convolution_2d(input_tensor=concat_1, number_filters=64, kernel_sizes=(1,1), paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='0b_1x1')
                conv_8 = convolution_2d(input_tensor=conv_7, number_filters=64, kernel_sizes=(7,1), paddings='SAME', stride_sizes=(1, 1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='1b_7x1')
                conv_9 = convolution_2d(input_tensor=conv_8, number_filters=64, kernel_sizes=(1,7), paddings='SAME', stride_sizes=(1, 1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='2b_1x7')
                conv_10 = convolution_2d(input_tensor=conv_9, number_filters=96, kernel_sizes=(3,3), paddings='VALID', stride_sizes=(1, 1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='3b_3x3')
            
            with tf.compat.v1.variable_scope('Concatenate_2'):
                concat_2 = concatenate(list_tensor=[conv_6,conv_10], axis=-1, names='conv_3x3_conv_3x3')

            with tf.compat.v1.variable_scope('Branch_5'):
                conv_11 = convolution_2d(input_tensor=concat_2, number_filters=192, kernel_sizes=(3,3), paddings='VALID', stride_sizes=(2,2), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, name='0a_3x3')
            with tf.compat.v1.variable_scope('Branch_6'):
                max_pool_2 = max_pool_2d(input_tensor=concat_2, pool_sizes=(3,3), stride_sizes=(2,2), paddingss='VALID', names='0b_3x3')
            
            with tf.compat.v1.variable_scope('Concatenate_3'):
            concat_3 = concatenate(list_tensor=[max_pool_2,conv_11], axis=-1, names='maxpool_3x3_conv_3x3')
        return concat_3
    
    # Inception A
    def inception_resnet_a(self, input_tensor, batch_normalization=True):
        """[summary]
        
        Arguments:
            input_tensor {[type]} -- [description]
        
        Keyword Arguments:
            batch_normalization {bool} -- [description] (default: {True})
            scope {[type]} -- [description] (default: {None})
            reuse {bool} -- [description] (default: {True})
        """
        with tf.compat.v1.variable_scope(self.scope, 'BlockInceptionResnetA', [input_tensor]):
            with tf.compat.v1.variable_scope('Relu_1'):
                relu_1 = relu(input_tensor=input_tensor, names='input_inception_resnet_a')
            with tf.compat.v1.variable_scope('Branch_0'):
                conv_1 = convolution_2d(input_tensor=relu_1, number_filters=32, kernel_sizes=(1,1), paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='0a_1x1')
            with tf.compat.v1.variable_scope('Branch_1'):
                conv_2 = convolution_2d(input_tensor=relu_1, number_filters=32, kernel_sizes=(1,1), paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='0b_1x1')
                conv_3 = convolution_2d(input_tensor=conv_2, number_filters=32, kernel_sizes=(3,3), paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='1b_3x3')
            with tf.compat.v1.variable_scope('Branch_2'):
                conv_4 = convolution_2d(input_tensor=relu_1, number_filters=32, kernel_sizes=(1,1) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='0c_1x1')
                conv_5 = convolution_2d(input_tensor=conv_4, number_filters=48, kernel_sizes=(3,3) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='1c_3x3')
                conv_6 = convolution_2d(input_tensor=conv_5, number_filters=64, kernel_sizes=(3,3) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='2c_3x3')
            
            with tf.compat.v1.variable_scope('Concatenate_1'):
                concat_1 = concatenate(list_tensor=[conv_1,conv_3,conv_6], axis=-1, names='conv_1x1_conv_3x3_conv_3x3')
            
            with tf.compat.v1.variable_scope('Branch_1c'):
                conv_7 = convolution_2d(input_tensor=concat_1, number_filters=384, kernel_sizes=(1,1) , paddings='SAME', stride_sizes=(1,1), activations=None, batch_normalizations=batch_normalization, dropout_rates=self.dropout_rate, names='0aa_1x1')
            with tf.compat.v1.variable_scope('Add_1'):
                add_1 = add(input_tensor_1=relu_1, input_tensor_2=conv_7, names='input_conv_1x1')

            with tf.compat.v1.variable_scope('Relu_2'):
                relu_2 = relu(input_tensor=add_1, names='output_inception_resnet_a')
        return relu_2    
    
    # Reduction A
    def reduction_a(self, input_tensor, batch_normalization=True):
        """[summary]
        
        Arguments:
            input_tensor {[type]} -- [description]
        
        Keyword Arguments:
            batch_normalization {bool} -- [description] (default: {True})
            scope {[type]} -- [description] (default: {None})
            reuse {[type]} -- [description] (default: {None})
        """
        with tf.compat.v1.variable_scope(self.scope, 'BlockReductionA', [input_tensor]):
            with tf.compat.v1.variable_scope('Branch_0'):
                max_pool_1 = max_pool_2d(input_tensor=input_tensor, pool_sizes=(3,3), stride_sizes=(2,2), paddings='VALID', names='0a_3x3')
            with tf.compat.v1.variable_scope('Branch_1'):
                conv_1 = convolution_2d(input_tensor=input_tensor, number_filters=384, kernel_sizes=(3,3) , stride_sizes=(2,2), activations='relu', paddings='VALID', batch_normalizations=batch_normalization, names='0b_3x3')
            with tf.compat.v1.variable_scope('Branch_2'):
                conv_2 = convolution_2d(input_tensor=input_tensor, number_filters=256, kernel_sizes=(1,1) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, names='0c_1x1')
                conv_3 = convolution_2d(input_tensor=conv_2, number_filters=256, kernel_sizes=(3,3) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, names='1c_3x3')
                conv_4 = convolution_2d(input_tensor=conv_3, number_filters=384, kernel_sizes=(3,3) , paddings='VALID', stride_sizes=(2,2), activations='relu', batch_normalizations=batch_normalization, names='2c_3x3')
            with tf.compat.v1.variable_scope('Concatenate_1'):
                concat_1 = concatenate(list_tensor=[max_pool_1,conv_1,conv_4], axis=-1, names='maxpool_3x3_conv_3x3_conv_3x3')
        return concat_1
    
    
    # Inception B
    def inception_resnet_b(self, input_tensor, batch_normalization=True):
        """[summary]
        
        Arguments:
            input_tensor {[type]} -- [description]
        
        Keyword Arguments:
            batch_normalization {bool} -- [description] (default: {True})
            scope {[type]} -- [description] (default: {None})
            reuse {[type]} -- [description] (default: {None})
        """
        with tf.compat.v1.variable_scope(self.scope, 'BlockInceptionResnetB', [input_tensor]):
            with tf.compat.v1.variable_scope('Relu_1'):
                relu_1 = relu(input_tensor=input_tensor, names='input_inception_resnet_b')
            with tf.compat.v1.variable_scope('Branch_0'):
                conv_1 = convolution_2d(input_tensor=relu_1, number_filters=192, kernel_sizes=(1,1) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, name='0a_1x1')
            with tf.compat.v1.variable_scope('Branch_1'):
                conv_2 = convolution_2d(input_tensor=relu_1, number_filters=128, kernel_sizes=(1,1) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, name='0b_1x1')
                conv_3 = convolution_2d(input_tensor=conv_2, number_filters=160, kernel_sizes=(1,7) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, name='1b_1x7')
                conv_4 = convolution_2d(input_tensor=conv_3, number_filters=192, kernel_sizes=(7,1) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, name='2b_7x1')
            with tf.compat.v1.variable_scope('Concatenate_1'):
                concat_1 = concatenate(list_tensor=[conv_1,conv_4], axis=-1, names='conv_1x1_conv_7x1')
            with tf.compat.v1.variable_scope('Branch_1c'):
                conv_5 = convolution_2d(input_tensor=concat_1, number_filters=1154, kernel_sizes=(1,1) , paddings='SAME', stride_sizes=(1,1), activations=None, batch_normalizations=batch_normalization, name='0c_1x1')

            with tf.compat.v1.variable_scope('Add_1'):
                add_1 = add(input_tensor_1=relu_1, input_tensor_2=conv_5, names='input_conv_1x1')
        
            with tf.compat.v1.variable_scope('Relu_2'):
                relu_2 = relu(input_tensor=add_1, names='output_inception_resnet_b')

        return relu_2

    # Reduction B
    def reduction_b(self, input_tensor, batch_normalization=True):
        """[summary]
        
        Arguments:
            input_tensor {[type]} -- [description]
        
        Keyword Arguments:
            batch_normalization {bool} -- [description] (default: {True})
            scope {[type]} -- [description] (default: {None})
            reuse {[type]} -- [description] (default: {None})
        """
        with tf.compat.v1.variable_scope(self.scope, 'BlockReductionB', [input_tensor]):
            with tf.compat.v1.variable_scope('Branch_0'):
                max_pool_1 = max_pool_2d(input_tensor=input_tensor, pool_sizes=(3,3), stride_sizes=(2,2), paddings='VALID', names='0a_3x3')
            with tf.compat.v1.variable_scope('Branch_1'):
                conv_1 = convolution_2d(input_tensor=input_tensor, number_filters=256, kernel_sizes=(1,1) , stride_sizes=(1,1), paddings='SAME', activations='relu', batch_normalizations=batch_normalization, name='0b_1x1')
                conv_2 = convolution_2d(input_tensor=conv_1, number_filters=384, kernel_sizes=(3,3) , stride_sizes=(2,2), paddings='VALID', activations='relu', batch_normalizations=batch_normalization, name='1b_1x1')
            with tf.compat.v1.variable_scope('Branch_1'):
                conv_3 = convolution_2d(input_tensor=input_tensor, number_filters=256, kernel_sizes=(1,1) , stride_sizes=(1,1), paddings='SAME', activations='relu', batch_normalizations=batch_normalization, name='0c_1x1')
                conv_4 = convolution_2d(input_tensor=conv_3, number_filters=256, kernel_sizes=(3,3) , stride_sizes=(2,2), paddings='VALID', activations='relu', batch_normalizations=batch_normalization, name='1c_1x1')
            with tf.compat.v1.variable_scope('Branch_2'):
                conv_5 = convolution_2d(input_tensor=input_tensor, number_filters=256, kernel_sizes=(1,1) , stride_sizes=(1,1), paddings='SAME', activations='relu', batch_normalizations=batch_normalization, name='0d_1x1')
                conv_6 = convolution_2d(input_tensor=conv_5, number_filters=256, kernel_sizes=(3,3) , stride_sizes=(1,1), paddings='SAME', activations='relu', batch_normalizations=batch_normalization, name='1d_1x7')
                conv_7 = convolution_2d(input_tensor=conv_6, number_filters=256, kernel_sizes=(3,3) , stride_sizes=(2,2), paddings='VALID', activations='relu', batch_normalizations=batch_normalization, name='2d_3x3')
            with tf.compat.v1.variable_scope('Concatenate_1'):
                concat_1 = concatenate(list_tensor=[max_pool_1,conv_2,conv_7], axis=-1, names='maxpool_3x3_conv_3x3_conv_3x3')
        return concat_1

    # Inception C
    def inception_c(self, input_tensor, batch_normalization=True):
        """[summary]
        
        Arguments:
            input_tensor {[type]} -- [description]
        
        Keyword Arguments:
            batch_normalization {bool} -- [description] (default: {True})
            scope {[type]} -- [description] (default: {None})
            reuse {[type]} -- [description] (default: {None})
        """
        with tf.compat.v1.variable_scope(self.scope, 'BlockInceptionResnetC', [input_tensor]):
            with tf.compat.v1.variable_scope('Relu_1'):
                relu_1 = relu(input_tensor=input_tensor, names='input_inception_resnet_c')
            with tf.compat.v1.variable_scope('Branch_0'):
                conv_1 = convolution_2d(input_tensor=relu_1, number_filters=192, kernel_sizes=(1,1) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, name='0a_1x1')
            with tf.compat.v1.variable_scope('Branch_1'):
                conv_2 = convolution_2d(input_tensor=relu_1, number_filters=192, kernel_sizes=(1,1) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, name='0b_1x1')
                conv_3 = convolution_2d(input_tensor=conv_2, number_filters=224, kernel_sizes=(1,3) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, name='1b_1x3')
                conv_4 = convolution_2d(input_tensor=conv_3, number_filters=256, kernel_sizes=(3,1) , paddings='SAME', stride_sizes=(1,1), activations='relu', batch_normalizations=batch_normalization, name='2b_3x1')
            with tf.compat.v1.variable_scope('Concatenate_1'):
                concat_1 = concatenate(list_tensor=[conv_1,conv_4], axis=-1, names='conv_1x1_conv_3x1')
            with tf.compat.v1.variable_scope('Branch_1c'):
                conv_5 = convolution_2d(input_tensor=concat_1, number_filters=2048, kernel_sizes=(1,1) , paddings='SAME', stride_sizes=(1,1), activations=None, batch_normalizations=batch_normalization, name='0c_1x1')

            with tf.compat.v1.variable_scope('Add_1'):
                add_1 = add(input_tensor_1=relu_1, input_tensor_2=conv_5, names='input_conv_1x1')
        
            with tf.compat.v1.variable_scope('Relu_2'):
                relu_2 = relu(input_tensor=add_1, names='output_inception_resnet_c')

        return relu_2

    # Create Model
    def create_model(self):
        """[summary]
        
        Arguments:
            input_tensor {[type]} -- [description]
        
        Keyword Arguments:
            classes {int} -- [description] (default: {1000})
            n_inception_a {int} -- [description] (default: {4})
            n_inception_b {int} -- [description] (default: {7})
            n_inception_c {int} -- [description] (default: {3})
            batch_normalizations {bool} -- [description] (default: {True})
        """
        with tf.compat.v1.variable_scope(self.scope, 'inception_v4_resnet_v2', [self.input_tensor]):
            stem_layer = self.stem_block(input_tensor=self.input_tensor, batch_normalization=self.batch_normalizations)

            for i in range(0,self.n_inception_a):
                inception_a_layer = self.inception_a(input_tensor=stem_layer, batch_normalization=self.batch_normalizations)

            reduction_a_layer = self.reduction_a(input_tensor=inception_a_layer, batch_normalization=self.batch_normalizations)

            for j in range(0,self.n_inception_b):
                inception_b_layer = self.inception_b(input_tensor=reduction_a_layer, batch_normalization=self.batch_normalizations)

            reduction_b_layer = self.reduction_b(input_tensor=inception_b_layer, batch_normalization=self.batch_normalizations)

            for k in range(0,self.n_inception_c):
                inception_c_layer = self.inception_c(input_tensor=reduction_b_layer, batch_normalization=self.batch_normalizations)

            if n_inception_a == 0:
                inception_v4 = stem_layer
            elif n_inception_b == 0:
                inception_v4 = reduction_a_layer
            elif n_inception_c == 0:
                inception_v4 = reduction_b_layer
            else:
                inception_v4 = inception_c_layer

            base_var_list = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)

            inception_v4 = avarage_pool_2d(input_tensor=inception_v4, kernel_sizes=(3,3), paddings='SAME', stride_sizes=(1,1), names='output')

            inception_v4 =  dropout(input_tensor=inception_v4, names='output', dropout_rates=0.2)

            inception_v4 = flatten(input_tensor=inception_v4, names='output')

            full_var_list = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)

            non_logit = dense(input_tensor=inception_v4, hidden_units=self.classes, names='output')
            
            if self.classes > 2:
                output = softmax(input_tensor=non_logit, names='output')
            else:
                output = sigmoid(input_tensor=non_logit, names='output')

        return non_logit, output, base_var_list, full_var_list

