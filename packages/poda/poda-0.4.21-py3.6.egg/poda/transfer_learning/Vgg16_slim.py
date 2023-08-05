# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Contains model definitions for versions of the Oxford VGG network.
These model definitions were introduced in the following technical report:
  Very Deep Convolutional Networks For Large-Scale Image Recognition
  Karen Simonyan and Andrew Zisserman
  arXiv technical report, 2015
  PDF: http://arxiv.org/pdf/1409.1556.pdf
  ILSVRC 2014 Slides: http://www.robots.ox.ac.uk/~karen/pdf/ILSVRC_2014.pdf
  CC-BY-4.0
More information can be obtained from the VGG website:
www.robots.ox.ac.uk/~vgg/research/very_deep/
Usage:
  with slim.arg_scope(vgg.vgg_arg_scope()):
    outputs, end_points = vgg.vgg_a(inputs)
  with slim.arg_scope(vgg.vgg_arg_scope()):
    outputs, end_points = vgg.vgg_16(inputs)
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from poda.layers.dense import *
from poda.layers.merge import *
from poda.layers.activation import *
from poda.layers.convolutional import *
from poda.utils import *
slim = tf.contrib.slim

def build_base_layer_model(input_tensor,num_blocks=5,scope='vgg_16'):
    with tf.compat.v1.variable_scope(scope, 'vgg_16', [input_tensor]) as sc:
        end_points_collection = sc.original_name_scope + '_end_points'
        # Collect outputs for conv2d, fully_connected and max_pool2d.
        with slim.arg_scope([slim.conv2d, slim.fully_connected, slim.max_pool2d],outputs_collections=end_points_collection):
            net = slim.repeat(input_tensor, 2, slim.conv2d, 64, [3, 3], scope='conv1')
            block_1 = slim.max_pool2d(net, [2, 2], scope='pool1')
            net = slim.repeat(block_1, 2, slim.conv2d, 128, [3, 3], scope='conv2')
            block_2 = slim.max_pool2d(net, [2, 2], scope='pool2')
            net = slim.repeat(block_2, 3, slim.conv2d, 256, [3, 3], scope='conv3')
            block_3 = slim.max_pool2d(net, [2, 2], scope='pool3')
            net = slim.repeat(block_3, 3, slim.conv2d, 512, [3, 3], scope='conv4')
            block_4 = slim.max_pool2d(net, [2, 2], scope='pool4')
            net = slim.repeat(block_4, 3, slim.conv2d, 512, [3, 3], scope='conv5')
            block_5 = slim.max_pool2d(net, [2, 2], scope='pool5')

            if num_blocks==1:
                net = block_1
            elif num_blocks==2:
                net = block_2
            elif num_blocks==3:
                net = block_3
            elif num_blocks==4:
                net = block_4
            elif num_blocks==5:
                net = block_5
            return net
            
def build_top_layer_model(base_layer,num_depthwise_layer=None,
                          num_fully_connected_layer=1,num_hidden_unit=512,
                          activation_fully_connected='relu',dropout_keep_prob=None,regularizers=None,num_classes=1000):
    previous_layer = base_layer
    if num_depthwise_layer!=None:
        num_depthwise_layer = num_depthwise_layer * 3
        for i in range(num_depthwise_layer):
            depth_wise_net = depthwise_convolution_2d(input_tensor=previous_layer,number_filters=1, 
                                                      kernel_sizes=(3,3), stride_sizes=(2,2), paddings='same',
                                                      activations='relu',names=str(i))
            previous_layer = depth_wise_net

    flatten_layer = flatten(input_tensor=previous_layer)

    if num_fully_connected_layer !=None:
        for j in range(num_fully_connected_layer):
            fully_connected_net = dense(input_tensor=flatten_layer,hidden_units=num_hidden_unit,
                                                  activations=activation_fully_connected,regularizers=regularizers,
                                                  scale=dropout_keep_prob,names=str(j))
            flatten_layer = fully_connected_net
    else:
        flatten_layer = flatten_layer

    non_logit = dense(input_tensor=flatten_layer,hidden_units=num_classes,activations=None)
    if num_classes > 2:
        output = softmax(input_tensor=non_logit, names='output')
    else:
        output = sigmoid(input_tensor=non_logit, names='output')
    return non_logit, output
    
def vgg16(input_tensor,num_classes=1000,num_blocks=5,num_depthwise_layer=None,num_fully_connected_layer=1,num_hidden_unit=512,activation_fully_connected=None,regularizers=None):
    net = build_base_layer_model(input_tensor=input_tensor,num_blocks=num_blocks)
    base_var_list = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)
    non_logit , output = build_top_layer_model(net,num_depthwise_layer=num_depthwise_layer,num_fully_connected_layer=num_fully_connected_layer,num_hidden_unit=num_hidden_unit,
                                               activation_fully_connected=activation_fully_connected,regularizers=regularizers,num_classes=num_classes)

    full_var_list = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)

    return non_logit , output , base_var_list , full_var_list

def vgg_arg_scope(self,weight_decay=0.0005):
    with slim.arg_scope([slim.conv2d, slim.fully_connected],
                            activation_fn=tf.nn.relu,
                            weights_regularizer=slim.l2_regularizer(weight_decay),
                            biases_initializer=tf.zeros_initializer()):
        with slim.arg_scope([slim.conv2d], padding='SAME') as arg_sc:
            return arg_sc