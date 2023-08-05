import tensorflow as tf
from poda.layers.activation import *
from poda.layers.dense import *
from poda.layers.regularizer import *

def avarage_pool_1d(input_tensor, kernel_sizes=(3), stride_sizes=(1), paddings='same', names=None):
    """[summary]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer]
    
    Keyword Arguments:
        kernel_sizes {tuple} -- [Size of kernel] (default: {(3,3)})
        stride_sizes {tuple} -- [Size of striding of kernel] (default: {(1,1)})
        paddings {str} -- [Indicating the type of padding algorithm to use] (default: {'same'})
        names {[type]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [A layer with avarage pool 2D with dtype tf.float32]
    """
    if names!=None:
        names = str(names)
    else:
        names = 'avg_pool_1d'

    if paddings=='Valid' or paddings=='valid' or paddings=='VALID':
        paddings = 'VALID'
    elif paddings=='Same' or paddings=='same' or paddings=='SAME':
        paddings = 'SAME'
    else:
        paddings = 'SAME'

    layer = tf.nn.avg_pool1d(value=input_tensor,ksize=kernel_sizes,strides=stride_sizes,padding=paddings,data_format='NHWC',name=names)
    return layer

def avarage_pool_2d(input_tensor, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', names=None):
    """[summary]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer]
    
    Keyword Arguments:
        kernel_sizes {tuple} -- [Size of kernel] (default: {(3,3)})
        stride_sizes {tuple} -- [Size of striding of kernel] (default: {(1,1)})
        paddings {str} -- [Indicating the type of padding algorithm to use] (default: {'same'})
        names {[type]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [A layer with avarage pool 2D with dtype tf.float32]
    """
    if names!=None:
        names = str(names)
    else:
        names = 'avg_pool_2d'

    if paddings=='Valid' or paddings=='valid' or paddings=='VALID':
        paddings = 'VALID'
    elif paddings=='Same' or paddings=='same' or paddings=='SAME':
        paddings = 'SAME'
    else:
        paddings = 'SAME'

    layer = tf.nn.avg_pool2d(value=input_tensor,ksize=kernel_sizes,strides=stride_sizes,padding=paddings,data_format='NHWC',name=names)
    return layer

def avarage_pool_3d(input_tensor, kernel_sizes=(3,3,3), stride_sizes=(1,1,1), paddings='same', names=None):
    """[summary]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer]
    
    Keyword Arguments:
        kernel_sizes {tuple} -- [Size of kernel] (default: {(3,3)})
        stride_sizes {tuple} -- [Size of striding of kernel] (default: {(1,1)})
        paddings {str} -- [Indicating the type of padding algorithm to use] (default: {'same'})
        names {[type]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [A layer with avarage pool 2D with dtype tf.float32]
    """
    if names!=None:
        names = str(names)
    else:
        names = 'avg_pool_3d'

    if paddings=='Valid' or paddings=='valid' or paddings=='VALID':
        paddings = 'VALID'
    elif paddings=='Same' or paddings=='same' or paddings=='SAME':
        paddings = 'SAME'
    else:
        paddings = 'SAME'

    layer = tf.nn.avg_pool3d(value=input_tensor,ksize=kernel_sizes,strides=stride_sizes,padding=paddings,data_format='NHWC',name=names)
    return layer

def batch_normalization(input_tensor, is_trainable=True):
    """[summary]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer]
    
    Keyword Arguments:
        is_trainable {bool} -- [State of trainable layer] (default: {True})
    
    Returns:
        [Tensor] -- [A trainable tensor]
    """
    return tf.compat.v1.keras.layers.BatchNormalization(inputs=input_tensor,training=is_trainable)

def convolution_1d(input_tensor, number_filters, kernel_sizes=3, stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=False, dropout_rates=None, names=None):
    """[summary]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer values]
        number_filters {[int]} -- [the dimensionality of the output space (i.e. the number of filters in the convolution).]
    
    Keyword Arguments:
        kernel_sizes {int} -- [Size of kernel] (default: {3})
        stride_sizes {tuple} -- [Size of striding of kernel] (default: {(1,1)})
        paddings {str} -- [Indicating the type of padding algorithm to use] (default: {'same'})
        activation {str} -- [Type of activation function in layer] (default: {'relu'})
        dropout_rates {[type]} -- [Value of dropout rate and determine to use dropout or not] (default: {None})
        names {[str]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [Layer convolution 1D with dtype tf.float32]
    """
    if names!=None:
        names = str(names)
    else:
        names = 'conv_1d'

    if paddings=='Valid' or paddings=='valid' or paddings=='VALID':
        paddings = 'VALID'
    elif paddings=='Same' or paddings=='same' or paddings=='SAME':
        paddings = 'SAME'
    else:
        paddings = 'SAME'

    weight = new_weights(shapes=[kernel_sizes, input_tensor.get_shape().as_list()[-1], number_filters], names=names, dtypes=tf.float32)

    layer = tf.nn.conv1d(value=input_tensor, filters=weight, stride=stride_sizes[0], padding=paddings, use_cudnn_on_gpu=True, data_format=None, name='conv_1d_'+names)

    if activations!=None:
        layer = define_activation_function(input_tensor=layer, activation_name=activations, names=names)
    else:
        layer = layer

    if batch_normalizations:
        layer = batch_normalization(input_tensor=layer, is_trainable=batch_normalizations)
    else:
        layer = layer

    if dropout_rates!=None:
        layer = dropout(input_tensor=layer, dropout_rates=dropout_rates, names=names)
    else:
        layer = layer
    return layer

def convolution_2d(input_tensor, number_filters, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=False, dropout_rates=None, names=None):
    """[This function creates a convolution kernel that is convolved (actually cross-correlated) with the layer input to produce a tensor of outputs]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer values]
        number_filters {[int]} -- [the dimensionality of the output space (i.e. the number of filters in the convolution).]
    
    Keyword Arguments:
        kernel_sizes {int} -- [description] (default: {(3,3)})
        stride_sizes {tuple} -- [description] (default: {(1,1)})
        paddings {str} -- [Indicating the type of padding algorithm to use] (default: {'same'})
        activation {str} -- [Type of activation function in layer] (default: {'relu'})
        dropout_layer {[float]} -- [Value of dropout rate and determine to use dropout or not] (default: {None})
        names {[str]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [Layer convolution 2D with dtype tf.float32]
    """
    if names!=None:
        names = str(names)
    else:
        names = 'conv_2d'

    if paddings=='Valid' or paddings=='valid' or paddings=='VALID':
        paddings = 'VALID'
    elif paddings=='Same' or paddings=='same' or paddings=='SAME':
        paddings = 'SAME'
    else:
        paddings = 'SAME'

    weight = new_weights(shapes=[kernel_sizes[0], kernel_sizes[1], input_tensor.get_shape().as_list()[-1], number_filters], names=names, dtypes=tf.float32)

    layer = tf.nn.conv2d(input=input_tensor, filter=weight, strides=[stride_sizes[0], stride_sizes[1]], padding=paddings, use_cudnn_on_gpu=True,
                         data_format='NHWC', dilations=[1, 1, 1, 1], name='conv_2d_'+names)

    if activations!=None:
        layer = define_activation_function(input_tensor=layer, activation_names=activations, names=names)
    else:
        layer = layer

    if batch_normalizations:
        layer = batch_normalization(input_tensor=layer, is_trainable=batch_normalizations)
    else:
        layer = layer

    if dropout_rates!=None:
        layer = dropout(input_tensor=layer, dropout_rates=dropout_rates, names=names)
    else:
        layer = layer
    return layer

def convolution_3d(input_tensor, number_filters, kernel_sizes=(3,3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=False, dropout_rates=None, names=None):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [description]
        number_filters {[type]} -- [description]
    
    Keyword Arguments:
        kernel_sizes {tuple} -- [description] (default: {(3,3,3)})
        stride_sizes {tuple} -- [description] (default: {(1,1)})
        paddings {str} -- [Indicating the type of padding algorithm to use] (default: {'same'})
        activations {str} -- [Type of activation function in layer] (default: {'relu'})
        dropout_rates {[type]} -- [Value of dropout rate and determine to use dropout or not] (default: {None})
        names {[type]} -- [Name of the layer] (default: {None})

    Returns:
        [Tensor] -- [Layer convolution 1D with dtype tf.float32]
    """    
    if names!=None:
        names = str(names)
    else:
        names = 'conv_3d'

    if paddings=='Valid' or paddings=='valid' or paddings=='VALID':
        paddings = 'VALID'
    elif paddings=='Same' or paddings=='same' or paddings=='SAME':
        paddings = 'SAME'
    else:
        paddings = 'SAME'

    weight = new_weights(shapes=[kernel_sizes[0], kernel_sizes[1], kernel_sizes[1], input_tensor.get_shape().as_list()[-1], number_filters], names=names, dtypes=tf.float32)

    layer = tf.nn.conv3d(input,filter,strides=[stride_sizes[0],stride_sizes[1],stride_sizes],padding=paddings,data_format='NDHWC',dilations=[1, 1, 1, 1, 1],name='conv_3d_'+names)
    
    if activations!=None:
        layer = define_activation_function(input_tensor=layer, activation_name=activations, names=names)
    else:
        layer = layer
    
    if batch_normalizations:
        layer = batch_normalization(input_tensor=layer, is_trainable=batch_normalizations)
    else:
        layer = layer

    if dropout_rates!=None:
        layer = dropout(input_tensor=layer, dropout_rates=dropout_rates, names=names)
    else:
        layer = layer

    return layer

def depthwise_convolution_2d(input_tensor, number_filters=1, kernel_sizes=(3,3), stride_sizes=(1,1), paddings='same', activations='relu', batch_normalizations=False, dropout_rates=None, names=None):
    """[Function for adding depthwise convolution 2D layer]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer values]
        number_filters {[int]} -- [the multiplier dimensionality of the output space (i.e. the number of filters in the convolution).]
    
    Keyword Arguments:
        kernel_size {int , int} -- [Size of kernel] (default: {(3,3)})
        stride_size {int , int} -- [Size of striding of kernel] (default: {(1,1)})
        paddings {str} -- [Indicating the type of padding algorithm to use] (default: {'same'})
        activations {str} -- [Type of activation function in layer] (default: {'relu'})
        dropout_layer {[float]} -- [Value of dropout rate and determine to use dropout or not] (default: {None})
        names {[str]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [Layer depthwise convolution 2D with dtype tf.float32]
    """
    if names!=None:
        names = str(names)
    else:
        names = 'deptwise_conv_2d'
    
    if paddings=='Valid' or paddings=='valid' or paddings=='VALID':
        paddings = 'VALID'
    elif paddings=='Same' or paddings=='same' or paddings=='SAME':
        paddings = 'SAME'
    else:
        paddings = 'SAME'

    weight = new_weights(shapes=[kernel_sizes[0], kernel_sizes[1], input_tensor.get_shape().as_list()[-1], number_filters], names=names, dtypes=tf.float32)

    layer = tf.nn.depthwise_conv2d(input=input_tensor, filter=weight, strides=[stride_sizes[0], stride_sizes[1]], padding=paddings, rate=None, name='deptwise_conv_2d_'+names, data_format=None )

    if activations!=None:
        layer = define_activation_function(input_tensor=layer, activation_name=activations, names=names)
    else:
        layer = layer

    if batch_normalizations:
        layer = batch_normalization(input_tensor=layer, is_trainable=batch_normalizations)
    else:
        layer = layer

    if dropout_rates!=None:
        layer = dropout(input_tensor=layer, dropout_rates=dropout_rates, names=names)
    else:
        layer = layer
    return layer

def max_pool_1d(input_tensor, pool_sizes=(2), stride_sizes=(1), paddings='same', names=None):
    """[summary]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer values]
    
    Keyword Arguments:
        pool_size {tuple} -- [Size of kernel] (default: {(2,2)})
        stride_sizes {tuple} -- [Size of striding of kernel] (default: {(1,1)})
        paddings {str} -- [Indicating the type of padding algorithm to use] (default: {'same'})
        names {[str]} -- [Name of the layer] (default: {None})

    Returns:
        [Tensor] -- [A layer with maxpool 1D with dtype tf.float32]
    """
    if names!=None:
        names = str(names)
    else:
        names = 'max_pool_1d'

    if paddings=='Valid' or paddings=='valid' or paddings=='VALID':
        paddings = 'VALID'
    elif paddings=='Same' or paddings=='same' or paddings=='SAME':
        paddings = 'SAME'
    else:
        paddings = 'SAME'

    layer = tf.nn.max_pool1d(input=input_tensor, ksize=pool_sizes, strides=stride_sizes, padding=paddings,name=None)
    return layer

def max_pool_2d(input_tensor, pool_sizes=(2,2), stride_sizes=(1,1), paddings='same', names=None):
    """[summary]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer values]
    
    Keyword Arguments:
        pool_size {tuple} -- [Size of kernel] (default: {(2,2)})
        stride_sizes {tuple} -- [Size of striding of kernel] (default: {(1,1)})
        paddings {str} -- [Indicating the type of padding algorithm to use] (default: {'same'})
        names {[str]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [A layer with maxpool 2D with dtype tf.float32]
    """
    if names!=None:
        names = str(names)
    else:
        names = 'max_pool_2d'

    if paddings=='Valid' or paddings=='valid' or paddings=='VALID':
        paddings = 'VALID'
    elif paddings=='Same' or paddings=='same' or paddings=='SAME':
        paddings = 'SAME'
    else:
        paddings = 'SAME'

    layer = tf.nn.max_pool2d(input=input_tensor, ksize=pool_sizes, strides=stride_sizes, padding=paddings,name=names)
    return layer

def max_pool_3d(input_tensor, pool_sizes=(2,2,2), stride_sizes=(1,1,1), paddings='same', names=None):
    """[summary]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer values]
    
    Keyword Arguments:
        pool_size {tuple} -- [Size of kernel] (default: {(2,2)})
        stride_sizes {tuple} -- [Size of striding of kernel] (default: {(1,1)})
        paddings {str} -- [Indicating the type of padding algorithm to use] (default: {'same'})
        names {[str]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [A layer with maxpool 3D with dtype tf.float32]
    """
    if names!=None:
        names = str(names)
    else:
        names = 'max_pool_3d'

    if paddings=='Valid' or paddings=='valid' or paddings=='VALID':
        paddings = 'VALID'
    elif paddings=='Same' or paddings=='same' or paddings=='SAME':
        paddings = 'SAME'
    else:
        paddings = 'SAME'

    layer = tf.nn.max_pool3d(input=input_tensor, ksize=pool_sizes, strides=stride_sizes, padding=paddings,name=None)
    return layer