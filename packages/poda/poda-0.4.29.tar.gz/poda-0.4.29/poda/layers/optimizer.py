import tensorflow as tf

def adadelta(learning_rates=0.0001, rho=0.95, epsilon=1e-08, use_lockings=False, names=None):
    """[summary]
    
    Keyword Arguments:
        learning_rates {float} -- [Value of learning rate] (default: {0.0001})
        rho {float} -- [Value of learning rho] (default: {0.999})
        epsilons {[type]} -- [Value of learning epsilons] (default: {1e-08})
        use_lockings {bool} -- [State of locking] (default: {False})
        names {[type]} -- [Name of the optimizer] (default: {None})

    Returns:
        [Optimizer] -- [Optimizer for training graph]
    """
    if names!=None:
        names = str(names)
    else:
        names= ''
    
    optimizer = tf.compat.v1.train.AdadeltaOptimizer(learning_rate=learning_rates,rho=rho,epsilon=epsilon,use_locking=use_lockings,name=names)
    return optimizer

def adagrad(learning_rates=0.0001, initial_accumulator_value=0.1, use_lockings=False, names=None):
    """[summary]
    
    Keyword Arguments:
        learning_rates {float} -- [Value of learning rate] (default: {0.0001})
        initial_accumulator_value {float} -- [Value of learning rho] (default: {0.999})
        use_lockings {bool} -- [State of locking] (default: {False})
        names {[type]} -- [Name of the optimizer] (default: {None})

    Returns:
        [Optimizer] -- [Optimizer for training graph]
    """
    if names!=None:
        names = str(names)
    else:
        names= ''
    
    optimizer = tf.compat.v1.train.AdagradOptimizer(learning_rate=learning_rates,initial_accumulator_value=initial_accumulator_value,use_locking=use_lockings,name=names)
    return optimizer

def adam(learning_rates=0.0001, beta1=0.9, beta2=0.999, epsilon=1e-08, use_lockings=False, names=None):
    """[summary]
    
    Keyword Arguments:
        learning_rates {float} -- [Value of learning rate] (default: {0.0001})
        beta1 {float} -- [Value of learning beta1] (default: {0.9})
        beta2 {float} -- [Value of learning beta2] (default: {0.999})
        epsilons {[type]} -- [Value of learning epsilons] (default: {1e-08})
        use_lockings {bool} -- [State of locking] (default: {False})
        names {[type]} -- [Name of the optimizer] (default: {None})

    Returns:
        [Optimizer] -- [Optimizer for training graph]
    """
    if names!=None:
        names = str(names)
    else:
        names= ''

    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rates,beta1=beta1,beta2=beta2,epsilon=epsilon,use_locking=use_lockings,name=names)
    return optimizer

def optimizers(optimizers_names='adam', learning_rates=0.0001):
    """[summary]
    
    Keyword Arguments:
        optimizers_names {str} -- [Type of optimizer] (default: {'adam'})
        learning_rates {float} -- [Value of learning rate] (default: {0.0001})
    
    Returns:
        [Optimizer] -- [Optimizer for training graph]
    """
    optimizers_function = None
    if optimizers_names=='adam':
        optimizers_function = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rates,beta1=0.9,beta2=0.999,epsilon=1e-08,use_locking=False,name='Adam')
    elif optimizers_names=='adadelta':
        optimizers_function = tf.compat.v1.train.AdadeltaOptimizer(learning_rate=learning_rates,rho=0.95,epsilon=1e-08,use_locking=False,name='Adadelta')
    elif optimizers_names=='adagrad':
        optimizers_function = tf.compat.v1.train.AdagradOptimizer(learning_rate=learning_rates,initial_accumulator_value=0.1,use_locking=False,name='Adagrad')
    elif optimizers_names=='sgd':
        optimizers_function = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=learning_rates,use_locking=False,name='GradientDescent')
    elif optimizers_names=='rmsprop':
        optimizers_function = tf.compat.v1.train.RMSPropOptimizer(learning_rate=learning_rates,decay=0.9,momentum=0.0,epsilon=1e-10,use_locking=False,centered=False,name='RMSProp')
    return optimizers_function

def rmsprop(learning_rates=0.0001, decay=0.9, momentum=0.0, epsilon=1e-10, use_lockings=False, centered=False, names=None):
    """[summary]
    
    Keyword Arguments:
        learning_rates {float} -- [Value of learning rate] (default: {0.0001})
        rho {float} -- [Value of learning rho] (default: {0.999})
        epsilons {[type]} -- [Value of learning epsilons] (default: {1e-08})
        use_lockings {bool} -- [State of locking] (default: {False})
        names {[type]} -- [Name of the optimizer] (default: {None})

    Returns:
        [Optimizer] -- [Optimizer for training graph]
    """
    if names!=None:
        names = str(names)
    else:
        names= ''
    
    optimizer = tf.compat.v1.train.RMSPropOptimizer(learning_rate=learning_rates,decay=decay,momentum=momentum,epsilon=epsilon,use_locking=use_lockings,centered=centered,name=names)
    return optimizer

def sgd(learning_rates=0.0001, use_lockings=False, names=None):
    """[summary]
    
    Keyword Arguments:
        learning_rates {float} -- [Value of learning rate] (default: {0.0001})
        use_lockings {bool} -- [State of locking] (default: {False})
        names {[type]} -- [Name of the optimizer] (default: {None})

    Returns:
        [Optimizer] -- [Optimizer for training graph]
    """
    if names!=None:
        names = str(names)
    else:
        names= ''

    optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=learning_rates,use_locking=use_lockings,name=names)
    return optimizer