import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleLeft, faTimes } from '@fortawesome/free-solid-svg-icons';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import BotIAText from '../images/BotIAText.png'
import BotIASimbol from '../images/BotIASimbol.png'
import Formulario from './Formulario';


function ChatComponent() {
    const [mensaje, setMensaje] = useState('');
    useEffect(() => {
    async function fetchMensaje() {
        try {
        const response = await axios.get('http://127.0.0.1:5000/inicio');
        setMensaje(response.data);
        } catch (error) {
        console.error('Error al obtener el mensaje:', error);
        }
    }

    fetchMensaje();
    }, []);
      
    
  return (
    <section>
      <div className="container">
        <div className="row d-flex justify-content-center">
          <div className="col-md-8 col-lg-6 col-xl-4">
            <div className="card overflow-auto" id="chat1" style={{ borderRadius: '15px', width: '450px', height: '650px', marginTop:'30px'}}>
              <div className=" d-flex justify-content-between p-3 border-bottom-0" style={{ borderTopLeftRadius: '15px', borderTopRightRadius: '15px' }}>
                <FontAwesomeIcon icon={faAngleLeft} />
                <FontAwesomeIcon icon={faTimes} />
              </div>
              <div className="card-body">
                {/* Here begins chat content*/}
                <div className="d-flex justify-content-center">
                    <img src= {BotIAText} alt="BotIA" style={{ width: '40%', height: '100%', marginBottom:'2%', marginTop:'10%' }} />
                </div>
                
                <div className="d-flex flex-row justify-content-center mt-4 mb-4">
                    <div className="p-3 ms-3" style={{ borderRadius: '15px', backgroundColor: 'rgba(57, 192, 237, 0.2)' }}>
                    <p className="mb-0">Hola</p>
                    </div>
                </div>

                <div className="d-flex flex-row justify-content-center mt-4 mb-4">
                    <div className="p-3 ms-3" style={{ borderRadius: '15px', backgroundColor: 'rgba(57, 192, 237, 0.2)' }}>
                    <p className="mb-0">¿Cómo puedo ayudarte?</p>
                    </div>
                </div>

                <div className="d-flex flex-row justify-content-start mt-4 mb-4" style={{marginTop:'30%'}}>
                    <img src={BotIASimbol} alt="BotIA" style={{ width: '45px', height: '100%' }} />
                    <div className="p-3 ms-3" style={{ borderRadius: '15px', backgroundColor: 'rgba(57, 192, 237, 0.2)' }}>
                    <p className="mb-0">{mensaje}</p>
                    </div>
                </div>
                <Formulario/>

              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default ChatComponent;
