import tensorflow as tf

def dropout(input_tensor, names, dropout_rates=None):
    """[Create a dropout function in a layer]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing preactivation values]
    
    Keyword Arguments:
        dropout_rate {float} -- [Rate for dropout node] (default: {0.2})
        name {[str]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [A layer with dropout and dtype tf.float32]
    """
    if names!=None:
        names = str(names)
    else:
        names = ''

    if dropout_rates==None:
        dropout_rates = 0.2

    return tf.nn.dropout(x=input_tensor, rate=dropout_rates, noise_shape=None,
                            seed=None,
                            name='dropout_'+names)

def l1_regularization(input_tensor, scope):
    """[Create a l1 regularization in a layer]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing preactivation values]
    
    Returns:
        [Tensor] -- [A layer with regularizer l1 and dtype tf.float32]
    """
    return tf.contrib.layers.l1_regularizer(scale=input_tensor,scope=None)

def l2_regularization(input_tensor, scope):
    """[Create a l2 regularization in a layer]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing preactivation values]

    Returns:
        [Tensor] -- [A layer with regularizer l2 and dtype tf.float32]
    """
    return tf.contrib.layers.l2_regularizer(scale=input_tensor,scope=None)