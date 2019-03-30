#G00349377
#Jake Warren 
#Graph Theory - Project 2019
#This program will allow the user to parse a Regular Expression(RE) using the shunting yard algorithm -
# - into a Non Finite Automata(NFA). It will also check the NFA to see if the RE matches a string of text.


#Shunting Yard Algorithm
def shunt(infix):
    #A dictionary of special characters for the regular expressions
    specialChars = {'*': 4,'+': 3, '.': 2, '|': 1}

    #OperatorStack
    stack =""
    #Output
    postfix =""

    for c in infix:
        #Add ( to the stack
        if c == '(':
            stack = stack + c 
        elif c == ')':
            #Pushes to the end of the stack
            while stack[-1] != '(':
                #Add operators to the post fix and Removes operator from the stack
                postfix, stack = postfix + stack[-1], stack[:-1]
            #Repeat to remove '(' from the stack
            stack = stack[:-1]
        elif c in specialChars:
            #While the stack is not empty push operator from top of the stack which has a greater precedence
            while stack and specialChars.get(c, 0) <= specialChars.get(stack[-1], 0):
                 postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack + c
        #Pushes reg characters to our output
        else:
            postfix = postfix + c
        #Push remainder of the stack to the end of the post fix
    while stack:
        #Add operators to the post fix and remove '(' from the stack
        postfix,stack = postfix + stack[-1],stack[:-1]
    return postfix

#Thompsons Construction

class state:
    label, edge1, edge2 = None, None, None
    

#NFA will only ever have initial and accept state
class nfa:
    initial, accept = None,None
    #Instance of the nfa class
    def __init__(self,initial,accept):
        self.initial, self.accept = initial, accept

#compiles the post fix regular expression into a Non Finite Automata
def compile(postfix):
    nfaStack = []

    for c in postfix:
        
        #Concatinate
        if c =='.':
            #Pop in Last in first out order
            nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
            nfa1.accept.edge1 = nfa2.initial
            #pushes back onto the nfaStack
            nfaStack.append(nfa(nfa1.initial, nfa2.accept))   
        #Or
        elif c == '|':
            nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
           #create initial and accept states
            accept, initial = state(), state()
            #point initial edges to the initial states of both nfa's from the stack
            initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial
           #The two nfa's are now the new accept state
            nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept
           #Push the new formed NFA back to the stack
            nfaStack.append(nfa(initial, accept))      
        elif c == '*':
            #pop single NFA from stack
            nfa1 = nfaStack.pop()
            #create initial and accept states
            accept, initial = state(), state()
            #join initial to nfa1 initial state
            initial.edge1, nfa1.accept.edge1 = nfa1.initial, nfa1.initial
            #join accept state to nfa accept state
            initial.edge2, nfa1.accept.edge2 = accept, accept
            #Push the new formed NFA back to the stack
            nfaStack.append(nfa(initial, accept))  
        elif c == '+':
            #pop single NFA from stack
            nfa1 = nfaStack.pop()
            #create initial and accept states
            accept, initial = state(), state()
            #join initial to nfa1 initial state
            initial.edge1, nfa1.accept.edge1 = nfa1.initial, nfa1.initial
            #join accept state to nfa accept state
            initial.edge2, nfa1.accept.edge2 = accept, accept
            #Push the new formed NFA back to the stack
            nfaStack.append(nfa(initial, accept))  
        else:
        #new instance of accept and initial states
            accept, initial = state(), state()
        #join the initial state to the accept, using C
            initial.label, initial.edge1 = c, accept
        #Push the new formed NFA back to the stack
            nfaStack.append(nfa(initial, accept))

    #Should only return a single NFA
    return nfaStack.pop()
    
    #Check if state has arrows and are labeled
def checker(state):
#Create new set with state as the only variable
    states = set()
    states.add(state)

    #Check if state has an arrow(s) labelled E
    if state.label is None:
        #Check state
        if state.edge1 is not None:
            states |= checker(state.edge1)
            #Check state
        if state.edge2 is not None:
            states |= checker(state.edge2)
    return states

def match(infix, string):
#Apply shunting algorithm and compiles NFA
    postfix = shunt(infix)
    nfa = compile(postfix)

    #Set curruent and next set of the states
    currentState = set()
    nextState = set()

    #Join the initial state and current state
    currentState |= checker(nfa.initial)

    #Loop through the string
    for s in string:
        #Loop through the current states
        for c in currentState:
            # Check for any state that has the label S
            if c.label == s:
                #Join edge1 state to the next state
                nextState |= checker(c.edge1)
        #Set current to next and then wipe next
        currentState = nextState
        nextState = set()
    return (nfa.accept in currentState)

#Test lines
infixes = ["a.b.c", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b).c", "a.(b.b).c+a.b|c", "d+a+b"]
string =  ["", "abc", "abbc", "abcc", "abad", "abbbc","abbcabc","dab"]
#Tests
for i in infixes:
    for s in string:
        print(match(i, s), i, s)