from flask import Flask
from flask_cors import CORS
from flask import request,jsonify
from services.fake_news_prediction import BertFakeNewsModelSingleton
from werkzeug.exceptions import BadRequest
import joblib
import os
from transformers import pipeline
app = Flask(__name__)

CORS(app)

model=BertFakeNewsModelSingleton()
PIPELINE_PATH = os.path.join(os.path.dirname(__file__), './services/news_classifier_pipeline_naive_bayes.pkl')
pipeline_bayes = joblib.load(PIPELINE_PATH)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/api/predictions/bert',methods=['POST'])
def predict_news_bert():
    data=request.get_json()
    if not data or 'text' not in data:
        raise BadRequest("Missing 'text' in request body.")
    try:
        text=data.get('text')
        model_prediction,confidence_levels=model.predict(text)
        confidence = int(confidence_levels[model_prediction] * 100)
        prediction_label = "True" if model_prediction == 1 else "Fake"
        response = {
            "status": "success",
            "data": {
                "prediction": prediction_label,
                "confidence": confidence
            }
        }
        return jsonify(response), 200
    except Exception as e:
        print(f"Eroare la predictie: {e}")
        response={
            "status": "error",
            "message": "Eroare in timpul predictiei"
        }
        return jsonify(response), 500

@app.route('/api/predictions/nb', methods=['POST'])
def predict_news_naive_bayes():
    data = request.get_json()
    if not data or 'text' not in data:
        raise BadRequest("Missing 'text' in request body.")

    try:
        text = data['text']
        prediction = pipeline_bayes.predict([text])[0]
        confidence = pipeline_bayes.predict_proba([text])[0][prediction]

        return jsonify({
                "status": "success",
                "data": {
                    "prediction": "True" if prediction == 1 else "Fake",
                    "confidence": int(confidence * 100)
                }
            }), 200

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({
                "status": "error",
                "message": "Eroare în timpul predicției."
            }), 500

@app.route('/api/summary', methods=['POST'])
def resume_news():
    data = request.get_json()
    if not data or 'text' not in data:
        raise BadRequest("Missing 'text' in request body.")

    try:
        text = data['text']

        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return jsonify({
                "status": "success",
                "data": {
                    "summary": summary[0]['summary_text']
                }
            }), 200

    except Exception as e:
        print(f"Summary error: {e}")
        return jsonify({
                "status": "error",
                "message": "Eroare în timpul rezumării"
            }), 500


if __name__ == '__main__':
    app.run(debug=True)