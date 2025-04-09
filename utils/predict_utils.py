import os
import tensorflow as tf
import numpy as np

# LSTM switches
thyroid = tf.keras.models.load_model(os.path.abspath(     
    "models/saved_models/LSTM/thyroid_switch.keras"))
colon = tf.keras.models.load_model(os.path.abspath(     
    "models/saved_models/LSTM/colon_switch.keras"))
lung = tf.keras.models.load_model(os.path.abspath(     
    "models/saved_models/LSTM/lung_switch.keras"))

wvmodel = gensim.models.Word2Vec.load(os.path.abspath(  #loading word2vec embedding model
    "data/embedding_model/wvmodel.model"))
embedding_dim = wvmodel.vector_size


def text_to_embeddings(text, wvmodel):
    embeddings = [wvmodel.wv[word] for word in text.split() if word in wvmodel.wv]
    return np.mean(embeddings, axis=0) if embeddings else np.zeros(embedding_dim)

def preprocess_input(sentence, wvmodel, max_len=100):
    embeddings = text_to_embeddings(sentence, wvmodel)

    if (len(embeddings) < max_len):
        embeddings = np.pad(embeddings, ((0, max_len - len(embeddings)), (0,0)),
                            mode='constant')
    elif (len(embeddings) > max_len):
        embeddings = embeddings[:max_len]
    return np.reshape(embeddings, (1,1,max_len))

def switch_check(model, sentence):
    input_embeddings = preprocess_input(sentence, wvmodel)  # preprocessing
    
    prediction = model.predict(input_embeddings)  # model.predict returns a value between 0 and 1
    return prediction[0][0] if prediction[0][0] > 0.2 else 0

def predict_sentence(sentence):
    postive_classifications = {}

    postive_classifications['Thyroid Cancer'] = switch_check(thyroid, sentence)
    postive_classifications['Colon Cancer'] = switch_check(colon, sentence)
    postive_classifications['Lung Cancer'] = switch_check(lung, sentence)
    
    return {"Not Identified":0} if (list(postive_classifications.values())==[0,0,0]
                                ) else postive_classifications