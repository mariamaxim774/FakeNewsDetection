from flask import Flask
from flask_cors import CORS
from flask import request,jsonify
from services.fake_news_prediction import BertFakeNewsModelSingleton
app = Flask(__name__)

CORS(app)

model=BertFakeNewsModelSingleton()

@app.route('/predict_news',methods=['POST'])
def predict_news():
    data=request.get_json()
    text=data.get('text')
    model_prediction,confidence_levels=model.predict(text)
    confidence = int(confidence_levels[model_prediction] * 100)
    prediction = "True" if model_prediction == 1 else "Fake"
    print(prediction,confidence)
    return jsonify({"prediction":prediction,"confidence":confidence})

# Running app
if __name__ == '__main__':
    app.run(debug=True)