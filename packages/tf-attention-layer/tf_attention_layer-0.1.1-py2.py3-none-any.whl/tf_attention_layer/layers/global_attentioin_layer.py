import tensorflow as tf
from tensorflow.python.keras.layers import Layer

from tf_attention_layer import keras_utils


@keras_utils.register_keras_custom_object
class GlobalAttentionLayer(Layer):
    def __init__(self, **kwargs):
        # variables will be assigned later
        self.weight_one = None
        self.weight_two = None
        self.adopter_weight = None

        super().__init__(**kwargs)

        # setup mask supporting flag, used by base class (the Layer)
        # Note: this call must be behind the call of base class's __init__,
        # because base class set supports_masking to false unconditionally
        self.supports_masking = True

    def get_config(self):
        config = {}

        base_config = super(GlobalAttentionLayer, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def compute_output_shape(self, input_shape):
        input_shape_plain = tuple(tf.TensorShape(input_shape).as_list())
        output_shape = tf.TensorShape(
            input_shape_plain[:2] + (input_shape_plain[-1] * 2,)
        )
        return output_shape

    def build(self, input_shape):
        if isinstance(input_shape, list):
            input_shape = input_shape[0]

        input_shape = tuple(tf.TensorShape(input_shape).as_list())

        # start variables for score function

        self.weight_one = self.add_weight(shape=input_shape[-2:], name="weight_one")

        self.weight_two = self.add_weight(shape=input_shape[-2:], name="weight_two")

        self.adopter_weight = self.add_weight(
            shape=input_shape[-1:], name="adopter_weight"
        )

        # end variables for score function

        # or directly call self.built = True
        super(GlobalAttentionLayer, self).build(input_shape)

    def call(self, inputs, mask=None, **kwargs):
        # TODO: use mask

        if isinstance(inputs, list):
            inputs = inputs[0]

        # start score function

        var_one = inputs * self.weight_one
        var_two = inputs * self.weight_two

        var_one = tf.expand_dims(var_one, 2)

        var_two = tf.expand_dims(var_two, 1)

        var_sum = var_one + var_two

        tanh_sum = tf.tanh(var_sum)

        weight_matrix = tf.tensordot(tanh_sum, self.adopter_weight, [3, 0])

        # end score function

        exp_weight_matrix = tf.exp(weight_matrix)

        exp_weight_sum = tf.reduce_sum(exp_weight_matrix, 2, keepdims=True)

        normed_weight = exp_weight_matrix / exp_weight_sum

        weighted_var_matrix = tf.expand_dims(normed_weight, -1) * tf.expand_dims(
            inputs, 1
        )

        weighted_var = tf.reduce_sum(weighted_var_matrix, 1)

        weighted_var_concat_raw_var = tf.concat([weighted_var, inputs], -1)

        return weighted_var_concat_raw_var
