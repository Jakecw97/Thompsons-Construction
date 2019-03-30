#G00349377
#Jake Warren 
#Graph Theory Project 2019
#This program will allow the user to parse a Regular Expression(RE) using the shunting yard algorithm -
# - into a Non Finite Automata(NFA). It will also check the NFA to see if the RE matches a string of text.


#Shunting Yard Algorithm
def shunt(infix):
    #A dictionary of special characters for the regular expressions
    specialChars = {'*': 4,'?': 3,'+': 3,'-': 3, '.': 2, '|': 1}

    #OperatorStack
    stack =""
    #Output
    pofix =""

    for c in infix:
        #Add ( to the stack
        if c =='(':
            stack = stack + c
           
        elif c==')':
            #Pushes to the end of the stack
            while stack[-1] != '(':
                #Add operators to the post fix
                pofix = pofix + stack[-1]
                #Removes operator from the stack
                stack = stack[:-1]
                #Repeat to remove '(' from the stack
                stack = stack[:-1]

        elif c in specialChars:
            #While the stack is not empty push operator from top of the stack which has a greater precedence
            while stack and specialChars.get(c, 0) <= specials.get(stack[-1], 0):
                 profix, stack = profix + stack[-1], stack[:-1]
            stack = stack + c

        #Pushes reg characters to our output
        else:
            profix = profix + c

        #Push remainder of the stack to the end of the post fix
        while stack
            #Add operators to the post fix and remove '(' from the stack
            pofix,stack = pofix + stack[-1],stack[:-1]
 

    return pofix