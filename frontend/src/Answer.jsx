import { useState,useEffect } from "react";
function Answer(props){
    let [isReal,setValue] = useState(true);
  
        useEffect(() => {
            if (props.prediction === "True") {
              setValue(true);
            } else {
              setValue(false);
              
            }
          }, [props.prediction]);
        const confidence=props.confidence;
        
      return(
        <>
        <p className="model"><b>{props.model}</b></p>
        <p className="raspuns"><b>{props.prediction === "True" ? "Adevărată" : "Falsă"}</b></p>
        <div className="progress-container">
        <div className="progress w-100 " role="progressbar" aria-label="Answer" aria-valuemin="0" aria-valuemax="100" style={{height: "30px"}}>
        <div className={`progress-bar ${isReal ? "bg-success" : "bg-danger"}`} style={{width: `${confidence}%`}}>{confidence}%</div>
        </div>
        </div>
        <p className="textValidare">Nivel de încredere  </p>
        </>
    );
}

export default Answer