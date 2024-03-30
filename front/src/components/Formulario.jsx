import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';
import User from '../images/User.png'

function Formulario() {
  const [mensaje, setMensaje] = useState('');
  const [simbolo, setSimbolo] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/procesar', { simbolo }, { headers: { 'Content-Type': 'application/json' } });
      setMensaje(response.data);
    } catch (error) {
      console.error('Error al procesar el símbolo:', error);
    }
  };

  useEffect(() => {
    if (mensaje !== '') {
      window.location.reload();
    }
  }, [mensaje]);

  return (
  
    <form onSubmit={handleSubmit}>
      <div className="d-flex flex-row justify-content-end" style={{marginBottom:'20%'}}>
        <div className="p-3 me-3 border" style={{ borderRadius: '15px', backgroundColor: '#fbfbfb' }}>
          <p className="mb-0">{simbolo || "..."}</p>
        </div>
        <img src={User} alt="user" style={{ width: '45px', height: '100%' }} />
      </div>
      <div className="row reply justify-content-center" >
        <div class="col-sm-10 col-xs-10">
          <input className="form-control" style={{backgroundColor:'#fbfbfb'}} type="text" value={simbolo} onChange={(e) => setSimbolo(e.target.value)} />
        </div>
        <div class="col-sm-1 col-xs-1 reply-send">
        <button type='submit' style={{ border: 'none', background: 'none' }}><FontAwesomeIcon icon={faArrowRight} /></button>
        </div>
      </div>
      
    </form>
  );
}

export default Formulario;