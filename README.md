# Oncology Document Analyzer System
ODAS is a part of Project Based Learning. It focuses on delivering oncology-specific knowledge discovery through the application of NLP and Machine Learning, enabling improved drug advisory and diagnostic solutions

### Project Structure
    .
    ├── venv
    │   ├── ODAS
    │      ├── data     # dataset with emb model
    │      ├── getters  # LLM calls
    │      ├── models   # classifier models
    │      ├── utils    # prediction and pdf functionality
    │      ├── app.py   # frontend server
    │      └── requirements.txt # dependencies 
    ├── .gitignore
    └── README.md

### Environment Variables

Place your env in your python virtual environment, in this project 'venv'. To run this project, you will need to add the following environment variables to your .env file

`GROQ_API_KEY`

`LANGCHAIN_API_KEY`

`HUGGINGFACEHUB_API_TOKEN`

To start working with this project install the required dependencies. Inside 'ODAS' dir, run the command below:

```
pip install requirements.txt 
```

To the start the streamlit server
```
streamlit run app.py
```
### Training your models
#### To train classifier models
```
python models/[model-name]/train.py
```
All the trained models are stored in 'saved_models' directory.

#### To train word embedding model
```
python data/train_w2v.py
```
Embedding model is stored in 'embedding_model' directory.

## 🛠️ Contributors  
- **Om Aryan**  
- **Pranay Rokade**  
- **Mehansh Masih**  
- **Vivek Sharma**  
- **Harsh Saoji**  


#### Download the dataset from below: 
https://www.kaggle.com/datasets/falgunipatel19/biomedical-text-publication-classification
