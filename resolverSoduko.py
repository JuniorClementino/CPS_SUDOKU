#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import unicodecsv
import csv
import time
from copy import deepcopy


def mostrar_ajuda():
    print "solveSudoku.py -i <nomearquivo> -t <tipooperacao>"
    print "<tipooperacao>  (1, 2, 3)"
    print "1: para Backtracking sem Heuristica"
    print "2: para Backtracking com verificação Adiante"
    print "3: para Backtracking com verificação mais adiante e valores minimos remanescentes"
    

def resolverSudoku(tipo_algoritmo, sudoku_entrada):
    resultadoSudoku = sudoku_entrada
  
    if tipo_algoritmo == "1": # Sem Heuristica
        backt_Simples= backtSimples()
        resultadoSudoku= backt_Simples.resolver_soduko(sudoku_entrada)
        numero_atribuicao = backt_Simples.get_numero_atribuicao()

    elif tipo_algoritmo == "2": # Heuristica verificação adiante
        back_ver = backtEmComum()
        resultadoSudoku, numero_atribuicao = resolver_back_ver_adiante(sudoku_entrada)
        
    elif tipo_algoritmo == "3": # Heuristica Ver Ad e Valores mininos
        back_ver_min = backtEmComum()
        resultadoSudoku, numero_atribuicao = resolver_back_valores_Min(sudoku_entrada)

    return resultadoSudoku, numero_atribuicao    


#-- Funções semelhantes para Backtracking Verificação adiante e Valores minimos-----#

#-----Lendo o uma posição do sudoku, se for 0 substitui por um valor válido"----#
def verifica_pos_vazia_e_troca_valorValido(sudoku):
        posicao = deepcopy(sudoku)
        for i in range(9):
            for j in range(9):
                celula = posicao[i][j]
                if celula == 0:
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
        top_x, top_y = 3 * (i/3), 3 * (j/3)
        for x in range(top_x, top_x+3):
            for y in range(top_y, top_y+3):
                if sudoku[x][y] in initialSet:
                    initialSet.remove(sudoku[x][y])
        return initialSet

#----Verificação dos possiveis valores válidos- Linha, coluna, quadro)- para backtVerAd e backtVerAdMinVal #
        
def valida_nova_atribuicao( elemento, i, j, pretendente):
        # Verificação linha, coluna, grupo
        linha = all([pretendente != elemento[i][x] for x in range(9)])
        if linha is True:
            coluna = all([pretendente != elemento[x][j] for x in range(9)])
            if coluna is True:
                # validação do quadro que o elemento pertence
                top_x, top_y = 3 * (i/3), 3 * (j/3)
                for x in range(top_x, top_x+3):
                    for y in range(top_y, top_y+3):
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
        top_x= 3 * (i/3)
        top_y = 3 * (j/3)
        for x in range(top_x, top_x+3):
            for y in range(top_y, top_y+3):
                if x == i and y == j:
                    continue
                if type(elemento[x][y]) is set:
                    if pretendente in elemento[x][y] and \
                            len(elemento[x][y]) == 1:
                        return False
        return True

#-----Se a função "valida_nova_atribuicao" retorna TRUE#
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
        top_x, top_y = 3 * (i/3), 3 * (j/3)
        for x in range(top_x, top_x+3):
            for y in range(top_y, top_y+3):
                if x == i and y == j:
                    continue
                if type(elemento[x][y]) is set:
                    if pretendente in elemento[x][y]:
                        elemento[x][y].remove(pretendente)
                        i_alterado.append(x)
                        j_alterado.append(y)
        return i_alterado, j_alterado

def recuperar_valores( elemento, i_alterado, j_alterado, pretendente):
        for item in range(0, len(i_alterado)):
            elemento[i_alterado[item]][j_alterado[item]].add(pretendente)

def mostrarSudoku(sudoku):
    return ('\n'.join([''.join(['{:1} '.format(item) for item in linha])
            for linha in sudoku])+'\n')



                #-----------------BACKTRACKING SIMPLES--------------------------------#
class backtSimples():

        #--Função de recursão do BACKTRACKING sem heuristica--#
    def backt_simple_recursao(self, elemento, i=0, j=0):
        i, j = self.buscar_prox_pos(elemento, i, j)
        if i == -1:
            return True

        for pretendente in range(1, 10):
            if self.validar_novo_elemento(elemento, i, j, pretendente) is True:
                if self.numero_atribuicao > self.atribuicao_max:
                    print "Numero de atribuições excede limite máximo \n",
                    raise ValueError(" ",  self.numero_atribuicao)
                elemento[i][j] = pretendente
                self.numero_atribuicao += 1
                if self.backt_simple_recursao(elemento, i, j) is True:
                    return True
                elemento[i][j] = 0
        return None

 #--Função para encontrar espaço que possa ser preenchido por um novo valor(espaco em branco==0)--#
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
                top_x = 3 * (i/3)
                top_y = 3 * (j/3)
                for x in range(top_x, top_x+3):
                    for y in range(top_y, top_y+3):
                        if elemento[x][y] == pretendente:
                            return False
                return True
        return False

    def __init__(self, at_max=1000000, num_at=0):
        self.atribuicao_max = at_max
        self.numero_atribuicao = num_at
    def get_numero_atribuicao(self):
        return self.numero_atribuicao

    def read(self, sudokuCSP):
        sudoku = deepcopy(sudokuCSP)
        return sudoku    

    def resolver_soduko(self, sudoku):
        sudoku = self.read(sudoku)
        self.backt_simple_recursao(sudoku)
        return sudoku
 #---------------------------Backtracking + verificação adiante-----------------------------#
def resolver_back_ver_adiante(sudoku):
    sudoku= verifica_pos_vazia_e_troca_valorValido(sudoku)
    back = backtEmComum()
    back.recursao_backt(sudoku,0,0,"verificacao_adiante")
    numero_atribuicao= back.get_numero_atribuicao()
    return sudoku, numero_atribuicao

    #Funçaõ exclusiva para verificacao adiante-Preparando valores (adiante) para entrar no backtraking#
def veri_adiante_buscar_prox_espaco_preencher(elemento, i, j):
        for x in range(0, 9):
            for y in range(0, 9):
                if type(elemento[x][y]) is set:
                    return x, y

        return -1, -1

#----------------------------Backtracking + verificação adiante + mínimos valores remanescentes -------------------------------#
def resolver_back_valores_Min(sudoku):
    sudoku= verifica_pos_vazia_e_troca_valorValido(sudoku)
    back = backtEmComum()
    back.recursao_backt(sudoku,0,0,"verificacao_adiante_val_min")
    numero_atribuicao= back.get_numero_atribuicao()
    return sudoku, numero_atribuicao

    #Funçaõ exclusiva para valores minimos- Preparando valores (valoresMinimos) antes de  entrar no backtraking#
def prox_espaco_preencher_Min(elemento, i, j):
        celula = {}
        celula["x"] = 0
        celula["y"] = 0
        celula["pos"] = set()
        incial = True
        for x in range(0, 9):
            for y in range(0, 9):
                if type(elemento[x][y]) is set:
                    if incial is True:
                        celula["x"] = x
                        celula["y"] = y
                        celula["pos"] = elemento[x][y]
                        incial = False
                    else:
                        if len(elemento[x][y]) < len(celula["pos"]):
                            celula["x"] = x
                            celula["y"] = y
                            celula["pos"] = elemento[x][y]
                        elif len(elemento[x][y]) == len(celula["pos"]):
                            pass

        if len(celula["pos"]) > 0:
            return celula["x"], celula["y"]

        return -1, -1 
        
#---Classe Backtracking em comum para ser utilazdo na verificação adiante e nos valores minimos---#
class backtEmComum():
    def recursao_backt(self, elemento, i=0, j=0, heuristica=""):
    # - recursão para verificação adiante- #    
        if heuristica == 'verificacao_adiante':
            i, j = veri_adiante_buscar_prox_espaco_preencher(elemento, i, j)
    # - recursão para verificação adiante- # 
        elif heuristica == 'verificacao_adiante_val_min':
            i, j = prox_espaco_preencher_Min(elemento,i,j)
            
        if i == -1:
            return True

        rangeValues = elemento[i][j]
        for valor_pretendente in rangeValues:
            if valida_nova_atribuicao(elemento, i, j, valor_pretendente) is True:
                if self.numero_atribuicao > self.atribuicao_max:
                    print "Numero de atribuições excede limite máximo \n",
                    raise ValueError("",  self.numero_atribuicao)
                elemento[i][j] = valor_pretendente
                i_alterado, j_alterado= atualizar_valores(elemento,i,j,valor_pretendente)
                self.numero_atribuicao += 1
               
                if self.recursao_backt(elemento, i, j,heuristica) is True:
                    return True
                elemento[i][j] = rangeValues
                recuperar_valores(elemento,i_alterado,j_alterado,valor_pretendente)
        return None

    def __init__(self, at_max=1000000, num_at=0):
        self.atribuicao_max = at_max
        self.numero_atribuicao = num_at
    def get_numero_atribuicao(self):
        return self.numero_atribuicao
 #---------------------------------Flags------Main - Leitura - Escrita - Arquivo-----------------------------------------#        
def conf_flag(argv):
    nome_arquivo_ = None
    tipo_op = None
    try:
        opts, args = getopt.getopt(argv,"hi:t:",["nomearquivo=","tipoop="])
    except getopt.GetoptError:
        #print 'solveSudoku.py -i <nomearquivo> -t <tipooperacao>'
        mostrar_ajuda()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'solveSudoku.py -i <nomearquivo> -t <tipooperacao>'
            sys.exit()
        elif opt in ("-i", "--in"):
            nome_arquivo_ = arg
        elif opt in ("-t", "--tipo"):
            tipo_op = arg

    return tipo_op,nome_arquivo_
def ler_arquivo_chamar_metodo ():
    tipo_op,nome_arquivo_ = conf_flag(sys.argv[1:])
    if nome_arquivo_ is None or tipo_op is None:
        mostrar_ajuda()
    nome_arquivo= "./"+str(nome_arquivo_)
    arquivoResultados=abrir_arquivo(tipo_op)
    
    w = unicodecsv.writer(arquivoResultados,encoding='UTF-8',delimiter=';',quotechar='"',quoting=csv.QUOTE_ALL)
    w.writerow(["numero_atribuicao", "tempo_gasto"])

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
            tempo_inicio = time.clock()
            # chamando e mostrando resultado final #
            resultado, atribuicoes = resolverSudoku(tipo_op, sudoku_entrada)
            tempo_final = time.clock() - tempo_inicio
            if resultado is not None:
                w.writerow([atribuicoes, tempo_final])
                print mostrarSudoku(resultado)
            else:
                print "Falhouuuu"
        except ValueError as error:
            tempo_final = time.clock() - tempo_inicio
            w.writerow([error.args[1], tempo_final])

def abrir_arquivo(tipo_op):
    if tipo_op is not None and tipo_op == "2":
        arquivoResultados = open("./backt_VerificacaoAdiante.csv", "wa")
    elif tipo_op is not None and tipo_op == "3":
        arquivoResultados = open("./backt_VerificacaoAdiante_ValoresMinimos.csv", "wa")
    elif tipo_op is not None and tipo_op == "1":
        arquivoResultados = open("./backt_SemHeuristica.csv", "wa")  
    else:
        sys.exit(2)
    return arquivoResultados 

def main():
    ler_arquivo_chamar_metodo()
if __name__ == "__main__":
    main()