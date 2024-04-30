class State:
    def __init__(self, name):
        if type(name) != str:
            print ("state name must be a string")
            return None
        self.name = name
        self.transitions = {}
        self.accept = False
        self.start = False

class CreateAutomata:
    # updates all the nodes and returns start, accept and transition functions
    def __init__(self, file_path):
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
                        s[alphabet].append(toState)
                        break

    def getStartState(self):
        return self.startState
    
    def getAcceptingStates(self):
        return self.acceptStates
    
    def getAlphabet(self):
        return self.alphabet
    
    def getStates(self):
        return self.states