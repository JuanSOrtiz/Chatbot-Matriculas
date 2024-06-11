import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleLeft, faTimes } from '@fortawesome/free-solid-svg-icons';
import BotIAText from '../images/BotIAText.png';


function Login() {
  const [user, setUser] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://127.0.0.1:5001/guardar_credenciales', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user, password }),
    });
    const data = await response.json();
    console.log(data.mensaje);
    navigate('/inicio');
  };

  return (
    <section>
      <div className="container">
        <div className="row d-flex justify-content-center">
          <div className="col-md-8 col-lg-6 col-xl-4">
            <div className="card overflow-auto" style={{ borderRadius: '15px', width: '450px', height: '650px', marginTop: '30px' }}>
              <div className="d-flex justify-content-between p-3 border-bottom-0" style={{ borderTopLeftRadius: '15px', borderTopRightRadius: '15px' }}>
                <FontAwesomeIcon icon={faAngleLeft} />
                <FontAwesomeIcon icon={faTimes} style={{ cursor: 'pointer' }} />
              </div>
              <div className="card-body">
                <div className="d-flex justify-content-center">
                  <img src={BotIAText} alt="BotIA" style={{ width: '40%', height: '100%', marginBottom: '2%', marginTop: '10%' }} />
                </div>
                <form onSubmit={handleSubmit}>
                  <div className="form-group">
                    <label htmlFor="user">Usuario </label>
                    <input 
                      type="text"
                      id="user"
                      className="form-control"
                      value={user}
                      onChange={(e) => setUser(e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="password">Contraseña</label>
                    <input 
                      type="password"
                      id="password"
                      className="form-control"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </div>
                  <button type="submit" className="btn btn-primary btn-block bg-green-500" style={{ marginTop: '20px', backgroundColor: '#34D146'}}>Enviar</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Login;
