#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import unicodecsv
import csv
import time
from copy import deepcopy

 #-----Mostrar MENU de opções"----#   
def resolverSudoku(tipo_algoritmo, sudoku_entrada):
    resultadoSudoku = sudoku_entrada
    TENTATIVA_ATRIBUICAO = 0

    if tipo_algoritmo == "1":
        backt_Simples= backtSimples()
        resultadoSudoku= backt_Simples.resolver_soduko(sudoku_entrada)
        TENTATIVA_ATRIBUICAO = backt_Simples.get_TENTATIVA_ATRIBUICAO()
    elif tipo_algoritmo == "2":
        backt_VerAd = backtVerAd()
        resultadoSudoku = backt_VerAd.resolver_sudoku(sudoku_entrada)
        TENTATIVA_ATRIBUICAO = backt_VerAd.get_TENTATIVA_ATRIBUICAO()
    elif tipo_algoritmo == "3":
        backtVerAd_MinVal = backtVerAdMinVal()
        resultadoSudoku = backtVerAd_MinVal.resolver_sudoku(sudoku_entrada)
        TENTATIVA_ATRIBUICAO = backtVerAd_MinVal.get_TENTATIVA_ATRIBUICAO()
    return resultadoSudoku, TENTATIVA_ATRIBUICAO    

#-----Lendo o uma posição do sudoku, se for 0 substitui por um valor válido"----#
def read(sudoku):
        posicao = deepcopy(sudoku)
        for i in range(9):
            for j in range(9):
                cell = posicao[i][j]
                if cell == 0:
                    posicao[i][j] = buscar_valores_validos(sudoku, i, j)
        return posicao

#-----Encontrando valores válidos- Linha, coluna, quadro) ----#
def buscar_valores_validos (sudoku, i, j):
        initialSet = set(range(1, 10))
        for coluna in range(0, 9):
            if sudoku[i][coluna] in initialSet:
                initialSet.remove(sudoku[i][coluna])
        for linha in range(0, 9):
            if sudoku[linha][j] in initialSet:
                initialSet.remove(sudoku[linha][j])
        secTopX, secTopY = 3 * (i/3), 3 * (j/3)
        for x in range(secTopX, secTopX+3):
            for y in range(secTopY, secTopY+3):
                if sudoku[x][y] in initialSet:
                    initialSet.remove(sudoku[x][y])
        return initialSet

#----Verificação dos possiveis valores válidos- Linha, coluna, quadro)- para backtVerAd  e backtVerAdMinVal #
        
def valida_nova_atribuicao( elemento, i, j, pretendente):
        # Verificação linha, coluna, grupo
        linha = all([pretendente != elemento[i][x] for x in range(9)])
        if linha is True:
            coluna = all([pretendente != elemento[x][j] for x in range(9)])
            if coluna is True:
                # validação do quadro que o elemento pertence
                secTopX, secTopY = 3 * (i/3), 3 * (j/3)
                for x in range(secTopX, secTopX+3):
                    for y in range(secTopY, secTopY+3):
                        if elemento[x][y] == pretendente:
                            return False
            else:
                return False
        else:
            return False

         # verifição adiante na coluna
        for coluna in range(0, 9):
            if coluna == j:
                continue
            if type(elemento[i][coluna]) is set:
                if pretendente in elemento[i][coluna] and \
                        len(elemento[i][coluna]) == 1:

                    return False
         # verifição adiante na linha
        for linha in range(0, 9):
            if linha == i:
                continue
            if type(elemento[linha][j]) is set:
                if pretendente in elemento[linha][j] and \
                        len(elemento[linha][j]) == 1:

                    return False
     # verifição adiante no quadro eixo X e Y
        secTopX, secTopY = 3 * (i/3), 3 * (j/3)
        for x in range(secTopX, secTopX+3):
            for y in range(secTopY, secTopY+3):
                if x == i and y == j:
                    continue
                if type(elemento[x][y]) is set:
                    if pretendente in elemento[x][y] and \
                            len(elemento[x][y]) == 1:
                        return False
        return True

#-----Se a função #
def atualizar_valores( elemento, i, j, pretendente):
        i_alterado = []
        j_alterado= []
        #atualizar valores da coluna
        for coluna in range(0, 9):
            if coluna == j:
                continue
            if type(elemento[i][coluna]) is set:
                if pretendente in elemento[i][coluna]:
                    elemento[i][coluna].remove(pretendente)
                    i_alterado.append(i)
                    j_alterado.append(coluna)
        #atualizar valores da linha 
        for linha in range(0, 9):
            if linha == i:
                continue
            if type(elemento[linha][j]) is set:
                if pretendente in elemento[linha][j]:
                    elemento[linha][j].remove(pretendente)
                    i_alterado.append(linha)
                    j_alterado.append(j)
        #atualizar valores da coluna
        secTopX, secTopY = 3 * (i/3), 3 * (j/3)
        for x in range(secTopX, secTopX+3):
            for y in range(secTopY, secTopY+3):
                if x == i and y == j:
                    continue
                if type(elemento[x][y]) is set:
                    if pretendente in elemento[x][y]:
                        elemento[x][y].remove(pretendente)
                        i_alterado.append(x)
                        j_alterado.append(y)
        return i_alterado, j_alterado


def restore_values( elemento, i_alterado, j_alterado, pretendente):
        for item in range(0, len(i_alterado)):
            elemento[i_alterado[item]][j_alterado[item]].add(pretendente)


def mostrarSudoku(sudoku):
    return ('\n'.join([''.join(['{:1} '.format(item) for item in linha])
            for linha in sudoku])+'\n')


                #-----------------BACKTRACKING SIMPLES--------------------------------#
class backtSimples():
    def __init__(self, lp=1000000, ta=0):
        self.LIMITE_PARADA = lp
        self.TENTATIVA_ATRIBUICAO = ta
    def get_TENTATIVA_ATRIBUICAO(self):
        return self.TENTATIVA_ATRIBUICAO

 #--Função para encontrar espaço que possa ser preenchido por um novo valor (espaco em branco==0)--#
    def buscar_prox_pos(self, elemento, i, j):
        for l in range(0, 9):
            for c in range(0, 9):
                if elemento[l][c] == 0:
                    return l, c
        return -1, -1

    #--Função de verificar  se o elemento atribuito(randomico) é valido --#
    def validar_novo_elemento(self, elemento, i, j, pretendente):
        linha = all([pretendente != elemento[i][x] for x in range(9)])
        if linha is True:
            coluna = all([pretendente != elemento[x][j] for x in range(9)])
            if coluna is True:
                #buscar valores na diagonal, quadrado!
                secTopX, secTopY = 3 * (i/3), 3 * (j/3)
                for x in range(secTopX, secTopX+3):
                    for y in range(secTopY, secTopY+3):
                        if elemento[x][y] == pretendente:
                            return False
                return True
        return False

    #--Função de recursão do BACKTRACKING sem heuristica--#
    def backt_simple_recursao(self, elemento, i=0, j=0):

        i, j = self.buscar_prox_pos(elemento, i, j)

        if i == -1:
            return True

        for pretendente in range(1, 10):
            if self.validar_novo_elemento(elemento, i, j, pretendente) is True:
                if self.TENTATIVA_ATRIBUICAO > self.LIMITE_PARADA:
                    print "Numero de atribuições excede limite máximo \n",
                    raise ValueError("Numero de atribuições excede limite máximo",  self.TENTATIVA_ATRIBUICAO)
                elemento[i][j] = pretendente
                self.TENTATIVA_ATRIBUICAO += 1
                if self.backt_simple_recursao(elemento, i, j) is True:
                    return True
                elemento[i][j] = 0
        return None


    def read(self, sudokuCSP):
        state = deepcopy(sudokuCSP)

        return state    


    def resolver_soduko(self, sudoku):
        state = self.read(sudoku)
        # print state
        self.backt_simple_recursao(state)
        # print state
        return state

 #---------------------------Backtracking + verificação adiante-----------------------------#
class backtVerAd():
    def __init__(self, lp=1000000, ta=0):
        self.LIMITE_PARADA = lp
        self.TENTATIVA_ATRIBUICAO = ta

    def get_TENTATIVA_ATRIBUICAO(self):
        return self.TENTATIVA_ATRIBUICAO

    def buscar_prox_espaco_preencher(self, elemento, i, j):
        for x in range(0, 9):
            for y in range(0, 9):
                if type(elemento[x][y]) is set:
                    return x, y

        return -1, -1

    def recursao_backt(self, elemento, i=0, j=0):

        i, j = self.buscar_prox_espaco_preencher(elemento, i, j)

        if i == -1:
            return True
        rangeValues = elemento[i][j]
        for valor_pretendente in rangeValues:
            if valida_nova_atribuicao(elemento, i, j, valor_pretendente) is True:
                if self.TENTATIVA_ATRIBUICAO > self.LIMITE_PARADA:
                    print "Numero de atribuições excede limite máximo \n",
                    raise ValueError("Numero de atribuicoes excede limite maximo",  self.TENTATIVA_ATRIBUICAO)
                elemento[i][j] = valor_pretendente
                i_alterado, j_alterado= atualizar_valores(elemento,
                                                            i,
                                                            j,
                                                            valor_pretendente)
                self.TENTATIVA_ATRIBUICAO += 1
               


                if self.recursao_backt(elemento, i, j) is True:
                    return True
                elemento[i][j] = rangeValues
                restore_values(elemento,
                                    i_alterado,
                                    j_alterado,
                                    valor_pretendente)
        return None

    def resolver_sudoku(self, sudoku):
        """ resolver_sudoku sudoku """
        state = read(sudoku)
        # print state
        self.recursao_backt(state)
        # print state
        return state

    #----------------------------Backtracking + verificação adiante + mínimos valores remanescentes -------------------------------#

class backtVerAdMinVal():
    def __init__(self, lp=1000000, ta=0):
        self.LIMITE_PARADA = lp
        self.TENTATIVA_ATRIBUICAO = ta

    def get_TENTATIVA_ATRIBUICAO(self):
        return self.TENTATIVA_ATRIBUICAO
    #--- Aqui que diferencia do "verificação adiante, primeiro ele cria uma lista de valores possiveis para cada elemento
    # E atribui  ao elemento que contem valores possiveis minimos"
    def prox_espaco_preencher_Min(self, elemento, i, j):
        cell = {}
        cell["x"] = 0
        cell["y"] = 0
        cell["set"] = set()
        first = True
        for x in range(0, 9):
            for y in range(0, 9):
                if type(elemento[x][y]) is set:
                    if first is True:
                        cell["x"] = x
                        cell["y"] = y
                        cell["set"] = elemento[x][y]
                        first = False
                    else:
                        if len(elemento[x][y]) < len(cell["set"]):
                            cell["x"] = x
                            cell["y"] = y
                            cell["set"] = elemento[x][y]
                        elif len(elemento[x][y]) == len(cell["set"]):
                            pass

        if len(cell["set"]) > 0:
            return cell["x"], cell["y"]

        return -1, -1

    #--- Mesma função Backtracking, se diferencia porque recebe o parametro da função"prox_espaco_preencher_Min" que são a lista dos valores mininos"
    def recursao_backt(self, elemento, i=0, j=0):

        i, j = self.prox_espaco_preencher_Min(elemento, i, j)

        if i == -1:
            return True

        rangeValues = elemento[i][j]
        for valor_pretendente in rangeValues:
            if valida_nova_atribuicao(elemento, i, j, valor_pretendente) is True:
                if self.TENTATIVA_ATRIBUICAO > self.LIMITE_PARADA:
                    print "Numero de atribuições excede limite máximo\n",
                    raise ValueError("Numero de atribuicoes excede limite maximo",  self.TENTATIVA_ATRIBUICAO)
                elemento[i][j] = valor_pretendente
                i_alterado, j_alterado= atualizar_valores(elemento,
                                                            i,
                                                            j,
                                                            valor_pretendente)
                self.TENTATIVA_ATRIBUICAO += 1

                if self.recursao_backt(elemento, i, j) is True:
                    return True
                elemento[i][j] = rangeValues
                restore_values(elemento,
                                    i_alterado,
                                    j_alterado,
                                    valor_pretendente)
        return None

    def resolver_sudoku(self, sudoku):
        state = read(sudoku)
        self.recursao_backt(state)
        return state


     #--------------------------------------------Main - Leitura - Escrita  Arquivo-----------------------------------------#

def main(argv):
    
    nome_arquivo_ = None
    tipo_op = None
    try:
        opts, args = getopt.getopt(argv,"hi:t:",["nomearquivo=","tipoop="])
    except getopt.GetoptError:
        print 'solveSudoku.py -i <nomearquivo> -t <tipooperacao>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'solveSudoku.py -i <nomearquivo> -t <tipooperacao>'
            sys.exit()
        elif opt in ("-i", "--in"):
            nome_arquivo_ = arg
        elif opt in ("-t", "--tipo"):
            tipo_op = arg
    
    if nome_arquivo_ is None or tipo_op is None:
        print "solveSudoku.py -i <nomearquivo> -t <tipooperacao>"
        print "<tipooperacao>  (1, 2, 3)"
        print "1: para Backtracking sem Heuristica"
        print "2: para Backtracking com verificação Adiante"
        print "3: para Backtracking com verificação mais adiante e valores minimos remanescentes"

    nome_arquivo= "./"+str(nome_arquivo_)

    if tipo_op is not None and tipo_op == "2":
        arquivoResultados = open("./Analise/backt_VerificacaoAdiante.csv", "wa")
    elif tipo_op is not None and tipo_op == "3":
        arquivoResultados = open("./Analise/backt_VerificacaoAdiante_ValoresMinimos.csv", "wa")
    elif tipo_op is not None and tipo_op == "1":
        arquivoResultados = open("./Analise/backt_SemHeuristica.csv", "wa")
    else:
        sys.exit(2)
    
    w = unicodecsv.writer(arquivoResultados,
                          encoding='UTF-8',
                          delimiter=';',
                          quotechar='"',
                          quoting=csv.QUOTE_ALL)
    w.writerow(["TENTATIVA_ATRIBUICAO", "TEMPO"])

                 #-----Lendo entrada  do arquivo---#
    arquivoSudoku = open(nome_arquivo, "r")
    numero_teste = arquivoSudoku.readline()
    numero_teste = int(numero_teste)
    sudokus = []
    for x in range(0, numero_teste):
        entrada_sudoku = []
        for linha in arquivoSudoku:
            if linha != "\n":
                linha = linha.replace('\n', '')
                linha = linha.split(" ")
                linha = map(int, linha)
                entrada_sudoku.append(linha)
            else:
                sudokus.append(entrada_sudoku)
                entrada_sudoku = []
                break
    sudokus.append(entrada_sudoku)

    for sudoku_entrada in sudokus:
        try:
            start_time = time.clock()
            result, at = resolverSudoku(tipo_op, sudoku_entrada)
            elapsed_time = time.clock() - start_time
            if result is not None:
                w.writerow([at, elapsed_time])
                print mostrarSudoku(result)
            else:
         	print "Falhouuuu"
        except ValueError as error:
            elapsed_time = time.clock() - start_time
            w.writerow([error.args[1], elapsed_time])

if __name__ == "__main__":
      main(sys.argv[1:])
