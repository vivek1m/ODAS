import sys
import time
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd

# Download necessary NLTK resources for processing text
nltk.download('stopwords')
nltk.download('wordnet')  
nltk.download('punkt')

# Load the dataset and specify columns to use
df = pd.read_csv("./raw/cancer_doc_classification.csv", sep=',', skiprows=1, usecols=[1, 2], names=['label', 'text'], encoding='ISO-8859-1')

# Extract the 'text' column from the dataset
abstract = df['text']

# Function to lemmatize and clean raw data
def lemmetize_raw_data():
    # Initialize the WordNet lemmatizer
    lemm = WordNetLemmatizer()
    
    # List to store the processed text
    corpus = []
    
    # Loop through each text entry in the dataset
    for i in range(0, len(abstract)):
        # Display progress in the terminal
        sys.stdout.write('Lemmatized Sentence[' + str(i) + ']')
        time.sleep(0.0005)
        if i < len(abstract) - 1:
            sys.stdout.write('\r')  # Overwrite the previous line
        
        # Remove special characters and numbers, keeping only letters
        extract = re.sub('[^a-zA-Z0-9]', ' ', abstract[i])
        extract = extract.lower()  # Convert text to lowercase
        extract = extract.split()  # Split text into individual words
        
        # Lemmatize words and remove stopwords
        extract = [lemm.lemmatize(word) for word in extract if word not in stopwords.words('english')]
        
        # Join the words back into a single string
        extract = ' '.join(extract)
        
        # Append the processed sentence to the corpus
        corpus.append(extract)
    
    # Convert the processed corpus into a DataFrame
    corpus_df = pd.DataFrame(corpus, columns=['text'])
    
    # Print a success message
    sys.stdout.write('Successfully Lemmatized Corpus.')
    
    # Save the processed corpus to a CSV file
    corpus_df.to_csv('./processed/corpus.csv', index=False)

# Uncomment the function call below to run the text lemmatization process
