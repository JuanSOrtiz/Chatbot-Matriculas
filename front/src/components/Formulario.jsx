import React, { useState } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';

function Formulario({ onProcessed }) {
  const [inputValue, setInputValue] = useState('');
  const [courseValue, setCourseValue] = useState('');
  const [currentState, setCurrentState] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const symbol = (currentState === 'E38' || currentState === 'E39') ? courseValue : inputValue;
      const response = await axios.post('http://127.0.0.1:5001/procesar', { simbolo: symbol }, { headers: { 'Content-Type': 'application/json' } });
      if (response.data) {
        setCurrentState(response.data.estado_actual);
      } else {
        console.error('La respuesta recibida no contiene la propiedad "respuesta":', response.data);
      }
      setInputValue('');
      setCourseValue('');
      onProcessed(response.data);
    } catch (error) {
      console.error('Error al procesar el símbolo:', error);
    }
  };

  const handleChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleCourseChange = (e) => {
    setCourseValue(e.target.value);
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', alignItems: 'flex-end' }}>
      <div className="input-group">
        {(currentState === 'E38' || currentState === 'E39') && (
          <input
            type="text"
            value={courseValue}
            onChange={handleCourseChange}
            placeholder="Ingrese el curso"
            className="form-control"
          />
        )}
        {(currentState !== 'E38' && currentState !== 'E39') && (
          <input
            type="text"
            value={inputValue}
            onChange={handleChange}
            placeholder="Ingrese un símbolo"
            className="form-control"
          />
        )}
        <button type="submit" className="btn btn-primary">
          <FontAwesomeIcon icon={faArrowRight} />
        </button>
      </div>
    </form>
  );
}

export default Formulario;
