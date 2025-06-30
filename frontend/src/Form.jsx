import { useState } from "react";
import Answer from "./Answer";
import Swal from "sweetalert2";

function Form() {
  const [userInput, setUserInput] = useState("");
  const [prediction, setPrediction] = useState({ bert: null, nb: null });
  const [confidence, setConfidence] = useState({ bert: null, nb: null });
  const [spinner, activateSpinner] = useState(false);
  const [showPrediction, setShowPrediction] = useState(false);
  const [summary, setSummary] = useState();
  const [showSummary, setShowSummary] = useState(false);

  function handleVerify(e) {
    e.preventDefault();
    if (!userInput.trim()) {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "You should enter a news",
      });
      activateSpinner(false);
      setShowPrediction(false);
      return;
    }

    setShowSummary(false);
    activateSpinner(true);
    Promise.all([
      fetch("http://localhost:5000/api/predictions/bert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userInput }),
      }).then((res) => res.json()),

      fetch("http://localhost:5000/api/predictions/nb", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userInput }),
      }).then((res) => res.json()),
    ])
      .then(([bertData, nbData]) => {
        if (bertData.status === "success" && nbData.status === "success") {
          setPrediction({
            bert: bertData.data.prediction,
            nb: nbData.data.prediction,
          });
          setConfidence({
            bert: bertData.data.confidence,
            nb: nbData.data.confidence,
          });
          setShowPrediction(true);
        } else {
          Swal.fire({
            icon: "error",
            title: "Eroare",
            text: "Răspuns invalid de la unul din modele",
          });
        }
      })
      .catch((err) => {
        console.error(err);
        Swal.fire({
          icon: "error",
          title: "Eroare",
          text: "Nu s-au putut face predicțiile.",
        });
      })
      .finally(() => activateSpinner(false));
  }

  function handleSummarize() {
    if (!userInput.trim()) {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Introduceți un text pentru rezumat.",
      });
      return;
    }

    activateSpinner(true);
    fetch("http://localhost:5000/api/summary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: userInput }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          setSummary(data.data.summary);
          setShowSummary(true);
          setShowPrediction(false);
        } else {
          Swal.fire({
            icon: "error",
            title: "Eroare",
            text: "Rezumatul nu a putut fi generat.",
          });
        }
      })
      .catch((err) => {
        console.error(err);
        Swal.fire({
          icon: "error",
          title: "Eroare",
          text: "Eroare de rețea sau server.",
        });
      })
      .finally(() => activateSpinner(false));
  }

  return (
    <>
      <div className="form-and-result-container">
        <div className="form-section">
          <form>
            <textarea
              id="newsText"
              name="text"
              rows="6"
              cols="70"
              placeholder="Introduceti textul stirii aici"
              value={userInput}
              onChange={(e) => {
                setUserInput(e.target.value);
              }}
            />
            <div className="actions">
              <button
                className="checkButton"
                type="button"
                onClick={handleVerify}
              >
                Verifica
              </button>
              <button
                className="summaryButton"
                type="button"
                onClick={handleSummarize}
              >
                Rezumat
              </button>
            </div>
          </form>

          {spinner && (
            <div className="d-flex justify-content-center">
              <div className="spinner-border text-secondary" role="status">
                <span className="sr-only"></span>
              </div>
            </div>
          )}
        </div>

        <div className="results-section">
          {showSummary ? (
            <div className="summary-box">
              <h3>Rezumatul știrii:</h3>
              <p>{summary}</p>
            </div>
          ) : !showPrediction ? (
            <div className="model-info">
              <h3>Cum verificăm veridicitatea știrii?</h3>
              <p>
                <strong>BERT</strong> folosește o rețea neuronală antrenată pe
                limbaj natural pentru a înțelege contextul propoziției.
              </p>
              <p>
                <strong>Bayes Naiv</strong> este un model probabilistic care
                estimează șansele ca o știre să fie falsă pe baza frecvenței
                cuvintelor și a probabilităților condiționate.
              </p>
            </div>
          ) : (
            <div className="container">
              <div className="item">
                <Answer
                  model="BERT"
                  prediction={prediction.bert}
                  confidence={confidence.bert}
                />
              </div>
              <div className="item">
                <Answer
                  model="Bayes Naiv"
                  prediction={prediction.nb}
                  confidence={confidence.nb}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default Form;
