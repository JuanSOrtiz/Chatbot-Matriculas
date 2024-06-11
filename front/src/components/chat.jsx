import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleLeft, faTimes } from '@fortawesome/free-solid-svg-icons';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Importar useNavigate
import axios from 'axios';
import BotIAText from '../images/BotIAText.png';
import BotIASimbol from '../images/BotIASimbol.png';
import Formulario from './Formulario';

function ChatComponent() {
  const navigate = useNavigate(); // Usar useNavigate para la navegación
  const [mensaje, setMensaje] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [initialMessageFetched, setInitialMessageFetched] = useState(false);

  useEffect(() => {
    if (!initialMessageFetched) {
      fetchInitialMessage();
    }
  }, [initialMessageFetched]);

  const fetchInitialMessage = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5001/inicio');
      addMessage(response.data.mensaje, 'bot');
      setLoading(false);
      setInitialMessageFetched(true);
    } catch (error) {
      console.error('Error fetching initial message:', error);
    }
  };

  const handleProcessed = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5001/respuesta');
      addMessage(response.data.respuesta, 'bot');
    } catch (error) {
      console.error('Error fetching response:', error);
    }
  };

  const handleResetChat = async () => {
    try {
      setRespuesta('');
      setHistory([]);
      setLoading(true);
      setInitialMessageFetched(false);
    } catch (error) {
      console.error('Error resetting chat:', error);
    }
  };

  const addMessage = (message, sender) => {
    setHistory(prevHistory => [...prevHistory, { message, sender }]);
  };

  return (
    <section>
      <div className="container">
        <div className="row d-flex justify-content-center">
          <div className="col-md-8 col-lg-6 col-xl-4">
            <div className="card overflow-auto" id="chat1" style={{ borderRadius: '15px', width: '450px', height: '650px', marginTop: '30px' }}>
              <div className="d-flex justify-content-between p-3 border-bottom-0" style={{ borderTopLeftRadius: '15px', borderTopRightRadius: '15px' }}>
                <FontAwesomeIcon icon={faAngleLeft} onClick={() => navigate('/inicio')} /> {/* Navegar a /inicio */}
                <FontAwesomeIcon icon={faTimes} onClick={handleResetChat} style={{ cursor: 'pointer' }} />
              </div>
              <div className="card-body">
                <div className="d-flex justify-content-center">
                  <img src={BotIAText} alt="BotIA" style={{ width: '40%', height: '100%', marginBottom: '2%', marginTop: '10%' }} />
                </div>

                {history.map((item, index) => (
                  <div key={index} className={`d-flex flex-row justify-content-${item.sender === 'bot' ? 'start' : 'center'} mt-4 mb-4`}>
                    {item.sender === 'bot' && <img src={BotIASimbol} alt="BotIA" style={{ width: '45px', height: '100%' }} />}
                    <div className="p-3 ms-3" style={{ borderRadius: '15px', backgroundColor: 'rgba(57, 192, 237, 0.2)' }}>
                      <p className="mb-0">{item.message}</p>
                    </div>
                  </div>
                ))}

                <Formulario onProcessed={handleProcessed} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default ChatComponent;
