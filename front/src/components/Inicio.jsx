import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleLeft, faTimes } from '@fortawesome/free-solid-svg-icons';
import BotIAText from '../images/BotIAText.png';
import '../App2.css';  // Asegúrate de importar el archivo CSS

function Inicio() {
  const navigate = useNavigate();

  const irChat = async () => {
    navigate('/chatbot');
  };

  const irBotia = async () => {
    navigate('/botia');
  };

  return (
    <section>
      <div className="container">
        <div className="row d-flex justify-content-center">
          <div className="col-md-8 col-lg-6 col-xl-4">
            <div className="card overflow-auto" style={{ borderRadius: '15px', width: '450px', height: '650px', marginTop: '30px' }}>
              <div className="d-flex justify-content-between p-3 border-bottom-0" style={{ borderTopLeftRadius: '15px', borderTopRightRadius: '15px' }}>
                <FontAwesomeIcon icon={faAngleLeft} style={{ cursor: 'pointer' }} />
                <FontAwesomeIcon icon={faTimes} style={{ cursor: 'pointer' }} />
              </div>
              <div className="card-body">
                <div className="d-flex justify-content-center">
                  <img src={BotIAText} alt="BotIA" style={{ width: '40%', height: '100%', marginBottom: '2%', marginTop: '10%' }} />
                </div>
                <h2 className="custom-h2">Hola, mi nombre es BotIA, ¿Cómo puedo ayudarte hoy?</h2>
                <div className="row">
                  <div className="col-12 mb-3">
                    <button className="btn-custom" onClick={irChat}>Automatización de solicitudes</button>
                  </div>
                  <div className="col-12">
                    <button className="btn-custom" onClick={irBotia}>Preguntas frecuentes</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Inicio;
