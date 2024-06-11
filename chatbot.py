from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import subprocess
import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


app = Flask(__name__)
CORS(app)

class AFD:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_finales, respuestas):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_actual = estado_inicial 
        self.estados_finales = estados_finales
        self.respuestas = respuestas
        self.sede = None
        self.tipo = None
        self.user = None
        self.password = None
        self.course = None

    def procesar_simbolo(self, simbolo):
        print(self.estado_actual)
        if self.estado_actual == "E38" or self.estado_actual == "E39":
            self.course = simbolo
            siguiente_estado = self.transiciones.get((self.estado_actual, "ANY"))
            if siguiente_estado:
                self.estado_actual = siguiente_estado
                self.actualizar_datos()
                if self.estado_actual == "E40":
                    self.realizar_automatizacion()
                    print("Ejecutando el script")
            else:
                raise ValueError("Transición no definida para el estado E_Course")
        else:
            if simbolo not in self.alfabeto:
                raise ValueError("Símbolo no válido: " + simbolo)
            siguiente_estado = self.transiciones.get((self.estado_actual, simbolo))
            if siguiente_estado:
                self.estado_actual = siguiente_estado
                self.actualizar_datos()
                if self.estado_actual == "E40":
                    self.realizar_automatizacion()
                    print("Ejecutando el script")
            else:
                raise ValueError("Transición no definida para el símbolo: " + simbolo)

    def actualizar_datos(self):
        if self.estado_actual == "E36":
            self.sede = "Ingenieria sistemas presencial"
        elif self.estado_actual == "E37":
            self.sede = "Ingenieria sistemas virtual"
        elif self.estado_actual == "E38":
            self.tipo = "ajuste matricula"
        elif self.estado_actual == "E39":
            self.tipo = "comite carrera"

    def obtener_respuesta(self, estado):
        return self.respuestas.get(estado, "No hay respuesta para este estado.")
    
    def realizar_automatizacion(self):
        try:
            driver = webdriver.Chrome()
            driver.get("https://ssofi.udea.edu.co/ingenieria/")
            assert "Sistema de Solicitudes" in driver.title
            user = driver.find_element(By.NAME, "txtIdentificacion")
            user.clear()
            user.send_keys(self.user)
            password = driver.find_element(By.NAME, "txtClave")
            password.clear()
            password.send_keys(self.password)
            password.send_keys(Keys.RETURN)
            driver.switch_to.frame(0)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btn0_1"))).click()
            driver.switch_to.parent_frame()
            driver.switch_to.frame(2)
            category = Select(driver.find_element(By.ID, "cboCategoria"))
            category.select_by_visible_text("Programas de pregrado")
            wait = WebDriverWait(driver, 10)
            if self.sede == "Ingenieria sistemas presencial":
                department = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/table/tbody/tr[4]/td/table/tbody/tr[5]/td[2]/select/option[35]")))
            elif self.sede == "Ingenieria sistemas virtual":
                department = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/table/tbody/tr[4]/td/table/tbody/tr[5]/td[2]/select/option[33]")))
            department.click()
            if self.tipo == "ajuste matricula":
                comittee = Select(driver.find_element(By.ID, "cboComite"))
                comittee.select_by_visible_text("Ajustes de Matrícula - Ing. de Sistemas")
                case = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/table/tbody/tr[4]/td/table/tbody/tr[7]/td[2]/select/option[2]")))
                case.click()
                caseType = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/table/tbody/tr[4]/td/table/tbody/tr[8]/td[2]/select/option[2]")))
                caseType.click()
            elif self.tipo == "comite carrera":
                comittee = Select(driver.find_element(By.ID, "cboComite"))
                comittee.select_by_visible_text("Comité de Carrera - Ingeniería de Sistemas")
                case = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/table/tbody/tr[4]/td/table/tbody/tr[7]/td[2]/select/option[2]")))
                case.click()
                caseType = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/table/tbody/tr[4]/td/table/tbody/tr[8]/td[2]/select/option[4]")))
                caseType.click()
            time.sleep(2)
            textArea = driver.find_element(By.ID, "txtJustificacion")
            textArea.clear()
            textArea.send_keys(f"Curso: {self.course}")
            textDescription = driver.find_element(By.ID, "txtDescripcion1")
            textDescription.click()
            textDescription.clear()
            textDescription.send_keys(f"Curso: {self.course}")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        finally:
            input("Presiona Enter para salir...")
            driver.quit()

# Estados y configuraciones del AFD
estados = ["E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12", "E13", "E14", "E15", "E16", "E17", "E18", "E19", "E20", "E21", "E22", "E23", "E24", "E25", "E26", "E27", "E28", "E29", "E30", "E31", "E32", "E33", "E34", "E35", "E36", "E37", "E38", "E39", "E40"]
alfabeto = ["0", "1", "2", "3", "4", "9"]
estado_inicial = "E0"
estados_finales = ["E9", "E10", "E11", "E12", "E13", "E14", "E15", "E19", "E20", "E21", "E25", "E26", "E27", "E28", "E30", "E31", "E32", "E33", "E34", "E40"]

transiciones = {
    ("E0", "0"): "E1", ("E0", "1"): "E2", ("E0", "2"): "E3", ("E0", "3"): "E29", ("E0", "4"): "E35",
    ("E1", "0"): "E4", ("E1", "1"): "E5", ("E1", "2"): "E6", ("E1", "3"): "E7", ("E1", "4"): "E8",
    ("E4", "0"): "E9",
    ("E5", "0"): "E10", ("E5", "1"): "E11", ("E5", "2"): "E12",
    ("E6", "0"): "E13",
    ("E7", "0"): "E14",
    ("E8", "0"): "E15",
    ("E2", "0"): "E16", ("E2", "1"): "E17", ("E2", "2"): "E18",
    ("E16", "0"): "E19",
    ("E17", "0"): "E20",
    ("E18", "0"): "E21",
    ("E3", "0"): "E22", ("E3", "1"): "E23", ("E3", "2"): "E24",
    ("E22", "0"): "E25",
    ("E23", "0"): "E26", ("E23", "1"): "E27",
    ("E24", "0"): "E28",
    ("E29", "0"): "E30", ("E29", "1"): "E31", ("E29", "2"): "E32", ("E29", "3"): "E33", ("E29", "4"): "E34",
    ("E35", "0"): "E36", ("E35", "1"): "E37",
    ("E36", "0"): "E38", ("E36", "1"): "E39", ("E37", "0"): "E38", ("E37", "1"): "E39",
    ("E38", "ANY"): "E40", ("E39", "ANY"): "E40",
}

ruta_respuestas = "respuestas.json"

with open(ruta_respuestas, "r", encoding="utf-8") as file:
    respuestas = json.load(file)

chatbot = AFD(estados, alfabeto, transiciones, estado_inicial, estados_finales, respuestas)

@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.json
    simbolo = data.get('simbolo')
    try:
        chatbot.procesar_simbolo(simbolo)
        response = {"mensaje": "Procesado correctamente", "estado_actual": chatbot.estado_actual}
    except ValueError as e:
        response = {"error": str(e)}
    return jsonify(response)

@app.route('/respuesta', methods=['GET'])
def obtener_respuesta():
    estado = chatbot.estado_actual
    respuesta = chatbot.obtener_respuesta(estado)
    return jsonify({"estado": estado, "respuesta": respuesta})

@app.route('/inicio', methods=['GET'])
def inicio():
    chatbot.estado_actual = "E0"
    estado_inicial_respuesta = chatbot.obtener_respuesta(chatbot.estado_actual)
    return jsonify({"mensaje": estado_inicial_respuesta})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"estado_actual": chatbot.estado_actual})

@app.route('/guardar_credenciales', methods=['POST'])
def guardar_credenciales():
    data = request.json
    chatbot.user = data.get('user')
    chatbot.password = data.get('password')
    return jsonify({"mensaje": "Credenciales guardadas correctamente"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
