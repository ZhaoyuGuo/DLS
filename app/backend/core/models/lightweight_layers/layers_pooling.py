#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ar'

from layers_basic import LW_Layer, default_dim_ordering
from layers_convolutional import conv_output_length

###############################################
class _LW_Pooling1D(LW_Layer):
    input_dim = 3
    def __init__(self, pool_length=2, stride=None, border_mode='valid'):
        if stride is None:
            stride = pool_length
        assert border_mode in {'valid', 'same'}, 'border_mode must be in {valid, same}'
        self.pool_length = pool_length
        self.stride = stride
        self.border_mode = border_mode
    def get_output_shape_for(self, input_shape):
        length = conv_output_length(input_shape[1], self.pool_length, self.border_mode, self.stride)
        return (input_shape[0], length, input_shape[2])

class LW_MaxPooling1D(_LW_Pooling1D):
    def __init__(self, pool_length=2, stride=None, border_mode='valid'):
        super(LW_MaxPooling1D, self).__init__(pool_length, stride, border_mode)

class LW_AveragePooling1D(_LW_Pooling1D):
    def __init__(self, pool_length=2, stride=None, border_mode='valid'):
        super(LW_AveragePooling1D, self).__init__(pool_length, stride, border_mode)

###############################################
class _LW_Pooling2D(LW_Layer):
    def __init__(self, pool_size=(2, 2), strides=None, border_mode='valid', dim_ordering='default'):
        if dim_ordering == 'default':
            dim_ordering = default_dim_ordering
        assert dim_ordering in {'tf', 'th'}, 'dim_ordering must be in {tf, th}'
        self.pool_size = tuple(pool_size)
        if strides is None:
            strides = self.pool_size
        self.strides = tuple(strides)
        assert border_mode in {'valid', 'same'}, 'border_mode must be in {valid, same}'
        self.border_mode = border_mode
        self.dim_ordering = dim_ordering
    def get_output_shape_for(self, input_shape):
        if self.dim_ordering == 'th':
            rows = input_shape[2]
            cols = input_shape[3]
        elif self.dim_ordering == 'tf':
            rows = input_shape[1]
            cols = input_shape[2]
        else:
            raise Exception('Invalid dim_ordering: ' + self.dim_ordering)
        rows = conv_output_length(rows, self.pool_size[0], self.border_mode, self.strides[0])
        cols = conv_output_length(cols, self.pool_size[1], self.border_mode, self.strides[1])
        if self.dim_ordering == 'th':
            return (input_shape[0], input_shape[1], rows, cols)
        elif self.dim_ordering == 'tf':
            return (input_shape[0], rows, cols, input_shape[3])
        else:
            raise Exception('Invalid dim_ordering: ' + self.dim_ordering)

class LW_MaxPooling2D(_LW_Pooling2D):
    def __init__(self, pool_size=(2, 2), strides=None, border_mode='valid', dim_ordering='default'):
        super(LW_MaxPooling2D, self).__init__(pool_size, strides, border_mode, dim_ordering)

class LW_AveragePooling2D(_LW_Pooling2D):
    def __init__(self, pool_size=(2, 2), strides=None, border_mode='valid', dim_ordering='default'):
        super(LW_AveragePooling2D, self).__init__(pool_size, strides, border_mode, dim_ordering)

###############################################
class _LW_Pooling3D(LW_Layer):
    def __init__(self, pool_size=(2, 2, 2), strides=None, border_mode='valid', dim_ordering='default'):
        if dim_ordering == 'default':
            dim_ordering = default_dim_ordering
        assert dim_ordering in {'tf', 'th'}, 'dim_ordering must be in {tf, th}'
        self.pool_size = tuple(pool_size)
        if strides is None:
            strides = self.pool_size
        self.strides = tuple(strides)
        assert border_mode in {'valid', 'same'}, 'border_mode must be in {valid, same}'
        self.border_mode = border_mode
        self.dim_ordering = dim_ordering
    def get_output_shape_for(self, input_shape):
        if self.dim_ordering == 'th':
            len_dim1 = input_shape[2]
            len_dim2 = input_shape[3]
            len_dim3 = input_shape[4]
        elif self.dim_ordering == 'tf':
            len_dim1 = input_shape[1]
            len_dim2 = input_shape[2]
            len_dim3 = input_shape[3]
        else:
            raise Exception('Invalid dim_ordering: ' + self.dim_ordering)
        len_dim1 = conv_output_length(len_dim1, self.pool_size[0], self.border_mode, self.strides[0])
        len_dim2 = conv_output_length(len_dim2, self.pool_size[1], self.border_mode, self.strides[1])
        len_dim3 = conv_output_length(len_dim3, self.pool_size[2], self.border_mode, self.strides[2])
        if self.dim_ordering == 'th':
            return (input_shape[0], input_shape[1], len_dim1, len_dim2, len_dim3)
        elif self.dim_ordering == 'tf':
            return (input_shape[0], len_dim1, len_dim2, len_dim3, input_shape[4])
        else:
            raise Exception('Invalid dim_ordering: ' + self.dim_ordering)

class LW_MaxPooling3D(_LW_Pooling3D):
    def __init__(self, pool_size=(2, 2, 2), strides=None, border_mode='valid', dim_ordering='default'):
        super(LW_MaxPooling3D, self).__init__(pool_size, strides, border_mode, dim_ordering)

class LW_AveragePooling3D(_LW_Pooling3D):
    def __init__(self, pool_size=(2, 2, 2), strides=None, border_mode='valid', dim_ordering='default'):
        super(LW_AveragePooling3D, self).__init__(pool_size, strides, border_mode, dim_ordering)

###############################################
class _LW_GlobalPooling1D(LW_Layer):
    def __init__(self):
        pass
    def get_output_shape_for(self, input_shape):
        return (input_shape[0], input_shape[2])

class LW_GlobalAveragePooling1D(_LW_GlobalPooling1D):
    pass

class LW_GlobalMaxPooling1D(_LW_GlobalPooling1D):
    pass

###############################################
class _LW_GlobalPooling2D(LW_Layer):

    def __init__(self, dim_ordering='default'):
        if dim_ordering == 'default':
            dim_ordering = default_dim_ordering
        self.dim_ordering = dim_ordering
    def get_output_shape_for(self, input_shape):
        if self.dim_ordering == 'tf':
            return (input_shape[0], input_shape[3])
        else:
            return (input_shape[0], input_shape[1])

class LW_GlobalAveragePooling2D(_LW_GlobalPooling2D):
    pass

class LW_GlobalMaxPooling2D(_LW_GlobalPooling2D):
    pass

###############################################
class _LW_GlobalPooling3D(LW_Layer):
    def __init__(self, dim_ordering='default'):
        if dim_ordering == 'default':
            dim_ordering = default_dim_ordering
        self.dim_ordering = dim_ordering
    def get_output_shape_for(self, input_shape):
        if self.dim_ordering == 'tf':
            return (input_shape[0], input_shape[4])
        else:
            return (input_shape[0], input_shape[1])

class LW_GlobalAveragePooling3D(_LW_GlobalPooling3D):
    pass

class LW_GlobalMaxPooling3D(_LW_GlobalPooling3D):
    pass

###############################################
if __name__ == '__main__':
    pass