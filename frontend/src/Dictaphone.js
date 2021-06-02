import React from 'react'
import { useRef, useState, useEffect } from "react";
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
import "./Dictaphone.css";
import microPhoneIcon from "./microphone.svg";

const Dictaphone = (props) => {
  const { transcript, resetTranscript } = useSpeechRecognition()
  const [isListening, setIsListening] = useState(false);
  const microphoneRef = useRef(null);
  



	
  
  const handleListing = () => {
	resetTranscript();
	props.parentCallback("");
    setIsListening(true);
    microphoneRef.current.classList.add("listening");
    SpeechRecognition.startListening({
      continuous: true,
    });
  };
  const stopHandle = () => { 
    setIsListening(false);
    microphoneRef.current.classList.remove("listening");
    SpeechRecognition.stopListening();
	props.parentCallback(transcript);
	resetTranscript();
  };

  

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return null
  }



  return (
 <div className="microphone-wrapper">
      <div className="mircophone-container">
        <div
          className="microphone-icon-container"
          ref={microphoneRef}
          onClick={handleListing}
        >
          <img src={microPhoneIcon} className="microphone-icon" />
        </div>
        <div className="microphone-status">
          {isListening ? "Listening........." : ""}
        </div>
        {isListening && (
          <button className="microphone-stop btn" onClick={stopHandle}>
            Stop
          </button>
        )}
      </div>
    </div>
  )
}
export default Dictaphone