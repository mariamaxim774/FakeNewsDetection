import { useState,useEffect } from "react";
import Answer from "./Answer"
import Swal from 'sweetalert2';

function Form(){
    const [userInput, setUserInput] = useState("");
    const [prediction, setPrediction] = useState(null);
    const [confidence, setConfidence] = useState(null);
    const [spinner,activateSpinner]=useState(false);
    const [showPrediction, setShowPrediction] = useState(false);
    function handleSubmit(e) {
        e.preventDefault();
        if (!userInput.trim()) {
            setShowPrediction(false)
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'You should enter a news',
              });
             
        }
        else{
            setShowPrediction(true)
        }
        fetch("http://localhost:5000/predict_news", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: userInput })
        })
        .then(res => res.json())
        .then(data => {
            setPrediction(data.prediction);
            setConfidence(data.confidence)
            activateSpinner(false)
            
        })
        .catch(err => console.error(err));
    }

   

    return (
        <>
            <form onSubmit={handleSubmit}>
                <textarea
                    id="newsText"
                    name="text"
                    rows="6"
                    cols="70"
                    placeholder="Introduceti textul stirii aici"
                    value={userInput}
                    onChange={(e) => {setUserInput(e.target.value)}}
                />
                <button className="formButton" type="submit" onClick={() => activateSpinner(true)}>Verifica</button>
            </form>

            {spinner && (
                <div class="d-flex justify-content-center">
                <div class="spinner-border text-secondary" role="status">
                  <span class="sr-only"></span>
                </div>
              </div>
            )}
            {showPrediction && (
                <Answer prediction={prediction} confidence={confidence}/>
            )}
        </>
    );
}

export default Form;
