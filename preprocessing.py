from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pandas as pd
import nltk.data

nltk.download()
tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')

def remove_city_newsletter(text):
    return re.sub(r"^[A-Za-z/,\s]+(?:\([A-Za-z]+\))?\s-\s", '', text)


def remove_html_caracters(text):
    html_special_chars_pattern = r'&[a-zA-Z0-9#]+;|<|>'
    return re.sub(html_special_chars_pattern,'',text)

def remove_links(text):
    return re.sub(r'https?://\S+|www\.\S+', '', text)

def vectorized_data(text):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(text)
    vectorizer.get_feature_names_out()
    df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    return df


def data_steaming(text): #imi aduc cuvintele la forma de baza prin eliminarea sufixelor
    porter_stemmer = PorterStemmer()
    return " ".join([porter_stemmer.stem(word) for word in text.split()])

def cleaning_data(text): #removing stopwords and digits and lowercasing them
    stop_words = set(stopwords.words('english'))


    text = text.lower()
    text = re.sub('\n', '', text)
    regex_date_username = r"((january|february|march|april|may|june|july|august|september|october|november|december)\s\d{1,2},\s\d{4}).*?@(?!realDonaldTrump)\w+"

    text = re.sub(regex_date_username,'', text, flags=re.IGNORECASE) #eliminarea datelor
    text=remove_html_caracters(text)
    text=remove_city_newsletter(text)
    #text=remove_links(text)

    sentences=tokenizer.tokenize(text)

    text=" ".join(sentence for sentence in sentences if not sentence.startswith("Featured") )

    text = re.sub(r'[^\w\s]', '', text)  # elimin semnele de punctuatie
    text = re.sub(r"\d+", '', text)  # elimin cifrele

    return " ".join([w for w in text.split(" ") if w not in stop_words])


def data_tokenization(text): #functia de aici imi separa textul in cuvinte
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(text)

def preprocess_data(text):
    if isinstance(text, str):
        cleaned_data=cleaning_data(text)
        steamed_data=data_steaming(cleaned_data)
        #tokenized_data=data_tokenization(steamed_data)
        return steamed_data



