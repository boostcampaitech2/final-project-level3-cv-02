import tensorflow as tf
from keras.models import load_model
import keras





session = tf.Session(graph=tf.Graph())
loaded_model = None

def ready_model(export_path):
    # global variables
    # global graph
	global	loaded_model
	global	session

	if loaded_model is None:
		with session.graph.as_default():
			keras.backend.set_session(session)
			loaded_model = keras.models.load_model(export_path)

    # loaded_model = load_model(export_path)
    # graph = tf.get_default_graph()



# loaded_model = None
# graph = None