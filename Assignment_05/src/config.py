import tensorflow as tf


IMAGE_SIZE = (224, 224)

MODELS = {
	'VGG16': tf.keras.applications.VGG16(
    include_top=True, weights='imagenet', input_tensor=None, input_shape=None,
    pooling=None, classes=1000, classifier_activation='softmax'
),

}