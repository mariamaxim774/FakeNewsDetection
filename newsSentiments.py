import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from NewsSentiment import TargetSentimentClassifier
import pandas as pd
from nltk.tokenize import sent_tokenize
from tqdm import tqdm
import time



tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)



def analyze_sentiments(text):
    try:
        #impart in propozitii
        sentences=sent_tokenize(text)
        neutral_sentiments=0
        positive_sentiments=0
        negative_sentiments=0

        for sentence in sentences:
            ner_spans = nlp(sentence)
            # ents = [span["word"] for span in ner_spans]
            # print(f"Entities: {ents}")
            tsc = TargetSentimentClassifier()
            for span in ner_spans:
                l = sentence[:span['start']]
                m = sentence[span['start']:span['end']]
                r = sentence[span['end']:]
                sentiment = tsc.infer_from_text(l, m, r)
                #print(f"{span['entity']}\t{sentiment[0]['class_label']}\t{sentiment[0]['class_prob']:.2f}\t{m}")
                if sentiment[0]['class_label']=='neutral':
                    neutral_sentiments+=1
                elif sentiment[0]['class_label']=='negative':
                    negative_sentiments+=1
                else:
                    positive_sentiments+=1

        return pd.Series({
            'nr_positive': positive_sentiments,
            'nr_neutral': neutral_sentiments,
            'nr_negative': negative_sentiments
        })
    except Exception as e:
        return pd.Series([0, 0, 0])

tqdm.pandas()

df=pd.read_csv("./data/cleaned_data.csv")
start=time.time()
df=df.sample(2)
df[['nr_positive', 'nr_neutral', 'nr_negative']] = df['text'].apply(analyze_sentiments)
end=time.time()
print(end-start)
df.to_csv("./data/cleaned_data_with_sentiments.csv")