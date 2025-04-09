import sys
import pandas as pd
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from tqdm import tqdm

df = pd.read_csv('./processed/corpus.csv') # loading back the lemmetized corpus
sentences = df['text'].tolist()

# Initialize the progress bar
corpus = []             # Tokenize the sentences and update the progress bar
for sentence in tqdm(sentences, desc="Tokenizing"):
    tokens = word_tokenize(sentence.lower())
    corpus.append(tokens)

sys.stdout.write('\nTraining Word2Vec...')

# embedding model
wvmodel = Word2Vec(
    corpus,                 # Training data (list of sentences)
    vector_size=100,        # Dimension of the embedding vectors
    window=5,               # Context window size
    min_count=1,            # Minimum number of occurrences of a word
    sg=0     
)

sys.stdout.write("\nWord2Vec Training Successful.")
wvmodel.save("./embedding_model/wvmodel.model")     # save the embedding model