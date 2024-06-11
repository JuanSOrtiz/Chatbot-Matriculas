import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Importar useNavigate
import '../App2.css';
import { MainContainer, TypingIndicator, ConversationHeader } from "@chatscope/chat-ui-kit-react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleLeft, faTimes, faArrowRight } from '@fortawesome/free-solid-svg-icons';
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import BotIASimbol from '../images/BotIASimbol.png';
import BotIAText from '../images/BotIAText.png';
import Fing from '../images/fingenieria.png';
import User from '../images/User.png';

function Botia() {
  const navigate = useNavigate(); // Usar useNavigate para la navegación
  const [pregunta, setPregunta] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (pregunta.trim() === '') return;

    setIsLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: pregunta }),
      });

      const data = await response.json();
      setRespuesta(data.answer);

      setChatHistory((prevHistory) => [
        ...prevHistory,
        { pregunta, respuesta: data.answer },
      ].slice(-3)); // Limita el historial a las últimas 3 interacciones

      setPregunta('');
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => setPregunta(e.target.value);

  const openModal = () => setIsModalOpen(true);

  const closeModal = () => setIsModalOpen(false);

  const clearChatHistory = () => {
    setChatHistory([]);
    closeModal();
  };

  return (
    <div>
      <div style={{ marginLeft: '85%' }}>
        <button onClick={openModal} style={{ backgroundColor: 'white', border: 'none' }}>
          <img src={BotIASimbol} alt="BotIA" style={{ width: '30%', height: '40%', padding: '10px' }} />
        </button>
      </div>

      {isModalOpen && (
        <div style={{ position: 'relative', margin: 'auto', height: '100%', width: '500px', padding: '30px' }}>
          <MainContainer responsive style={{ height: '600px', display: 'block', borderRadius: '20px' }}>
            <ConversationHeader style={{ backgroundColor: 'ghostwhite', position: 'sticky', top: '0', zIndex: '1' }}>
              <ConversationHeader.Back>
                <FontAwesomeIcon icon={faAngleLeft} onClick={() => navigate('/inicio')} /> {/* Navegar a /inicio */}
              </ConversationHeader.Back>
              <ConversationHeader.Content style={{ paddingLeft: '95%' }}>
                <FontAwesomeIcon icon={faTimes} onClick={clearChatHistory} />
              </ConversationHeader.Content>
            </ConversationHeader>

            <div className="d-flex justify-content-center" style={{ display: 'flex' }}>
              <img src={BotIAText} alt="BotIA" style={{ width: '30%', height: '90%', marginBottom: '2%', paddingLeft: '17%', marginTop: '10%' }} />
              <img src={Fing} alt="BotIA" style={{ width: '30%', height: '90%', marginBottom: '2%', paddingLeft: '5%', marginTop: '10%' }} />
            </div>

            <div className="col-md-8 col-lg-6 col-xl-4" style={{ padding: '10px' }}>
              <div className="chat-history">
                {chatHistory.map((item, index) => (
                  <div key={index} className="chat-message">
                    <div style={{ display: 'flex' }}>
                      <div className="chat-message-question">{item.pregunta}</div>
                      <img src={User} alt="User" style={{ width: '35px', height: '90%', padding: '10px' }} />
                    </div>
                    <div style={{ display: 'flex' }}>
                      <img src={BotIASimbol} alt="BotIA" style={{ width: '45px', height: '100%', padding: '10px' }} />
                      {isLoading ? (
                        <TypingIndicator content="BotIA escribiendo" />
                      ) : (
                        <div className="chat-message-answer">{item.respuesta}</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
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
                style={{ width: '75%' }}
              />
              <button type="submit" className="chat-submit">
                <FontAwesomeIcon icon={faArrowRight} />
              </button>
            </form>
          </MainContainer>
        </div>
      )}
    </div>
  );
}

export default Botia;
