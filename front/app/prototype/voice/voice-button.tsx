"use client";

import { useState } from "react";

const VoiceButton: React.FC = () => {
  const [result, setResult] = useState<string>("");

  const handleVoiceRecognition = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setResult("Your browser does not support the Web Speech API.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.addEventListener("result", (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0][0].transcript;
      setResult(`You said: ${transcript}`);
    });

    recognition.addEventListener("end", () => {
      recognition.stop();
    });

    recognition.addEventListener(
      "error",
      (event: SpeechRecognitionErrorEvent) => {
        setResult(`Error occurred: ${event.error} ${event.message}`);
      }
    );
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <button
        onClick={handleVoiceRecognition}
        className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-700 focus:outline-none"
      >
        Activate Voice Recognition
      </button>
      <p className="mt-4 text-lg text-gray-700">{result}</p>
    </div>
  );
};

export default VoiceButton;
