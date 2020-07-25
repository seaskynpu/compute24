#!/usr/bin/python3
# -*- coding: utf-8 -*-
from itertools import permutations, combinations




def compute24(combination):
    templates=["%d%s%d%s%d%s%d",
              "(%d%s%d)%s%d%s%d",
              "%d%s(%d%s%d)%s%d",
              "%d%s%d%s(%d%s%d)",
              "(%d%s%d%s%d)%s%d",
              "%d%s(%d%s%d%s%d)",
              "(%d%s%d)%s(%d%s%d)",
              "((%d%s%d)%s%d)%s%d",
              "(%d%s(%d%s%d))%s%d",
              "%d%s((%d%s%d)%s%d)",
              "%d%s(%d%s(%d%s%d))"]

    operators=["+","-","*","/"]
    count=0
    resultList=[]
    for numlist in list(permutations(combination)):
        for operator1 in operators:
            for operator2 in operators:
                for operator3 in operators:
                    for tmplate in templates:
                        count=count+1
                        expression=tmplate%(numlist[0],operator1,numlist[1],operator2,numlist[2],operator3,numlist[3])
                        try:
                            result=eval(expression)
                            if 24 == result:
                                print(expression.replace('/', '÷').replace('*', '×'))
                                resultList.append(expression.replace('/', '÷').replace('*', '×'))
                        except ZeroDivisionError:
                            print("You can't divide by zero!")
    return resultList

def idealization(expression):
    print(expression)
    bracketCnt=expression.count('(')
    if bracketCnt == 1:
        print('--------------->3')
        indexOfLBracket = expression.index('(')
        indexOfRBracket = expression.index(')')
        bracketStr = expression[indexOfLBracket + 1:indexOfRBracket]
        print(indexOfLBracket)
        print(indexOfRBracket)
        print('--------------------ddddddddd---------------')
        print(expression[indexOfLBracket-1])
        print(len(expression))
        print(expression[indexOfRBracket])
        print('--------------------ddddddddd---------------')
        if indexOfLBracket==0:
            print('--------------->4')
            if expression[indexOfRBracket+1] in {'+','-'}:
                print('--------------->5')
                newExpression = expression.replace('(' + bracketStr + ')', bracketStr)
                print(newExpression)
            else:
                print('--------------->6')
                newExpression = expression
        elif expression[indexOfLBracket-1] in {'+','-'} and (len(expression)==indexOfRBracket+1 or expression[indexOfRBracket] not in ['×','÷']):
            if expression[indexOfLBracket-1]=='-':
                print('--------------->7')
                newBracketStr=bracketStr.replace('+','#')
                newBracketStr=bracketStr.replace('-','+')
                newBracketStr=bracketStr.replace('#', '-')
                newExpression = expression.replace('(' + bracketStr + ')', newBracketStr)
                print(newExpression)
            else:
                print('--------------->8')
                newExpression = expression.replace('(' + bracketStr + ')', bracketStr)
        else:
            print('--------------->9')
            newExpression = expression
        print('--------------->11')
        return newExpression




    if bracketCnt == 2:
        print('--------------->2')
        indexOfOuterLBracket = expression.index('(')
        indexOfOuterRBracket = expression.rindex(')')
        print(indexOfOuterLBracket)
        print(indexOfOuterRBracket)

        indexOfInnerLBracket = expression.index('(',indexOfOuterLBracket+1,indexOfOuterRBracket)
        indexOfInnerRBracket = expression.index(')', indexOfOuterLBracket + 1, indexOfOuterRBracket)
        print(indexOfInnerLBracket)
        print(indexOfInnerRBracket)
        print(expression[indexOfOuterLBracket+1:indexOfOuterRBracket-1])

        innerBracketStr=expression[indexOfInnerLBracket+1:indexOfInnerRBracket]
        #如果内括号的前后没有×或÷，则括号可以去除，如果括号前是-，则去除括号时，括号内符号取反
        if expression[indexOfInnerLBracket-1] not in ['×','÷'] and expression[indexOfInnerRBracket+1] not in ['×','÷'] :
                if expression[indexOfInnerLBracket-1] == '-':
                    newInnerBracketStr=innerBracketStr.replace('+','#')
                    newInnerBracketStr=newInnerBracketStr.replace('-','+')
                    newInnerBracketStr=newInnerBracketStr.replace('#', '-')
                    print(newInnerBracketStr)
                else:
                    newInnerBracketStr=innerBracketStr
        else:
            if innerBracketStr.count('+')==0 and innerBracketStr.count('-')==0:
                newInnerBracketStr = innerBracketStr
            else:
                newInnerBracketStr = '('+innerBracketStr+')'
        newExpression=expression.replace('('+innerBracketStr+')',newInnerBracketStr)
        print(newExpression)
        print('--------------->1')
        finalExpression=idealization(newExpression)
        print('--------------->10')
        print(finalExpression)
        return finalExpression




if __name__ == '__main__':
    #numbers=[1,2,3,4,5,6,7,8,9,10]
    numbers = [8, 3, 4, 7]
    for combination in combinations(numbers, 4):
        #print(combination)
        resultList=compute24(combination)
        print(resultList)
        for i in resultList:
            print('!!!!!!!!!@@@@!!!!!!!!!!!!!'+i)
            kkk=idealization(i)
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@'+kkk)







