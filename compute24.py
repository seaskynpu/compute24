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
                                ##print(expression.replace('/', '÷').replace('*', '×'))
                                resultList.append(expression.replace('/', '÷').replace('*', '×'))
                        except ZeroDivisionError:
                            print("You can't divide by zero!")
    return resultList

#判断表达式是一对括号（返回oneBracket）还是两对括号，如果是两对括号（返回twoBracket），是否是嵌套括号（返回nestingBracket）,如果没有括号，返回noneBracket
def judgeType(expression):
    bracketCnt = expression.count('(')
    if bracketCnt == 1:
        return ["oneBracket",len(expression),[expression.index('('),expression.index(')')]]
    elif bracketCnt == 2:
        indexOfFirstLBracket=expression.index('(')
        indexOfSecondLBracket = expression.index('(', indexOfFirstLBracket + 1)
        indexOfFirstRBracket = expression.index(')')
        indexOfSecondRBracket = expression.index(')', indexOfFirstRBracket + 1)
        if indexOfFirstRBracket > indexOfSecondLBracket:
            return ['nestingBracket',len(expression),[indexOfFirstLBracket,indexOfSecondRBracket],[indexOfSecondLBracket,indexOfFirstRBracket]]
        else:
            return ['twoBracket',len(expression),[indexOfFirstLBracket,indexOfFirstRBracket],[indexOfSecondLBracket,indexOfSecondRBracket]]
    else:
        return ['noneBracket',len(expression)]


def eraseBarcket(exp):
    # 如果内括号的前后没有×或÷，则括号可以去除，如果括号前是-，则去除括号时，括号内符号取反
    ##print('---------------------->'+exp)
    if exp[0] not in ['×', '÷'] and exp[-1] not in ['×','÷']:
        if exp[0] == '-':
            expNew = exp[2:-2].replace('+', '&')
            expNew = expNew.replace('-', '+')
            expNew = expNew.replace('&', '-')
        else:
            expNew = exp[2:-2]
    else:
        if exp.count('+') == 0 and exp.count('-') == 0:
            expNew = exp[2:-2]
        else:
            expNew = exp[1:-1]
    ##print('---------->'+expNew)
    ##print(expNew)
    return expNew

def extractBracket(expression,len,begin,end):
    bracket = expression[begin:end + 1]
    if begin == 0:
        bracketWithContext = '#' + bracket
    else:
        bracketWithContext = expression[begin - 1] + bracket
    if end == len - 1:
        bracketWithContext = bracketWithContext + '#'
    else:
        bracketWithContext = bracketWithContext + expression[end + 1]
    ##print('-->' + bracket)
    ##print('-->' + bracketWithContext)
    return [bracket,bracketWithContext]

def idealization2(expression):
    ##print(expression)
    expressionInfo=judgeType(expression)
    lenOfExp = expressionInfo[1]
    if expressionInfo[0] == 'nestingBracket':
        innerBracket=extractBracket(expression, lenOfExp, expressionInfo[3][0], expressionInfo[3][1])
        innerBracketNew=eraseBarcket(innerBracket[1])
        ##print(innerBracketNew)

        outterBracket = extractBracket(expression,lenOfExp,expressionInfo[2][0],expressionInfo[2][1])
        ##print(outterBracket)
        outterBracketReplaced=[outterBracket[0].replace(innerBracket[0],'I'),outterBracket[1].replace(innerBracket[0],'I')]
        ##print(outterBracketReplaced)
        outterBracketReplacedNew = eraseBarcket(outterBracketReplaced[1])
        ##print(outterBracketReplacedNew)
        expressionNew=expression.replace(outterBracket[0],outterBracketReplacedNew).replace('I',innerBracketNew)
        ##print('expressionNew------------->'+expressionNew)
    if expressionInfo[0] == 'twoBracket':
        firstBracket=extractBracket(expression, lenOfExp, expressionInfo[2][0], expressionInfo[2][1])
        firstBracketNew = eraseBarcket(firstBracket[1])
        ##print(firstBracketNew)

        secondBracket=extractBracket(expression, lenOfExp, expressionInfo[3][0], expressionInfo[3][1])
        secondBracketNew = eraseBarcket(secondBracket[1])
        ##print(secondBracketNew)
        expressionNew=expression.replace(firstBracket[0],firstBracketNew).replace(secondBracket[0],secondBracketNew)
        ##print('expressionNew------------->'+expressionNew)
    if expressionInfo[0] == 'oneBracket':
        bracket = extractBracket(expression, lenOfExp, expressionInfo[2][0], expressionInfo[2][1])
        bracketNew = eraseBarcket(bracket[1])
        expressionNew = expression.replace(bracket[0], bracketNew)
        ##print('expressionNew------------->'+expressionNew)
    if expressionInfo[0] == 'noneBracket':
        expressionNew=expression
    return  expressionNew


        # outerBracketWithContextReplaced = outerBracketWithContext.replace(innerBracket, 'I')


def idealization1(expression):
    ##print(expression)
    expressionInfo=judgeType(expression)
    lenOfExp = expressionInfo[1]
    if expressionInfo[0] == 'nestingBracket':
        innerBracketBegin=expressionInfo[3][0]
        innerBracketEnd=expressionInfo[3][1]
        ##print(innerBracketBegin)
        ##print(innerBracketEnd)
        # 处理嵌套的括号
        innerBracket=expression[innerBracketBegin:innerBracketEnd+1]
        ##print(innerBracket)
        innerBracketWithContext=expression[innerBracketBegin-1]+innerBracket+expression[innerBracketEnd+1]
        ##print(innerBracketWithContext)
        innerBracketNew=eraseBarcket(innerBracketWithContext)
        ##print('eraseBarcket(innerBracketWithContext)--->'+eraseBarcket(innerBracketWithContext))

        #处理外面的括号
        outerBracketBegin=expressionInfo[2][0]
        outerBracketEnd=expressionInfo[2][1]

        outerBracket=expression[outerBracketBegin:outerBracketEnd+1]
        ##print(outerBracket)
        if outerBracketBegin==0:
            ##print('111')
            outerBracketWithContext='#'+outerBracket
        else:
            ##print('222')
            ##print(expression[outerBracketBegin-1])
            outerBracketWithContext=expression[outerBracketBegin-1]+outerBracket
        if outerBracketEnd==lenOfExp-1:
            outerBracketWithContext =  outerBracketWithContext+'#'
        else:
            outerBracketWithContext = outerBracketWithContext + expression[outerBracketEnd+2]
        outerBracketWithContextReplaced=outerBracketWithContext.replace(innerBracket,'I')
        ##print('-->'+outerBracketWithContext)
        ##print(outerBracketWithContextReplaced)
        ##print('eraseBarcket(outerBracketWithContextReplaced)---------->'+eraseBarcket(outerBracketWithContextReplaced))
        outerBracketWithContextReplacedNew=eraseBarcket(outerBracketWithContextReplaced)
        ##print(outerBracketWithContextReplacedNew.replace('I',innerBracketNew))
        finalExp=expression.replace(outerBracket,outerBracketWithContextReplacedNew.replace('I',innerBracketNew))
        ##print(finalExp)
    if expressionInfo[0] == 'twoBracket':
        ##print('process first Bracket')
        firstBracketBegin=expressionInfo[2][0]
        firstBracketEnd=expressionInfo[2][1]
        firstBracket=expression[firstBracketBegin:firstBracketEnd+1]
        ##print(firstBracket)
        if firstBracketBegin==0:
            ##print('111')
            firstBracketWithContext='#'+firstBracket
        else:
            ##print('222')
            ##print(expression[firstBracketBegin-1])
            firstBracketWithContext=expression[firstBracketBegin-1]+firstBracket
        if firstBracketEnd==lenOfExp-1:
            firstBracketWithContext =  firstBracketWithContext+'#'
        else:
            firstBracketWithContext = firstBracketWithContext + expression[firstBracketEnd+2]
        ##print(eraseBarcket(firstBracketWithContext))

        ##print('process second Bracket')
        secondBracketBegin=expressionInfo[3][0]
        secondBracketEnd=expressionInfo[3][1]
        secondBracket=expression[secondBracketBegin:secondBracketEnd+1]
        ##print(secondBracket)
        if secondBracketBegin==0:
            ##print('111')
            secondBracketWithContext='#'+secondBracket
        else:
            ##print('222')
            ##print(expression[secondBracketBegin-1])
            secondBracketWithContext=expression[secondBracketBegin-1]+secondBracket
        if secondBracketEnd==lenOfExp-1:
            secondBracketWithContext =  secondBracketWithContext+'#'
        else:
            secondBracketWithContext = secondBracketWithContext + expression[secondBracketEnd+2]
        ##print(eraseBarcket(secondBracketWithContext))






def idealization(expression):
    ##print(expression)
    bracketCnt=expression.count('(')
    if bracketCnt == 1:
        ##print('--------------->3')
        indexOfLBracket = expression.index('(')
        indexOfRBracket = expression.index(')')
        bracketStr = expression[indexOfLBracket + 1:indexOfRBracket]
        ##print(indexOfLBracket)
        ##print(indexOfRBracket)
        ##print('--------------------ddddddddd---------------')
        ##print(expression[indexOfLBracket-1])
        ##print(len(expression))
        ##print(expression[indexOfRBracket])
        ##print('--------------------ddddddddd---------------')
        if indexOfLBracket==0:
            ##print('--------------->4')
            if expression[indexOfRBracket+1] in {'+','-'}:
                ##print('--------------->5')
                newExpression = expression.replace('(' + bracketStr + ')', bracketStr)
                ##print(newExpression)
            else:
                ##print('--------------->6')
                newExpression = expression
        elif expression[indexOfLBracket-1] in {'+','-'} and (len(expression)==indexOfRBracket+1 or expression[indexOfRBracket] not in ['×','÷']):
            if expression[indexOfLBracket-1]=='-':
                ##print('--------------->7')
                newBracketStr=bracketStr.replace('+','#')
                newBracketStr=bracketStr.replace('-','+')
                newBracketStr=bracketStr.replace('#', '-')
                newExpression = expression.replace('(' + bracketStr + ')', newBracketStr)
                ##print(newExpression)
            else:
                ##print('--------------->8')
                newExpression = expression.replace('(' + bracketStr + ')', bracketStr)
        else:
            ##print('--------------->9')
            newExpression = expression
        ##print('--------------->11')
        return newExpression




    if bracketCnt == 2:
        ##print('--------------->2')
        indexOfOuterLBracket = expression.index('(')
        indexOfOuterRBracket = expression.rindex(')')
        ##print(indexOfOuterLBracket)
        ##print(indexOfOuterRBracket)

        indexOfInnerLBracket = expression.index('(',indexOfOuterLBracket+1,indexOfOuterRBracket)
        indexOfInnerRBracket = expression.index(')', indexOfOuterLBracket + 1, indexOfOuterRBracket)
        ##print(indexOfInnerLBracket)
        ##print(indexOfInnerRBracket)
        ##print(expression[indexOfOuterLBracket+1:indexOfOuterRBracket-1])

        innerBracketStr=expression[indexOfInnerLBracket+1:indexOfInnerRBracket]
        #如果内括号的前后没有×或÷，则括号可以去除，如果括号前是-，则去除括号时，括号内符号取反
        if expression[indexOfInnerLBracket-1] not in ['×','÷'] and expression[indexOfInnerRBracket+1] not in ['×','÷'] :
                if expression[indexOfInnerLBracket-1] == '-':
                    newInnerBracketStr=innerBracketStr.replace('+','#')
                    newInnerBracketStr=newInnerBracketStr.replace('-','+')
                    newInnerBracketStr=newInnerBracketStr.replace('#', '-')
                    ##print(newInnerBracketStr)
                else:
                    newInnerBracketStr=innerBracketStr
        else:
            if innerBracketStr.count('+')==0 and innerBracketStr.count('-')==0:
                newInnerBracketStr = innerBracketStr
            else:
                newInnerBracketStr = '('+innerBracketStr+')'
        newExpression=expression.replace('('+innerBracketStr+')',newInnerBracketStr)
        ##print(newExpression)
        ##print('--------------->1')
        finalExpression=idealization(newExpression)
        ##print('--------------->10')
        ##print(finalExpression)
        return finalExpression




if __name__ == '__main__':
    #numbers=[1,2,3,4,5,6,7,8,9,10]
    numbers = [1, 3, 8, 7, 9]
    for combination in combinations(numbers, 4):
        print('*********'+combination.__str__()+'*********')
        resultList=compute24(combination)
        print(resultList)
        for r in resultList:
            print(r)
            rNew=idealization2(r)
            print(r+'------------>'+rNew)
    # ##print(judgeType('1+2+3+4'))
    # ##print(judgeType('(1+2)+3+4'))
    # ##print(judgeType('1+(2+3)+4'))
    # ##print(judgeType('1+2+(3+4)'))
    # ##print(judgeType('(1+2)+(3+4)'))
    # ##print(judgeType('((1+2)+3)+4'))
    # ##print(judgeType('1+(2+(3+4))'))
    #idealization1('1+(2+(3+4))')
    # idealization1('(1+2)+(3+4)')
    #idealization1('(1+(2+3))+4')
    # idealization2('((1+2)+3)+4')
    # idealization2('(1+(2+3))+4')
    # idealization2('1+((2+3)+4)')
    # idealization2('1+(2+(3+4))')
    # idealization2('(1+2)+(3+4)')
    # idealization2('(1+2)×(3+4)')
    # idealization2('(1+2)÷(3+4)')
    # idealization2('(1×2)-(3+4)')
    # idealization2('(1×2)-(3÷4)')
    # idealization2('(1×2)-3÷4')
    # idealization2('1×(2-3)÷4')
    # idealization2('1×2-(3÷4)')
    # idealization2('(1×2-3)÷4')
    # idealization2('1×(2-3)÷4)')





