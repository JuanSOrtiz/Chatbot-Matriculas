import os
import sys

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin


import os

import xml.etree.ElementTree as ET
#import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
#from langchain_openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma
from langchain_openai import ChatOpenAI

import constants



os.environ["OPENAI_API_KEY"] = constants.APIKEY

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]


if PERSIST and os.path.exists("persist"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist")
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  #loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
  loader = DirectoryLoader("data/")

  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.2, max_tokens=256),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []


@app.route('/ask', methods=['POST'])
def ask_question():
    query = request.json.get('question')
    if not query:
        return jsonify({"error": "No question provided"}), 400

    result = chain({"question": query, "chat_history": chat_history})
    chat_history.append((query, result['answer']))

    return jsonify({"answer": result['answer']}), 200


@app.route('/chat-history', methods=['GET'])
def get_chat_history():
    return jsonify({"chat_history": chat_history}), 200

if __name__ == '__main__':
    app.run(debug=True)











# import os
# import sys

# import openai
# from langchain.chains import ConversationalRetrievalChain, RetrievalQA
# from langchain.chat_models import ChatOpenAI
# from langchain.document_loaders import DirectoryLoader, TextLoader
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.indexes import VectorstoreIndexCreator
# from langchain.indexes.vectorstore import VectorStoreIndexWrapper
# from langchain.llms import OpenAI
# from langchain.vectorstores import Chroma

# import constants

# os.environ["OPENAI_API_KEY"] = constants.APIKEY

# # Enable to save to disk & reuse the model (for repeated queries on the same data)
# PERSIST = False

# def load_data():
#     if PERSIST and os.path.exists("persist"):
#         print("Reusing index...\n")
#         vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
#         index = VectorStoreIndexWrapper(vectorstore=vectorstore)
#     else:
#         loader = DirectoryLoader("data/")
#         if PERSIST:
#             index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
#         else:
#             index = VectorstoreIndexCreator().from_loaders([loader])
#     return index

# index = load_data()

# chain = ConversationalRetrievalChain.from_llm(
#     llm=ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.2, max_tokens=256),
#     retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
# )

# chat_history = []

# while True:
#     query = input("Prompt: ")
#     if query in ['quit', 'q', 'exit']:
#         sys.exit()
#     elif query.startswith("train:"):
#         # Agregar la nueva instrucción al historial de chat para que el modelo la considere en futuros intercambios
#         nuevo_prompt = query[len("train:"):].strip()
#         chat_history.append(("Sistema", nuevo_prompt))
#         print("Nueva instrucción agregada al contexto.")
#     else:
#         result = chain({"question": query, "chat_history": chat_history})
#         print(result['answer'])

#         chat_history.append((query, result['answer']))
