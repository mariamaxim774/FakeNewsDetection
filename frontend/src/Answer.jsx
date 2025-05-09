import { useState,useEffect } from "react";
function Answer(props){
    console.log(props.prediction)
    console.log(props.confidence)
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
        <p className="raspuns"><b>{props.prediction}</b></p>
        <div className="progress-container">
        <div className="progress w-50 " role="progressbar" aria-label="Answer" aria-valuemin="0" aria-valuemax="100" style={{height: "30px"}}>
        <div className={`progress-bar ${isReal ? "bg-success" : "bg-danger"}`} style={{width: `${confidence}%`}}>{confidence}%</div>
        </div>
        </div>
        <p className="textValidare">Confidence level</p>
        </>
    );
}

export default Answer