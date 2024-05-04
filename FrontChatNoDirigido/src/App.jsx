import React, { useState } from 'react';
import './App.css'; // Asegúrate de tener los estilos CSS adecuados

function App() {
  const [pregunta, setPregunta] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: pregunta,
        }),
      });

      const data = await response.json();
      setRespuesta(data.answer); // Actualiza el estado respuesta con la respuesta del Chatbot

      // Agrega la pregunta y respuesta al historial de chat
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { pregunta, respuesta: data.answer },
      ]);

      // Limita el historial a las últimas 3 interacciones
      if (chatHistory.length >= 3) {
        setChatHistory((prevHistory) => prevHistory.slice(-3));
      }
      setPregunta(''); // Limpiar el campo de entrada después de enviar
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleInputChange = (e) => {
    setPregunta(e.target.value);
  };

  return (
    <div className="chat-container">
      <div className="chat-history">
        {chatHistory.map((item, index) => (
          <div key={index} className="chat-message">
            <div className="chat-message-question">
              <strong>Tú:</strong> {item.pregunta}
            </div>
            <div className="chat-message-answer">
              <strong>BotIA:</strong> {item.respuesta}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="chat-form">
        <input
          type="text"
          name="pregunta"
          id="pregunta"
          value={pregunta}
          onChange={handleInputChange}
          placeholder="Escribe tu pregunta aquí..."
          className="chat-input"
        />
        <button type="submit" className="chat-submit">
          Enviar
        </button>
      </form>
    </div>
  );
}

export default App;