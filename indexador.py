#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import codecs
import resource
import os
from os import makedirs
from os.path import join, isdir
from struct import Struct

class Tokenizador(object):
    FORMATO_POSTING = "I" # DOC_ID
    FORMATO_INDICE = "I I I" # ID_TERM DF PUNTERO_POSTING

    def __init__(self, path_corpus, path_vacias=None):
        self.path_corpus = path_corpus
        self.vacias = []
        self.documentos = os.listdir(path_corpus)
        self.initStructures()
        self.nombre_doc_actual = None
        self.doc_actual_tiene_terminos = None
        self.cargar_lista_vacias(path_vacias)
        self.crear_directorio()

    def initStructures(self):
        self.lexicon = {}
        self.posting = []


    def createChunks(self):
        print "Procesando documentos..."
        try:
            a = range(10000000000)
        except MemoryError as error:
            print "MEMORY ERROR!"
        

    def analizar_documento(self, path_doc, doc_id):
        # Leemos el archivo
        pass

    def generatePostingAux(self, tokens, doc_id):
        # Recorremos los tokens
        pass

    def update_vocabulario(self, tokens, doc_id):
        # Recorremos los tokens
        for token in tokens:
            # Si el termino no esta en el vocabulario lo agrego
            if token not in self.lexicon:
                self.lexicon[token] = 0 # Document frecuency
                self.posting[token] = {} # array de doc_id
            # Si el doc_id no esta en el listado de docs de ese token lo agrego
            if doc_id not in self.posting[token]:
                self.posting[token][doc_id] = 1 # Agrego el doc_id a la lista de posting
                self.lexicon[token] += 1 # Aumento en 1 el documento frecuency
            else:
                self.posting[token][doc_id] += 1 # Aumento el TF del doc_id

    @staticmethod
    def translate(to_translate):
        tabin = u"áéíóú"
        tabout = u"aeiou"
        tabin = [ord(char) for char in tabin]
        translate_table = dict(zip(tabin, tabout))
        return to_translate.translate(translate_table)

    @staticmethod
    def minMaxLargo(tokens):
        tokensAux = []
        for token in tokens:
            if len(token) >= 3 and len(token) <= 20 :
                tokensAux.append(token)
        return tokensAux

    # Tokenizador básico
    @staticmethod
    def tokenizar(texto, vacias = []):
        # To lower case
        texto = texto.lower()
        # Eliminamos caracteres especiales
        texto = Tokenizador.translate(texto)
        # Reemplazamos caracteres especiales con espacios
        texto = re.sub(u"[^a-zñ]|_", " ", texto)
        tokens = texto.split()
        # Sacamos stopwords si es necesario
        if len(vacias) > 0:
            tokens = list(set(tokens) - set(vacias))
        return tokens

    def cargar_lista_vacias(self, path_vacias):
        if path_vacias is not None:
            with codecs.open(path_vacias, mode="r", encoding="utf-8") as file_vacias:
                texto_vacias = file_vacias.read()
                self.vacias = textp_vacias.split()

    def crear_directorio(self):
        try:
            makedirs('index')
        except OSError:
            if not isdir('index'):
                raise

    def guardar_terminos(self):
        with codecs.open('index/terminos.txt', mode="w", encoding="utf-8") as file_terminos:
            for termino in self.terminos:
                file_terminos.write(termino + "\n")

    def guardar_documentos(self):
        with codecs.open('index/documentos.txt', mode="w", encoding="utf-8") as file_documentos:
            for nombre_doc in self.documentos:
                file_documentos.write(nombre_doc + "\n")

    def guardar_postings(self):
        packer = Struct(self.FORMATO_POSTING)
        puntero_posting = 0
        with open('index/postings.bin', mode="wb") as file_postings:
            for id_termino, termino in enumerate(self.terminos):
                # Por cada documento guardo el doc_id
                for doc_id in sorted(self.posting[termino]):
                    file_postings.write(packer.pack(doc_id))

    def guardar_indice(self):
        packer = Struct(self.FORMATO_INDICE)
        puntero_posting = 0
        with open('index/lexicon.bin', mode="wb") as file_lexicon:
            for id_termino, termino in enumerate(self.terminos):
                # ID | DF | PUNTERO
                file_lexicon.write(packer.pack(id_termino, self.lexicon[termino] ,puntero_posting)) 
                puntero_posting += self.lexicon[termino] * 4 # DF * 4 = X Bytes

def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    print 'Memoria  Maxima Asignada  :', soft

def start(dir_corpus, path_vacias=None):
    limit_memory(1) # limite en cantidad de bytes
    tokenizador = Tokenizador(dir_corpus, path_vacias=path_vacias)
    tokenizador.createChunks()
    print u"Finalizado!"

if __name__ == "__main__":
    if "-h" in sys.argv:
        print "MODO DE USO: python booleano.py -c <path_directorio_corpus> [-v <path_archivo_stopwords>]"
        sys.exit(0)
    if len(sys.argv) < 3:
        print "ERROR: "
        sys.exit(1)
    if "-c" in sys.argv:
        if sys.argv.index("-c") + 1 == len(sys.argv):
            print "ERROR: Debe ingresar el directorio del corpus"
            sys.exit(1)
        else:
            path_corpus = sys.argv[sys.argv.index("-c") + 1]
    if "-v" in sys.argv:
        if sys.argv.index("-v") + 1 == len(sys.argv):
            print "ERROR: Debe ingresar el path del archivo con stopwords"
            sys.exit(1)
        else:
            path_vacias = sys.argv[sys.argv.index("-v") + 1]

    start(path_corpus,path_vacias = None)