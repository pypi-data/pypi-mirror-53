import tensorflow as tf
from poda.layers.activation import *
from poda.layers.regularizer import *

def dense(input_tensor, hidden_units, names=None, activations=None, regularizers=None, scale=0.2, bias_initializers='ZERO'):
    """[Create a new trainable Fully Connected layer]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer]
        hidden_units {[int]} -- [description]
        names {[str]} -- [Name of the layer] (default: {None})
    
    Keyword Arguments:
        activation {str} -- [description] (default: {'relu'})
        regularizers {[type]} -- [description] (default: {None})
        scale {float} -- [description] (default: {0.2})
    
    Returns:
        [Tensor] -- [A trainable tensor]
    """
    if names!=None:
        name = str(names)
    else:
        name = 'dense'

    weight = new_weights(shapes=[input_tensor.get_shape().as_list()[1], hidden_units], names=name)

    bias = new_biases(shapes=[input_tensor.get_shape().as_list()[0], hidden_units], names=name, bias_initializers=bias_initializers)

    layer = tf.matmul(input_tensor, weight)
    layer += bias

    if activations!=None:
        layer = define_activation_function(input_tensor=layer, activation_names=activations, names=name)
    else:
        layer = layer

    if regularizers=='both':
        layer = dropout(input_tensor=layer, dropout_rates=scale, names=name)
        layer = l2_regularization(input_tensor=layer, names=name)
    elif regularizers=='l1':
        layer = l1_regularization(input_tensor=layer)
    elif regularizers=='l2':
        layer = l2_regularization(input_tensor=layer)
    elif regularizers=='dropout':
        layer = dropout(input_tensor=layer, dropout_rates=scale, names=name)
    else:
        layer = layer

    return layer

def new_weights(shapes, names, random_types='truncated_normal', dtypes=tf.float32):
    """[Create a new trainable tensor as weight]
    
    Arguments:
        shapes {[Array of int]} -- [- example (convolution), [filter height, filter width, input channels, output channels]
                                    - example (fully connected), [num input, num output]]
        names {[str]} -- [A name for the operation (optional)]
    
    Keyword Arguments:
        random_types {str} -- [Type of random values] (default: {'truncated_normal'})
        dtypes {[float32]} -- [Data type of tensor] (default: {tf.float32})
    
    Returns:
        [float32] -- [A trainable tensor]
    """
    if random_types=='random_normal':
        initial_weight = tf.random.normal(shape=shapes,mean=0.0,stddev=1.0,dtype=dtypes,seed=None)
    elif random_types=='random_uniform':
        initial_weight = tf.random.uniform(shape=shapes,minval=0,maxval=None,dtype=dtypes,seed=None)
    else:
        initial_weight = tf.random.truncated_normal(shape=shapes,mean=0.0,stddev=1.0,dtype=dtypes,seed=None)
    return tf.Variable(initial_weight, dtype=dtypes, name='weight_'+names)

def new_biases(shapes, names, bias_initializers='NOTZERO', dtypes=tf.float32):
    """[Create a new trainable tensor as bias]
    
    Arguments:
        shapes {[int]} -- [Length of filter or node ]
        names {[str]} -- [A name for the operation (optional)]
    
    Keyword Arguments:
        dtypes {[float32]} -- [Data type of tensor] (default: {tf.float32})
    
    Returns:
        [float32] -- [A trainable tensor]
    """
    if bias_initializers=='ZERO':
        initial_bias = tf.zeros(shape=shapes, dtype=dtypes, name=names)
    else:
        initial_bias = tf.constant(0.05, shape=shapes, dtype=dtypes)

    return tf.Variable(initial_bias, dtype=dtypes, name='bias_'+names)
