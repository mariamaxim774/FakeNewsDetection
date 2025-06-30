from transformers import BertTokenizer, BertForSequenceClassification
import torch

class BertFakeNewsModelSingleton:
    instance = None
    tokenizer = None
    model = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(BertFakeNewsModelSingleton, cls).__new__(cls)
            cls.instance._load_model()
        return cls.instance

    def _load_model(self):
        try:
            self.tokenizer = BertTokenizer.from_pretrained("./services/bert_model_fake_news_detection_8")
            self.model = BertForSequenceClassification.from_pretrained("./services/bert_model_fake_news_detection_8")
            print("BERT tokenizer and model loaded successfully (Singleton).")
        except Exception as e:
            print(f"Error loading BERT model: {e}")
            self.tokenizer = None
            self.model = None

    def predict(self, text):
        if self.tokenizer is None or self.model is None:
            print("Model not loaded. Cannot make predictions.")
            return None

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            return predicted_class, probabilities.tolist()[0]