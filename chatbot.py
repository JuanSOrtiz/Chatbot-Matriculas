from flask import Flask, jsonify , request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


class AFD:

  def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_finales):
    self.estados = estados
    self.alfabeto = alfabeto
    self.transiciones = transiciones
    self.estado_actual = estado_inicial
    self.estados_finales = estados_finales

  def procesar_simbolo(self, simbolo):
    if simbolo not in self.alfabeto:
      raise ValueError("Símbolo no válido: " + simbolo)

    siguiente_estado = self.transiciones[(self.estado_actual, simbolo)]
    self.estado_actual = siguiente_estado

  def es_estado_final(self):
    if self.estado_actual in self.estados_finales:
      return True


estados = ["E0","E1", "E2", "E3","E4","E5","E6","E7","E8","E9","E10","E11","E12","E13","E14","E15","E16","E17","E18","E19","E20","E21","E22","E23","E24","E25","E26","E27","E28","E29","E30","E31","E32","E33","E34"]
alfabeto = ["0", "1","2","3","4","9"]
transiciones = {
  ("E0", "0"): "E1",
  ("E0", "1"): "E2",
  ("E0", "2"): "E3",
  ("E0", "3"): "E29",


  ("E1", "0"): "E4",
  ("E1", "1"): "E5",
  ("E1", "2"): "E6",
  ("E1", "3"): "E7",
  ("E1", "4"): "E8",

  ("E4", "0"): "E9",

  ("E5", "0"): "E10",
  ("E5", "1"): "E11",
  ("E5", "2"): "E12",

  ("E6", "0"): "E13",

  ("E7", "0"): "E14",

  ("E8", "0"): "E15",

  ("E2", "0"): "E16",
  ("E2", "1"): "E17",
  ("E2", "2"): "E18",

  ("E16", "0"): "E19",

  ("E17", "0"): "E20",

  ("E18", "0"): "E21",

  ("E3", "0"): "E22",
  ("E3", "1"): "E23",
  ("E3", "2"): "E24",

  ("E22", "0"): "E25",

  ("E23", "0"): "E26",
  ("E23", "1"): "E27",

  ("E24", "0"): "E28",


  ("E29", "0"): "E30",
  ("E29", "1"): "E31",
  ("E29", "2"): "E32",
  ("E29", "3"): "E33",
  ("E29", "4"): "E34",

}
estado_inicial = "E0"
estados_finales = ["E9", "E10", "E11", "E12","E13","E14","E15", "E19","E20","E21","E25","E26","E27","E28","E30","E31","E32","E33","E34"]


chatbot = AFD(estados, alfabeto, transiciones, estado_inicial, estados_finales)

@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.json
    simbolo = data.get('simbolo')
    chatbot.procesar_simbolo(simbolo)
    response = jsonify({"mensaje": "Procesado correctamente"})
    response.headers['Access-Control-Allow-Origin'] = '*'  # Permitir solicitudes desde cualquier origen
    return response
    


@app.route('/inicio')
def inicio():
    respuestas={'E0':"0.Prematrícula, 1.Matrícula, 2.Ajustes 3.Definiciones y reglamentación",
                'E1':"0.Impedimentos, 1.Tandas, 2.Calendario, 3.Grupos, 4.Papeleria",
                "E2":"0.Impedimentos, 1.Cupos, 2.Calendario",
                'E3':"0.Cupos, 1.Calendario, 2.Incumplimiento",
                "E4":"0.Que pasa si salen impedimentos al matricularme?",
                "E5":"0.Por qué no me llega al correo que tanda me tocó? 1.Donde miro mi tanda? 2.Por qué no me muestra mi tanda?",
                "E6":"0.Cuando puedo ver mi tanda?",
                "E7":"0.¿Dónde puedo consultar los grupos de las materias, horarios y profesores?",
                "E8":"0.¿Cuándo van a revisar la documentación?",
                "E9":"Si tiene algún impedimento por liquidación de matrícula debe enviar un email a liquidacionpregrado@udea.edu.co.  Si es por pago debe escribir a carteraestudiantes@udea.edu.co. Si es por cantidad de créditos, diríjase a su pensum y a su versión correspondiente en el siguiente enlace: Que pasa si me salen impedimentos al matricularme?",
                "E10":"Los estudiantes son los responsables de mirar qué tanda les tocó a través del portal, y no solo eso, también deben mirar la oferta, generar la matrícula y descargar la constancia de la matrícula.",
                "E11":"Para mirar la tanda, deberá ingresar al Portal Universitario con su usuario y clave, y seguir la ruta:Estudiantes > Proceso de matrícula > Oferta de materias Allí podrá mirar la fecha y hora en la que deberá realizar la matrícula el día que esté estipulado la oferta de materias en el calendario académico.",
                "E12":"Seguramente aún no es el día de la oferta de materias. Consulta en el calendario académico y vuelve a consultar ese día.",
                "E13":"Consulta en el calendario académico.",
                "E14":"Puede consultarlos en el siguiente enlace: www.ayudame2.udea.edu.co",
                "E15":"La revisión de la documentación se hace de forma progresiva, debe estar constantemente pendiente de si ésta fue aprobada o no.",
                "E16":"0.¿Por qué no puedo matricularme?",
                "E17":"0.¿Qué hago si no hay cupo?",
                "E18":"0.¿Cuándo puedo matricularme?",
                "E19":"Si obtuviste rendimiento académico insuficiente no podrás matricularte, pero podrás presentar el próximo exámen de admisión a la UdeA al programa de tu preferencia",
                "E20":"Debes esperar a ajustes ya que ahí se abrirán nuevos cupos para los cursos.",
                "E21":"Para mirar cuándo puede realizar su matrícula, deberá ingresar al Portal Universitario con su usuario y clave, y seguir la ruta: Estudiantes > Proceso de matrícula > Oferta de materias Allí podrá mirar la fecha y hora en la que deberá realizar la matrícula el día que esté estipulado la oferta de materias en el calendario académico.",
                "E22":"0.¿Qué pasa si en ajustes tampoco hay cupo?",
                "E23":"0.¿Cuándo va a ser ajustes de matrículas? 1.¿Cómo puedo realizar la solicitud de cancelación extemporánea de uno o varios curso(s) registrado(s) en un semestre académico que no aplicaron Garantías Académicas?",
                "E24":"0.¿Qué pasa si no alcancé a matricular en la temporada de matrículas?¿Cuándo va a haber matrícula extemporánea?",
                "E25":"Dependiendo de la materia deberás solicitar el cupo. Si la materia es del tronco común, deberás pedirlo a vicedecanatura; si la materia es de la carrera, deberás pedirlo el jefe de la carrera, si es sociohumanístico deberá escribir al correo cursoshing@udea.edu.co. La solicitud de cupos del programa de Inglés PIFLE para los estudiantes de la versión 5 del pensum se deben solicitar a   coordinacionprogramainstitucionalingles@udea.edu.co o a gildominguezolga@gmail.com",
                "E26":"Deberás mirar el calendario académico. Allí se indica el período de ajustes de matrículas.",
                "E27":"Para presentar la solicitud de cancelación extemporánea de uno o varios curso(s), el estudiante deberá generar un caso en el Sistema de Solicitudes de la Facultad de Ingeniería-SSOFI-, así: 1. En cualquier buscador de Internet consulte 'Sistema de Solicitudes Facultad de Ingeniería SSOFI' - Seleccione el enlace https://ssofi.udea.edu.co/ingenieria/ 2. Digite su usuario y clave del Portal. 3. Seleccione la opción 'GENERAR', y diligencie completamente los campos del formulario que le aparecen: - En categoría, seleccione “Programas de Pregrado”, luego su programa académico. - En Comité o Consejo, seleccione “Comité de Asuntos Estudiantiles de Pregrado Virtuales y Regionalizados” o “Comité de Asuntos Estudiantiles de Pregrado Presenciales”, según sea el caso. - En Asunto, seleccione “Asuntos Estudiantiles”. - Seleccione el tipo de solicitud: Cancelación Extemporánea de curso(s) - Diligencie el campo “Descripción y justificación” con la siguiente información: Especifique el semestre académico e indique el código, nombre y grupo de el(los) curso(s) que solicita cancelar. Además, debe exponer los argumentos que sustentan la solicitud.  - En el campo de Anexos, deberá anexar los documentos que sustenten los argumentos expuestos y que considere para el estudio de la solicitud.  - Cuando termine de diligenciar toda la información y haga clic en la opción 'Guardar', el sistema le arrojará un número de caso, el cual debe conservar para hacerle seguimiento a la solicitud.",
                "E28":"El/la estudiante que no registre la matrícula del semestre académico 2022/1 el 11 de mayo de 2022, fecha establecida en el calendario académico, podrá realizar la matrícula en época de ajustes a la matrícula, es decir, entre el 13 y 20 de mayo de 2022. Por lo cual, no tiene que realizar trámite para levantar impedimento de matrícula extemporánea.",
                "E29":"0.¿Qué es un crédito académico? 1.¿Para qué me sirve el promedio? 2.¿Los cursos clasificados o reconocidos inciden en el promedio del semestre y el acumulado? 3.¿Qué es el periodo de prueba? 4.¿Cuál es el estado de insuficiencia?",
                "E30":"Es la unidad que mide el tiempo estimado de actividad académica del estudiante en función de las competencias profesionales y académicas. Un crédito equivale a 48 horas totales de trabajo del estudiante, incluidas las horas académicas con acompañamiento docente y las demás horas que deba emplear en actividades independientes de estudio, prácticas, preparación de exámenes u otras necesarias para alcanzar las metas de aprendizaje.",
                "E31":"El promedio del semestre permite determinar el rendimiento del estudiante en la Universidad y por tanto su situación académica. El promedio acumulado permite acceder a estímulos académicos o procesos de movilidad nacional e internacional, entre otros.",
                "E32":"No, los cursos clasificados o reconocidos de la Universidad o de otra institución no se tienen en cuenta para el cálculo de los promedios",
                "E33":"Cuando el período académico anterior fue su primer semestre en la Universidad y obtuvo un promedio igual o superior a  2.50 e inferior a 2.80. Si ha cursado más de un semestre y en el último período académico su promedio es inferior a 3.00 y al computarlo con el del semestre anterior a éste, el promedio aritmético sigue siendo inferior a 3.00 pero no menor que 2.50.",
                "E34":"Al terminar su primer semestre obtiene un promedio inferior a 2.50. Ha cursado más de un semestre, en el último período académico el promedio es  inferior a 3.00 y al computarlo con el del semestre anterior a éste el resultado aritmético es inferior a 2.50. Habiendo acumulado en su historia académica dos períodos de prueba,  en un nuevo semestre el promedio es inferior a 3.00 y al computarlo con el del período anterior a éste el promedio aritmético resultante sigue siendo inferior a 3.00."}
    return respuestas[chatbot.estado_actual]


@app.route('/test', methods=['GET'])
def test():
    return chatbot.estado_actual

if __name__ == '__main__':
    app.run(debug=True)
    









    
    
