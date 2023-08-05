import tensorflow as tf

def crelu(input_tensor, names=None):
    """[Concatenates a ReLU which selects only the positive part of the activation
        with a ReLU which selects only the negative part of the activation 
        Source: https://arxiv.org/abs/1603.05201]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing preactivation values]
        name {[str]} -- [A name for the operation (optional)]  (default: {None})
    
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with activation crelu]
    """
    return tf.nn.crelu(features=input_tensor,name='activation_crelu_'+names,axis=-1)

def define_activation_function(input_tensor, activation_names, names=None):
    """[Determine the type of activation function]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing preactivation values]
        activation_names {[str]} -- [Type of activation function]
    
    Keyword Arguments:
        names {[str]} -- [A name for the operation (optional)] (default: {None})
        
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with spesific activation function]
    """
    if activation_names=="crelu":
        output_tensor = tf.nn.crelu(features=input_tensor, name='activation_'+names, axis=-1)
    elif activation_names=="elu":
        output_tensor = tf.nn.elu(features=input_tensor, name='activation_'+names)
    elif activation_names=="leakyRelu":
        alpha=tf.constant(0.2, dtype=tf.float32)
        output_tensor = tf.nn.leaky_relu(features=input_tensor, alpha=alpha, name='activation_'+names)
    elif activation_names=="relu":
        output_tensor = tf.nn.relu(features=input_tensor, name='activation_'+names)
    elif activation_names=="relu6":
        output_tensor = tf.nn.relu6(features=input_tensor, name='activation_'+names)
    elif activation_names=="selu":
        output_tensor = tf.nn.selu(features=input_tensor, name='activation_'+names)
    elif activation_names=="sigmoid":
        output_tensor = tf.nn.sigmoid(x=input_tensor, name='activation_'+names)
    elif activation_names=="softmax":
        output_tensor = tf.nn.softmax(logits=input_tensor, axis=None, name='activation_'+names, dim=None)
    elif activation_names=="softsign":
        output_tensor = tf.nn.softsign(features=input_tensor, name='activation_'+names)
    elif activation_names=="tanh":
        output_tensor = tf.nn.tanh(x=input_tensor, name='activation_'+names)
    elif activation_names==None:
        output_tensor = input_tensor
    return output_tensor

def elu(input_tensor, names=None):
    """[Computes exponential linear: exp(features) - 1 if < 0, features otherwise
        Source: https://arxiv.org/abs/1511.07289]
    
    Arguments:
        input_tensor {[half, bfloat16, float32, float64]} -- [A Tensor representing preactivation values]
        name {[str]} -- [A name for the operation (optional)]  (default: {None})
    
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with activation elu]
    """
    return tf.nn.elu(features=input_tensor,name='activation_elu_'+names)

def leaky_relu(input_tensor, names=None, alpha=0.2):
    """[Compute the Leaky ReLU activation function
        Source: https://ai.stanford.edu/~amaas/papers/relu_hybrid_icml2013_final.pdf]
    
    Arguments:
        input_tensor {[float16, float32, float64, int32, int64]} -- [A Tensor representing preactivation values]
        name {[str]} -- [A name for the operation (optional)] (default: {None})
    
    Keyword Arguments:
        alpha {float} -- [Slope of the activation function at x < 0] (default: {0.2})
    
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with activation leaky relu]
    """
    return tf.nn.leaky_relu(features=input_tensor,alpha=alpha,name='activation_lrelu_'+names)

def relu(input_tensor, names=None):
    """[Computes rectified linear: max(features, 0)]
    
    Arguments:
        input_tensor {[float32, float64, int32, uint8, int16, int8, int64, bfloat16, uint16, half, uint32, uint64, qint8]} 
                        -- [A Tensor representing preactivation values]
    
    Keyword Arguments:
        name {[str]} -- [A name for the operation (optional)] (default: {None})
    
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with activation relu]
    """
    return tf.nn.relu(features=input_tensor,name='activation_relu_'+names)

def relu6(input_tensor, names=None):
    """[Computes Rectified Linear 6: min(max(features, 0), 6)
        Source: http://www.cs.utoronto.ca/~kriz/conv-cifar10-aug2010.pdf]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8} -- [A Tensor representing preactivation values]
    
    Keyword Arguments:
        name {[str]} -- [A name for the operation (optional)] (default: {None})
    
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with activation relu6]
    """
    return tf.nn.relu6(features=input_tensor,name='activation_relu6_'+names)

def selu(input_tensor, names=None):
    """[Computes scaled exponential linear: scale * alpha * (exp(features) - 1)
        if < 0, scale * features otherwise]
    
    Arguments:
        input_tensor {[half, bfloat16, float32, float64]} -- [A Tensor representing preactivation values]
    
    Keyword Arguments:
        name {[str]} -- [A name for the operation (optional)] (default: {None})
    
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with activation selu]
    """
    return tf.nn.selu(features=input_tensor,name='activation_selu_'+names)

def sigmoid(input_tensor , names=None):
    """[Computes sigmoid of x element-wise.
        Specifically, y = 1 / (1 + exp(-x))]
    
    Arguments:
        input_tensor {[float16, float32, float64, complex64, or complex128]} -- [A Tensor representing preactivation values]
    
    Keyword Arguments:
        name {[str]} -- [A name for the operation (optional)] (default: {None})
    
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with activation sigmoid]
    """
    return tf.nn.sigmoid(x=input_tensor,name='activation_sigmoid_'+names)

def softmax(input_tensor, names=None, axis=None):
    """[Computes softmax activations]
    
    Arguments:
        input_tensor {[half, float32, float64]} -- [A Tensor representing preactivation values]
    
    Keyword Arguments:
        axis {[int]} -- [The dimension softmax would be performed on. The default is -1 which indicates the last dimension.] (default: {None})
        name {[str]} -- [A name for the operation (optional)] (default: {None})
        dim {[int]} -- [Deprecated alias for axis] (default: {None})
    
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with activation softmax]
    """
    return tf.nn.softmax(logits=input_tensor,axis=axis,name='activation_softmax_'+names)

def softsign(input_tensor, names=None):
    """[Computes softsign: features / (abs(features) + 1).]
    
    Arguments:
        input_tensor {[half, bfloat16, float32, float64]} -- [A Tensor representing preactivation values]
    
    Keyword Arguments:
        name {[str]} -- [A name for the operation (optional)] (default: {None})
    
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with activation softsign]
    """
    return tf.nn.softsign(features=input_tensor,name='activation_softsign_'+names)

def tanh(input_tensor, names=None):
    """[Computes hyperbolic tangent of x element-wise]
    
    Arguments:
        input_tensor {[bfloat16, half, float32, float64, complex64]} -- [A Tensor representing preactivation values]
    
    Keyword Arguments:
        name {[str]} -- [A name for the operation (optional)] (default: {None})
    
    Returns:
        [Tensor] -- [A tensor dtype tf.float32 with activation tanh]
    """
    return tf.nn.tanh(x=input_tensor,name='activation_tanh_'+names)