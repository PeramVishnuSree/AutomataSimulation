class State:
    def __init__(self, name):
        if type(name) != str:
            print ("state name must be a string")
            return None
        self.name = name #string
        self.transitions = {} #dictionary of alphabet: [States]
        self.accept = False
        self.start = False

class CreateAutomata:
    # updates all the nodes and returns start, accept and transition functions
    def __init__(self, file_path):
        #self.currentStates: list of the states that are active
        #self.alphabet: string of alphabet
        #self.states: list of all the states
        #self.acceptStates: list of all the states that accept an input
        #self.startState: startState 
        self.currentSates = [] # list of all the states the NFA or DFA is active in
        file = open(file_path, "r")
        lines = file.readlines()
        file.close()

        self.alphabet = lines[0].strip() #self.alphabet

        n = int(lines[1].strip())
        self.startState = lines[n+2].strip()
        self.states = [] #self.states
        m = int(lines[n+3].strip())
        accept_states = [lines[n+4+j].strip() for j in range(m)]
        self.acceptStates = [] #self.acceptStates
        for i in range(n):
            cur = State(lines[2+i].strip())
            if cur.name == self.startState:
                print("setting start state")
                cur.start = True
                self.startState = cur #self.startState
            if cur.name in accept_states:
                print("seting accept states")
                cur.accept = True
                self.acceptStates.append(cur)
            self.states.append(cur)

        #set transitions
        t = int(lines[m+n+4].strip())
        for k in range(t):
            params = lines[m+n+5+k].strip().split(',')
            alphabet = params[2].strip()
            fromState = params[0].strip()
            toState = params[1].strip()

            for l in self.states:
                if l.name == toState:
                    toState = l
                    print("set to State")
                    break

            for s in self.states:
                if s.name == fromState:
                    print("setting transitions")
                    if alphabet not in s.transitions:
                        s.transitions[alphabet] = [toState]
                        break
                    else:
                        s.transitions[alphabet].append(toState)
                        break

    def getStartState(self):
        return self.startState
    
    def getAcceptingStates(self):
        return self.acceptStates
    
    def getAlphabet(self):
        return self.alphabet
    
    def getStates(self):
        return self.states
    
    def decideString(self, string):
        string = string.strip()
        self.currentSates.append(self.startState)
        for tran, stats in self.startState.transitions.items():
            if tran == 'EPSILON':
                self.currentSates += stats
        for i in range(len(string)):
            print(string, [s.name for s in self.currentSates])
            if len(self.currentSates) == 0:
                self.currentSates = []
                return False
            
            #update current state for each character
            for j in range(len(self.currentSates)):
                if string[i] in self.currentSates[0].transitions:
                    curTransitions = self.currentSates[0].transitions[string[i]]
                    self.currentSates += curTransitions
                    for trans in curTransitions:
                        if 'EPSILON' in trans.transitions:
                            self.currentSates += trans.transitions['EPSILON']
                    self.currentSates.pop(0)
                elif 'EPSILON' in self.currentSates[0].transitions:
                    self.currentSates += self.currentSates[0].transitions['EPSILON']
                    self.currentSates.pop(0)
                else: 
                    self.currentSates.pop(0)

        if len(self.currentSates) != 0:
            for state in self.currentSates:
                print("final print:", [stat.name for stat in self.currentSates]) #printing
                if state.accept == True:
                    self.currentSates = []
                    return True
                
        self.currentSates = []
        return False