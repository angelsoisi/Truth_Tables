# How to handle negation

import itertools
from tabulate import tabulate
from os import system,name
from time import sleep

import sys
def clear():
    if name=="nt":
        _=system("cls")

class Expression:
    #Class variables
    possibleKeys = ['p','q','r','s','t']
    symbolsList = ['~','^','v','>','<']
    values = [True, False]
    keys = []
    truthTableValues = []
    SubExpressionDict = dict()
    propositionsValues = dict()
    def __init__(self, expression):
        #Formatting expression to expected symbols
        expression = expression.lower()
        self.expression = expression
        # Creating truth values for each variable
        for i in Expression.possibleKeys:
            if (i in self.expression):
                self.keys.append(i)
        Expression.truthTableValues = list(itertools.product(Expression.values, repeat=len(self.keys)))
        for propositionIndex in range(len(self.keys)):
            propositionValuesList = []
            for row in self.truthTableValues:
                value = row[propositionIndex]
                propositionValuesList.append(value)
            self.propositionsValues[self.keys[propositionIndex]] = propositionValuesList
        self.analyzesubexpression(self.expression)
        '''
        (p>q)<>(~pvq)
        ~p
        (p>q)
        (~pvq)
        '''
        # Create truth table, each list is a row
        table = dict()
        table.update(self.propositionsValues)
        table.update(self.SubExpressionDict)
        '''
        header = self.keys
        for key in self.SubExpressionDict.keys():
            header.append(key)
        table = [header]
        for row in self.truthTableValues:
            table.append(row)
        table = self.truthTableValues
        '''
        print(tabulate(table, headers='keys'))


    def analyzesubexpression(self, expression):
        # Base case
        if len(expression) == 1 :
            if expression in self.possibleKeys:
                return "BaseCase"

        # Asumir que cada expresion son dos partes
        index = 0
        leftSubExpression = self.findSubExpression(expression[index:])
        offset = len(leftSubExpression)
        index += offset
        if index >= len(expression):
            return
        # Find symbol
        if expression[index] == '<':
            symbol = "<>"
            index += 2
        else:
            symbol = expression[index]
            index +=1
        rightSubExpression = self.findSubExpression(expression[index:])

        # Find negation
        self.findnegation(leftSubExpression)
        self.findnegation(rightSubExpression)

        # Check if each expresion is a single proposition
        if leftSubExpression in self.keys:
            leftPropValues = self.propositionsValues[leftSubExpression]
        elif leftSubExpression in self.SubExpressionDict:
            leftPropValues = self.SubExpressionDict.get(leftSubExpression)
        else:
            if leftSubExpression[0] == '(' and leftSubExpression[len(leftSubExpression) -1] == ')':
                self.analyzesubexpression(leftSubExpression[1:len(leftSubExpression) -1])
            else:
                self.analyzesubexpression(leftSubExpression)
            leftPropValues = self.SubExpressionDict.get(leftSubExpression)

        if rightSubExpression in self.keys:
            rightPropValues = self.propositionsValues[rightSubExpression]
        elif rightSubExpression in self.SubExpressionDict:
            rightPropValues = self.SubExpressionDict.get(rightSubExpression)
        else:
            if rightSubExpression[0] == '(' and rightSubExpression[len(rightSubExpression) -1] == ')':
                self.analyzesubexpression(rightSubExpression[1:len(rightSubExpression) -1])
            else:
                self.analyzesubexpression(rightSubExpression)
            rightPropValues = self.SubExpressionDict.get(rightSubExpression)

        if leftPropValues == None or rightPropValues == None:
            print("Error")
            return

        resultsList = []
        for rowIndex in range(len(leftPropValues)):
            leftValue = leftPropValues[rowIndex]
            rightValue = rightPropValues[rowIndex]
            result = "error"
            # Conjunción
            if symbol == '^':
                result = leftValue and rightValue
            # Disyunción
            elif symbol == 'v':
                result = leftValue or rightValue
            # implicacion
            elif symbol == '>':
                result = not(leftValue) or rightValue
            # bicondicional, doble implicacion
            elif symbol == '<>':
                result = (leftValue and rightValue) or not (leftValue or rightValue)
            else:
                print("Symbol not found, error")
            resultsList.append(result)
        # Add parenthesis?
        self.SubExpressionDict['(' + expression + ')'] = resultsList

    def findnegation(self, expression):
        if expression[0] == '~':
            subexpresssion = expression[1:]
            hasParenthesis = False
            if subexpresssion[0] == '(' and expression[len(expression) -1] == ')':
                subexpresssion = subexpresssion[1:len(expression) -2]
                hasParenthesis = True
            if subexpresssion in self.possibleKeys:
                #index = self.keys.index(subexpresssion)
                subexpresssionList = self.propositionsValues[subexpresssion]
            else:
                self.analyzesubexpression(subexpresssion)
                if hasParenthesis:
                    subexpresssionList = self.SubExpressionDict.get('('+subexpresssion+')')
                else:
                    subexpresssionList = self.SubExpressionDict.get(subexpresssion)
            resultsList = []
            for value in subexpresssionList:
                resultsList.append(not(value))
            if hasParenthesis:
                subexpresssion = '(' + subexpresssion + ')'
            self.SubExpressionDict['~' + subexpresssion] = resultsList



    def findSubExpression(self, expression):
        index = 0
        leftParenthesisno = 0
        insideParenthesis = False
        while (index < len(expression)):
            char = expression[index]
            if char == '~':
                index += 1
                continue
            elif char in self.symbolsList:
                if not(insideParenthesis):
                    return expression[:index]
            elif char == '(':
                insideParenthesis = True
                leftParenthesisno += 1
            elif char == ')':
                if leftParenthesisno == 1:
                    return expression[:index + 1]
                else:
                    leftParenthesisno -= 1
            #elif leftParenthesisno == 0:
            #    if char not in possibleKeys:
            #        return expression[:index + 1]
            index += 1
        return expression
import sys
#bloque union
def Union_a_b(a,b):

    final_list = sorted(list(set(a) | set(b)))
    return final_list


def Union_b_c(b,c):

    final_list = sorted(list(set(b) | set(c)))
    return final_list


def Union_a_c(a,c):

    final_list = sorted(list(set(a) | set(c)))
    return final_list


def Union_a_byc(a,b,c):

    first = sorted(list(set(b) | set(c)))
    final_list=sorted(list(set(a) | (set(first))))
    return final_list
#bloque interseccion

def interseccion_a_b(a,b):
    result = [i for i in a if i in b]
    return result


def interseccion_b_c(b,c):
    result = [i for i in b if i in c]
    return result



def interseccion_a_c(a,c):
    result = [i for i in a if i in c]
    return result

def interseccion_a_byc(a,b,c):
    result = [i for i in b if i in c]
    results=[i for i in a if i in result]
    return results

#bloque diferencia
def diferencia_a_b(a,b):
    liston=list(set(a) - set(b))
    return liston



def diferencia_b_c(b,c):
    liston=list(set(b) - set(c))
    return liston



def diferencia_a_c(a,c):
    liston=list(set(a) - set(c))
    return liston
#bloque diferencia simetrica
def diferencia_simetrica_a_b(a,b):
    sym=sorted(list(set(a).symmetric_difference(set(b))))
    return sym

def diferencia_simetrica_b_c(b,c):
    sym=sorted(list(set(b).symmetric_difference(set(c))))
    return sym


def diferencia_simetrica_a_c(a,c):
    sym=sorted(list(set(a).symmetric_difference(set(c))))
    return sym

def start1():
    a = input("introduce los elementos para tu conjunto (A) separados por espacio:")
    a = a.split()
    b = input("introduce los elementos para tu conjunto (B) separados por espacio:")
    b = b.split()
    c = input("introduce los elementos para tu conjunto (C) separados por espacio:")
    c = c.split()
    print("La cardinalidad de A es",len(set(a)))
    print("La cardinalidad de B es", len(set(b)))
    print("La cardinalidad de C es", len(set(c)))
    print('operaciones sobre conjuntos')
    print("4. Uniones")
    print("5 interseccion")
    print("6 diferencia")
    print("7 diferencia simetrica")
    print("8 Salir del menu")
    choice2=input("Introduce la opcion que quieres: ")
    if choice2=="4":
        print("\t Uniones")
        print("\t que operacion quieres usar: ")
        print("\t 1. A u B")
        print("\t 2. B u C")
        print("\t 3. A u C")
        print("\t 4. A u (B u C)")
        choice3 = input("introduce el numero de la operacion: ")
        if choice3 == "1":
            print(Union_a_b(a, b))
        if choice3 == "2":
            print(Union_b_c(b, c))
        if choice3 == "3":
            print(Union_a_c(a, c))
        if choice3 == "4":
            print(Union_a_byc(a, b, c))
    if choice2 == "5":
        print("\t interseccion")
        print("\t que operacion quieres usar: ")
        print("\t 1. A ∩ B")
        print("\t 2. B ∩ C")
        print("\t 3. A ∩ C")
        print("\t 4. A ∩ (B ∩ C)")
        choice4 = input("introduce el numero de la operacion: ")
        if choice4 == "1":
            print(interseccion_a_b(a, b))
        if choice4 == "2":
            print(interseccion_b_c(b, c))
        if choice4 == "3":
            print(interseccion_a_c(a, c))
        if choice4 == "4":
            print(interseccion_a_byc(a, b, c))
    if choice2 == "6":
        print("\t diferencias")
        print("\t que operacion quieres usar: ")
        print("\t 1. A - B")
        print("\t 2. B - C")
        print("\t 3. A - C")
        choice5 = input("introduce el numero de la operacion: ")
        if choice5 == "1":
            print(diferencia_a_b(a, b))
        if choice5 == "2":
            print(diferencia_b_c(b, c))
        if choice5 == "3":
            print(diferencia_b_c(a, c))
    if choice2 == "7":
        print("\t diferencia simetrica")
        print("\t que operacion quieres usar: ")
        print("\t 1. A Δ B")
        print("\t 2. B Δ C")
        print("\t 3. A Δ C")
        choice6 = input("introduce el numero de la operacion: ")
        if choice6 == "1":
            print(diferencia_simetrica_a_b(a, b))
        if choice6 == "2":
            print(diferencia_simetrica_a_c(b, c))
        if choice6 == "3":
            print(diferencia_simetrica_a_c(a, c))
    if choice2=="8":
        start()


def instrucciones():
    print("bienvenido al generador de tablas de verdad")
    print("Tienes los siguientes simbolos a tu disposicion")
    print("'~', '^', 'v', '>', '<'")
    print("si gustas usar de la bicondicional se emplea de la siguiente forma")
    print("p<>q")
    print("puedes usar las letras desde la p hasta la z")
    print("excepctuando la v")

def start():
    # Use a breakpoint in the code line below to debug your script.
    print('Inicio de programa')
    print("generador de tablas de verdad")
    print("-" * 50)
    print("1. ver instrucciones para uso")
    print("2. crear una tabla de verdad")
    print("3. teoria de conjuntos")
    print("4. salir")
    choice=input("Introduce la opcion que quieres.")
    if choice=="1":
        instrucciones()
    elif choice=="2":
        expression = input("Introduce tu enunciado: ")
        expressionObject = Expression(expression)
    elif choice=="3":
        start1()
    elif choice=="4":
     sys.exit()



     print("Fin de la tabla")
    sleep(6)
    clear()
    start()

if __name__ == '__main__':
    start()

