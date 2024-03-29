import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
      <label htmlFor="">Ingrese el numero</label>
      <input type="text" value={simbolo} onChange={(e) => setSimbolo(e.target.value)} />
      <button type='submit'>Enviar</button>
    </form>
  );
}

export default Formulario;