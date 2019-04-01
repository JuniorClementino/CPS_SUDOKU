#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import unicodecsv
import csv
import time
from copy import deepcopy

def atualizar_valores( assignment, i, j, pretendente):
        i_alterado = []
        j_alterado= []
        for coluna in range(0, 9):
            if coluna == j:
                continue
            if type(assignment[i][coluna]) is set:
                if pretendente in assignment[i][coluna]:
                    assignment[i][coluna].remove(pretendente)
                    i_alterado.append(i)
                    j_alterado.append(coluna)

        for linha in range(0, 9):
            if linha == i:
                continue
            if type(assignment[linha][j]) is set:
                if pretendente in assignment[linha][j]:
                    assignment[linha][j].remove(pretendente)
                    i_alterado.append(linha)
                    j_alterado.append(j)

        secTopX, secTopY = 3 * (i/3), 3 * (j/3)
        for x in range(secTopX, secTopX+3):
            for y in range(secTopY, secTopY+3):
                if x == i and y == j:
                    continue
                if type(assignment[x][y]) is set:
                    if pretendente in assignment[x][y]:
                        assignment[x][y].remove(pretendente)
                        i_alterado.append(x)
                        j_alterado.append(y)
        return i_alterado, j_alterado
def is_valid( assignment, i, j, pretendente):
        # Verificação linha, coluna, grupo
        linha = all([pretendente != assignment[i][x] for x in range(9)])
        if linha is True:
            coluna = all([pretendente != assignment[x][j] for x in range(9)])
            if coluna is True:
                # finding the top left x,y
                # co-ordinates of the section containing the i,j cell
                secTopX, secTopY = 3 * (i/3), 3 * (j/3)
                for x in range(secTopX, secTopX+3):
                    for y in range(secTopY, secTopY+3):
                        if assignment[x][y] == pretendente:
                            return False
            else:
                return False
        else:
            return False

        # Verificação Adiante!
        for coluna in range(0, 9):
            if coluna == j:
                continue
            if type(assignment[i][coluna]) is set:
                if pretendente in assignment[i][coluna] and \
                        len(assignment[i][coluna]) == 1:

                    return False

        for linha in range(0, 9):
            if linha == i:
                continue
            if type(assignment[linha][j]) is set:
                if pretendente in assignment[linha][j] and \
                        len(assignment[linha][j]) == 1:

                    return False

        secTopX, secTopY = 3 * (i/3), 3 * (j/3)
        for x in range(secTopX, secTopX+3):
            for y in range(secTopY, secTopY+3):
                if x == i and y == j:
                    continue
                if type(assignment[x][y]) is set:
                    if pretendente in assignment[x][y] and \
                            len(assignment[x][y]) == 1:
                        return False
        return True

    
                #-----------------BACKTRACKING SIMPLES--------------------------------#


class backtSimples():
    def __init__(self, lp=1000000, ta=0):
        self.LIMITE_PARADA = lp
        self.TENTATIVA_ATRIBUICAO = ta

    def get_TENTATIVA_ATRIBUICAO(self):
        return self.TENTATIVA_ATRIBUICAO

    def find_next_cell_to_fill(self, assignment, i, j):

        for x in range(0, 9):
            for y in range(0, 9):
                if assignment[x][y] == 0:
                    return x, y

        return -1, -1

    def is_valid(self, assignment, i, j, pretendente):
        linha = all([pretendente != assignment[i][x] for x in range(9)])
        if linha is True:
            coluna = all([pretendente != assignment[x][j] for x in range(9)])
            if coluna is True:
                # finding the top left x,y
                # co-ordinates of the section containing the i,j cell
                secTopX, secTopY = 3 * (i/3), 3 * (j/3)
                for x in range(secTopX, secTopX+3):
                    for y in range(secTopY, secTopY+3):
                        if assignment[x][y] == pretendente:
                            return False
                return True
        return False

    # % returns a solution (True) or failure (None)
    def recursive_backtracking(self, assignment, i=0, j=0):

        i, j = self.find_next_cell_to_fill(assignment, i, j)

        if i == -1:
            return True

        for valor_pretendente in range(1, 10):
            if self.is_valid(assignment, i, j, valor_pretendente) is True:
                if self.TENTATIVA_ATRIBUICAO > self.LIMITE_PARADA:
                    raise ValueError("Numero de atribuicoes excede"
                                     " limite maximo",
                                     self.TENTATIVA_ATRIBUICAO)

                assignment[i][j] = valor_pretendente
                self.TENTATIVA_ATRIBUICAO += 1

                # sys.exit(0)
                if self.recursive_backtracking(assignment, i, j) is True:
                    return True
                assignment[i][j] = 0

        return None

    def read(self, sudoku):
        """ Read field into state (replace 0 with set of possible values) """
        state = deepcopy(sudoku)

        return state

    def solve(self, sudoku):
        """ Solve sudoku """
        state = self.read(sudoku)
        # print state
        self.recursive_backtracking(state)
        # print state
        return state

 #---------------------------Backtracking + verificação adiante-----------------------------#

class backtVerAd():
    def __init__(self, lp=1000000, ta=0):
        self.LIMITE_PARADA = lp
        self.TENTATIVA_ATRIBUICAO = ta

    def get_TENTATIVA_ATRIBUICAO(self):
        return self.TENTATIVA_ATRIBUICAO

    def find_next_cell_to_fill(self, assignment, i, j):

        for x in range(0, 9):
            for y in range(0, 9):
                if type(assignment[x][y]) is set:
                    return x, y

        return -1, -1



    def restore_values(self, assignment, i_alterado, j_alterado, pretendente):

        for item in range(0, len(i_alterado)):
            assignment[i_alterado[item]][j_alterado[item]].add(pretendente)
        
   
    # % returns a solution (True) or failure (None)
    def recursive_backtracking(self, assignment, i=0, j=0):

        i, j = self.find_next_cell_to_fill(assignment, i, j)

        if i == -1:
            return True

        rangeValues = assignment[i][j]
        for valor_pretendente in rangeValues:
            if is_valid(assignment, i, j, valor_pretendente) is True:
                if self.TENTATIVA_ATRIBUICAO > self.LIMITE_PARADA:
                    raise ValueError("Numero de atribuicoes excede"
                                     " limite maximo",
                                     self.TENTATIVA_ATRIBUICAO)
                assignment[i][j] = valor_pretendente
                i_alterado, j_alterado= atualizar_valores(assignment,
                                                            i,
                                                            j,
                                                            valor_pretendente)
                # print assignment
                self.TENTATIVA_ATRIBUICAO += 1

                # sys.exit(0)
                if self.recursive_backtracking(assignment, i, j) is True:
                    # print "FOI"
                    return True
                assignment[i][j] = rangeValues
                self.restore_values(assignment,
                                    i_alterado,
                                    j_alterado,
                                    valor_pretendente)

        return None

    def buscar_valores_validos(self, sudoku, i, j):
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

    def read(self, sudoku):
        """ Read field into state (replace 0 with set of possible values) """
        state = deepcopy(sudoku)
        for i in range(9):
            for j in range(9):
                cell = state[i][j]
                if cell == 0:
                    state[i][j] = self.buscar_valores_validos(sudoku, i, j)
        return state

    def solve(self, sudoku):
        """ Solve sudoku """
        state = self.read(sudoku)
        # print state
        self.recursive_backtracking(state)
        # print state
        return state



      
    #----------------------------Backtracking + verificação adiante + mínimos valores remanescentes -------------------------------#

    
class backtVerAdMinVal():
    def __init__(self, lp=1000000, ta=0):
        self.LIMITE_PARADA = lp
        self.TENTATIVA_ATRIBUICAO = ta

    def get_TENTATIVA_ATRIBUICAO(self):
        return self.TENTATIVA_ATRIBUICAO

    def find_next_cell_to_fill(self, assignment, i, j):
        cell = {}
        cell["x"] = 0
        cell["y"] = 0
        cell["set"] = set()
        first = True
        for x in range(0, 9):
            for y in range(0, 9):
                if type(assignment[x][y]) is set:
                    if first is True:
                        cell["x"] = x
                        cell["y"] = y
                        cell["set"] = assignment[x][y]
                        first = False
                    else:
                        if len(assignment[x][y]) < len(cell["set"]):
                            cell["x"] = x
                            cell["y"] = y
                            cell["set"] = assignment[x][y]
                        elif len(assignment[x][y]) == len(cell["set"]):
                            pass

        if len(cell["set"]) > 0:
            return cell["x"], cell["y"]

        return -1, -1


    def restore_values(self, assignment, i_alterado, j_alterado, pretendente):

        for item in range(0, len(i_alterado)):
            assignment[i_alterado[item]][j_alterado[item]].add(pretendente)

    
    def recursive_backtracking(self, assignment, i=0, j=0):

        i, j = self.find_next_cell_to_fill(assignment, i, j)

        if i == -1:
            return True

        rangeValues = assignment[i][j]
        for valor_pretendente in rangeValues:
            if is_valid(assignment, i, j, valor_pretendente) is True:
                if self.TENTATIVA_ATRIBUICAO > self.LIMITE_PARADA:
                    raise ValueError("Numero de atribuicoes excede"
                                     " limite maximo",
                                     self.TENTATIVA_ATRIBUICAO)
                assignment[i][j] = valor_pretendente
                i_alterado, j_alterado= atualizar_valores(assignment,
                                                            i,
                                                            j,
                                                            valor_pretendente)
                # print assignment
                self.TENTATIVA_ATRIBUICAO += 1

                # sys.exit(0)
                if self.recursive_backtracking(assignment, i, j) is True:
                    # print "FOI"
                    return True
                assignment[i][j] = rangeValues
                self.restore_values(assignment,
                                    i_alterado,
                                    j_alterado,
                                    valor_pretendente)

        return None

    def buscar_valores_validos(self, sudoku, i, j):
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

    def read(self, sudoku):
        """ Read field into state (replace 0 with set of possible values) """
        state = deepcopy(sudoku)
        for i in range(9):
            for j in range(9):
                cell = state[i][j]
                if cell == 0:
                    state[i][j] = self.buscar_valores_validos(sudoku, i, j)
        return state

    def solve(self, sudoku):
        """ Solve sudoku """
        state = self.read(sudoku)
        # print state
        self.recursive_backtracking(state)
        # print state
        return state




     #--------------------------------------------------------------------------------------------------------------------------------------------------#

    

def mostrarSudoku(sudoku):
    return ('\n'.join([''.join(['{:1} '.format(item) for item in linha])
            for linha in sudoku]))


def resolverSudoku(tipo_algoritmo, inputItem):
    resultadoSudoku = inputItem
    TENTATIVA_ATRIBUICAO = 0

    if tipo_algoritmo == "1":
        backt_Simples= backtSimples()
        resultadoSudoku= backt_Simples.solve(inputItem)
        TENTATIVA_ATRIBUICAO = backt_Simples.get_TENTATIVA_ATRIBUICAO()
    elif tipo_algoritmo == "2":
        backt_VerAd = backtVerAd()
        resultadoSudoku = backt_VerAd.solve(inputItem)
        TENTATIVA_ATRIBUICAO = backt_VerAd.get_TENTATIVA_ATRIBUICAO()
    elif tipo_algoritmo == "3":
        backtVerAd_MinVal = backtVerAdMinVal()
        resultadoSudoku = backtVerAd_MinVal.solve(inputItem)
        TENTATIVA_ATRIBUICAO = backtVerAd_MinVal.get_TENTATIVA_ATRIBUICAO()
    return resultadoSudoku, TENTATIVA_ATRIBUICAO

def menu_op():
    print "Bem vindo ao SUDOKO:  Escolha qual método deve ser utilizado para resolução do Sudoko"
    print "1 : Backtracking"
    print "2 : Verificação Adiante"
    print "3 : Verificação Adiante e MVR"
#-----------------------------------------------------------------------------------------------------------------------------------#



def main():
    menu_op()
    # -------------Menu e  escolha das operações (Flags) escolhidos-------------#
    cowmode = False
    tipo_operacao = None
    tipo_operacao = raw_input()

    if tipo_operacao is None:
        menu_op()
        sys.exit(2)

    # -------------- Arquivos de Resultados e análise de cada algoritmo----------#
    if tipo_operacao is not None and tipo_operacao == "2":
        arquivoResultados = open("./Resultados/backtVerAdi.csv", "wa")
    elif tipo_operacao is not None and tipo_operacao == "3":
        arquivoResultados = open("./Resultados/backtVerAdiMin.csv", "wa")
    elif tipo_operacao is not None and tipo_operacao == "1":
        arquivoResultados = open("./Resultados/backtSimples.csv", "wa")
    else:
        print("Digite uma opção válida (1, 2, ou 3)")
        sys.exit(2)
        

    w = unicodecsv.writer(arquivoResultados,
                          encoding='UTF-8',
                          delimiter=';',
                          quotechar='"',
                          quoting=csv.QUOTE_ALL)
    w.writerow(["TENTATIVA_ATRIBUICAO", "TEMPO"])


                 #-----Lendo e escolhendo o arquivo---#
    arquivoSudoku = open("./entrada1.txt", "r")
    primeiraLinha = arquivoSudoku.readline()
    primeiraLinha = int(primeiraLinha)
    inputSet = []
    for x in range(0, primeiraLinha):

        input = []
        for linha in arquivoSudoku:
            if linha != "\n":
                linha = linha.replace('\n', '')
                linha = linha.split(" ")
                linha = map(int, linha)
                input.append(linha)
            else:
                inputSet.append(input)
                # print "input"
                # print " "
                input = []
                break
    inputSet.append(input)

    

    # My code here
    for inputItem in inputSet:
       
        try:
            start_time = time.clock()
            result, at = resolverSudoku(tipo_operacao, inputItem)
            # resultadoSudoku = btClass.solve(inputItem)
            elapsed_time = time.clock() - start_time

            if result is not None:
                w.writerow([at, elapsed_time])

                if cowmode is True:
                    print cowsay.CowSay().cowsay(mostrarSudoku(result), 18)
                else:
                    print mostrarSudoku(result)
                print
            else:
                if cowmode is True:
                    print cowsay.CowSay().cowsay("MUHHH")
                else:
                    print "Failure"
        except ValueError as error:
            elapsed_time = time.clock() - start_time
            w.writerow([error.args[1], elapsed_time])
            if cowmode is True:
                print cowsay.CowSay().cowsay(str(error.args[0]))
            else:
                print(error.args[0])
                print

# start Sudoku Solver
if __name__ == "__main__":

    main()
