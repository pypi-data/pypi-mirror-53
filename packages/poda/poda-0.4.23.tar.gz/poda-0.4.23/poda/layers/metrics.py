import tensorflow as tf 
import numpy as np

def calculate_accuracy_classification(input_tensor, label, threshold=0.5):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [description]
        label {[type]} -- [description]
    
    Keyword Arguments:
        threshold {float} -- [description] (default: {0.5})
    """
    matches = tf.equal(tf.argmax(input_tensor, 1), tf.argmax(label, 1))
    accuracy = tf.reduce_mean(tf.cast(matches, tf.float32))
    return accuracy

def calculate_accuracy_mask(input_tensor, label, threshold=0.5):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [A Tensor representing output graph]
        label {[type]} -- [A Tensor representing real target]
    
    Keyword Arguments:
        threshold {float} -- [description] (default: {0.5})
    
    Returns:
        [Scalar] -- [Accuracy between output graph and real target]
    """
    mask = tf.fill(tf.shape(label), 1.)
    input_tensor = tf.reshape(input_tensor, [tf.shape(input_tensor)[0], -1])
    label = tf.reshape(label, [tf.shape(label)[0], -1])

    input_tensor = tf.math.greater(input_tensor, tf.convert_to_tensor(np.array(threshold), tf.float32))
    input_tensor = tf.cast(input_tensor, tf.float32)
    label = tf.math.greater(label, tf.convert_to_tensor(np.array(threshold), tf.float32))
    label = tf.cast(label, tf.float32)

    error = tf.reduce_sum(tf.abs(input_tensor - label)) / (tf.reduce_sum(mask) + 0.0001)
    acc = 1. - error
    return acc

def calculate_loss(input_tensor, label, type_loss_function='sigmoid_crossentropy_mean', penalize_class=0, names=None):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [description]
        label {[type]} -- [description]
    
    Keyword Arguments:
        penalize_class {int} -- [description] (default: {0})
    """
    if names!=None:
        names = str(names)
    else:
        names= 'loss'

    if type_loss_function == 'mse_loss_mean':
        loss = tf.compat.v1.losses.mean_squared_error(labels=label, predictions=input_tensor)
        loss = tf.reduce_mean(loss)
    elif type_loss_function == 'mse_loss_sum':
        loss = tf.compat.v1.losses.mean_squared_error(labels=label, predictions=input_tensor)
        loss = tf.reduce_sum(loss)
    elif type_loss_function == 'softmax_crosentropy_mean':
        loss = tf.compat.v2.nn.softmax_cross_entropy_with_logits(labels=label, logits=input_tensor, name=names)
        loss = tf.reduce_mean(loss)
    elif type_loss_function == 'softmax_crosentropy_sum':
        loss = tf.compat.v2.nn.softmax_cross_entropy_with_logits(labels=label, logits=input_tensor, name=names)
        loss = tf.reduce_sum(loss)
    elif type_loss_function == 'sigmoid_crossentropy_mean':
        loss = tf.compat.v2.nn.sigmoid_cross_entropy_with_logits(labels=label, logits=input_tensor, name=names)
        loss = tf.reduce_mean(loss)
    elif type_loss_function == 'sigmoid_crossentropy_sum':
        loss = tf.compat.v2.nn.sigmoid_cross_entropy_with_logits(labels=label, logits=input_tensor, name=names)
        loss = tf.reduce_sum(loss)
    else:
        loss = tf.compat.v2.nn.sigmoid_cross_entropy_with_logits(labels=label, logits=input_tensor, name=names)
        loss = tf.reduce_mean(loss)
    return loss

def mse_mean(input_tensor, label, names=None):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [A Tensor representing output graph]
        label {[type]} -- [A Tensor representing real target]
    
    Keyword Arguments:
        names {[type]} -- [Name for metrics function] (default: {None})
    
    Returns:
        [Scalar] -- [Loss of Value between output graph and real target]
    """
    if names!=None:
        names = str(names)
    else:
        names= 'mse_mean_loss'

    loss = tf.compat.v1.losses.mean_squared_error(labels=label, predictions=input_tensor)
    loss = tf.reduce_mean(loss)
    return loss


def mse_sum(input_tensor, label, names=None):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [A Tensor representing output graph]
        label {[type]} -- [A Tensor representing real target]
    
    Keyword Arguments:
        names {[type]} -- [Name for metrics function] (default: {None})
    
    Returns:
        [Scalar] -- [Loss of Value between output graph and real target]
    """
    if names!=None:
        names = str(names)
    else:
        names= 'mse_sum_loss'

    loss = tf.compat.v1.losses.mean_squared_error(labels=label, predictions=input_tensor)
    loss = tf.reduce_sum(loss)
    return loss


def softmax_crosentropy_mean(input_tensor, label, names=None):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [A Tensor representing output graph]
        label {[type]} -- [A Tensor representing real target]
    
    Keyword Arguments:
        names {[type]} -- [Name for metrics function] (default: {None})
    
    Returns:
        [Scalar] -- [Loss of Value between output graph and real target]
    """
    if names!=None:
        names = str(names)
    else:
        names= 'softmax_crossentropy_mean_loss'

    loss = tf.compat.v2.nn.softmax_cross_entropy_with_logits(labels=label, logits=input_tensor, name=names)
    loss = tf.reduce_mean(loss)
    return loss


def softmax_crosentropy_sum(input_tensor, label, names=None):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [A Tensor representing output graph]
        label {[type]} -- [A Tensor representing real target]
    
    Keyword Arguments:
        names {[type]} -- [Name for metrics function] (default: {None})
    
    Returns:
        [Scalar] -- [Loss of Value between output graph and real target]
    """
    if names!=None:
        names = str(names)
    else:
        names= 'softmax_crossentropy_sum_loss'

    loss = tf.compat.v2.nn.softmax_cross_entropy_with_logits(labels=label, logits=input_tensor, name=names)
    loss = tf.reduce_sum(loss)
    return loss


def sigmoid_crossentropy_mean(input_tensor, label, names=None):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [A Tensor representing output graph]
        label {[type]} -- [A Tensor representing real target]
    
    Keyword Arguments:
        names {[type]} -- [Name for metrics function] (default: {None})
    
    Returns:
        [Scalar] -- [Loss of Value between output graph and real target]
    """
    if names!=None:
        names = str(names)
    else:
        names= 'sigmoid_crossentropy_mean_loss'

    loss = tf.compat.v2.nn.sigmoid_cross_entropy_with_logits(labels=label, logits=input_tensor, name=names)
    loss = tf.reduce_mean(loss)
    return loss


def sigmoid_crossentropy_sum(input_tensor, label, names=None):
    """[summary]
    
    Arguments:
        input_tensor {[type]} -- [A Tensor representing output graph]
        label {[type]} -- [A Tensor representing real target]
    
    Keyword Arguments:
        names {[type]} -- [Name for metrics function] (default: {None})
    
    Returns:
        [Scalar] -- [Loss of Value between output graph and real target]
    """
    if names!=None:
        names = str(names)
    else:
        names= 'sigmoid_crossentropy_sum_loss'

    loss = tf.compat.v2.nn.sigmoid_cross_entropy_with_logits(labels=label, logits=input_tensor, name=names)
    loss = tf.reduce_sum(loss)
    return loss