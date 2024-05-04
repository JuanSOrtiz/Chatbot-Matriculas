# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 11:02:40 2024

@author: JUAN
"""

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
  llm=ChatOpenAI(model="gpt-3.5-turbo"),
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