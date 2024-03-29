import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Formulario from './Formulario';

function App() {
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
    <div className="App">
      <h1>Mensaje desde Python:</h1>
      <p>{mensaje}</p>
      <Formulario/>
    </div>
  );
}

export default App;
