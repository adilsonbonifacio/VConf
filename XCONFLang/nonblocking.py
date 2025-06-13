import logging
from copy import deepcopy
from vpa import VPA

class NonBlocking:
    def __init__(self, vpa: VPA):
        self.vpa = vpa
        self.states = vpa.states
        self.transitions = vpa.transitions
        self.stack_symbols = vpa.stack_symbols
        self.calls = vpa.calls
        self.returns = vpa.returns
        self.internals = vpa.internals
        self.finals = vpa.finals
        self.initial_state = vpa.initial_state


    #def nonblocking(states, finals, trans, stacks, push, pop, inte):
    def nonblocking(self): #states, finals, trans, stacks, push, pop, inte):

        push = deepcopy(self.calls)
        pop = deepcopy(self.returns)
        inte = deepcopy(self.internals)
        ninitial = deepcopy(self.initial_state) 
        nstates = deepcopy(self.states) 
        nfinals = deepcopy(self.finals) 
        ntrans = deepcopy(self.transitions) 
        nstacks = deepcopy(self.stack_symbols)
        if not '*' in self.stack_symbols:
            nstacks.append('*')
        nstates.append('p')

        achou = True 
        while nstacks != [] and achou == True:
            Z = nstacks[0]
            if Z != '@' and Z != '*': 
                achou = False
        # no checking for epsilon moves - see Prop 14 when some epsilon moves exist

        set_pu = deepcopy(push)
        set_po = deepcopy(pop)
        set_inte = deepcopy(inte)
        symbols = []
        symbols = set_pu + set_po + set_inte
        npush = []
        npop = []
        ninte = []
        while self.states != []:
            s = self.states[0]
            self.states.remove(s)
            cur_trans = deepcopy(self.transitions)
            cur_symbols = deepcopy(symbols)
            while cur_trans != [] or cur_symbols != []:
                if cur_trans != [] : 
                    t = cur_trans[0]
                    cur_trans.remove(t)
                    if t[0]==s :
                        if t[1] in cur_symbols:
                            a=t[1] 
                            cur_symbols.remove(a) 
                            if a in set_pu : 
                                continue
                            elif a in set_po :
                                for W in nstacks : 
                                    if W != t[2] :
                                        nt = []
                                        nt = [s, a, W, 'p'] #setofstates_comp[indice['comp']]]
                                        if nt not in ntrans:
                                            npop.append(a)
                                            ntrans.append(nt)
                            elif a in set_inte:
                                continue 
                elif cur_symbols != [] : 
                    a = cur_symbols[0]
                    cur_symbols.remove(a) 
                    if a in set_pu : 
                        nt = []
                        nt = [s, a, Z, 'p'] #setofstates_comp[indice['comp']]]
                        if not nt in ntrans:
                            npush.append(a)
                            ntrans.append(nt)
                    elif a in set_po :
                        for W in nstacks : 
                            nt = []
                            nt = [s, a, W, 'p'] #setofstates_comp[indice['comp']]]
                            if nt not in ntrans:
                                npop.append(a)
                                ntrans.append(nt)
                    elif a in set_inte :
                        nt = []
                        nt = [s, a, '@', 'p'] #setofstates_comp[indice['comp']]]
                        if not nt in ntrans:
                            ninte.append(a)
                            ntrans.append(nt)

        for a in ninte:
            nt = ['p', a, '@', 'p']
            if not nt in ntrans:
                ntrans.append(nt)
        for a in npush:
            nt = ['p', a, Z, 'p']
            if not nt in ntrans:
                ntrans.append(nt)
        for a in npop:
            for W in nstacks:
                nt = ['p', a, W, 'p']
                if not nt in ntrans:
                    ntrans.append(nt)

        return [ninitial, nstates, nfinals, ntrans, nstacks]


def save_nonblocking_vpa(vpa2: VPA, iniciais, estados, transicoes, finais, pilha):
    import logging
    logging.info(f'Began to save a nonblocking VPA that accepts the intersection between D and the complementation of S (comp-otr(S))')
    vpa = VPA()
    vpa.states = estados
    vpa.calls = vpa2.calls
    vpa.returns = vpa2.returns
    vpa.internals = vpa2.internals
    vpa.stack_symbols = pilha
    vpa.transitions = transicoes
    vpa.finals = finais
    vpa.initial_state = iniciais
    return (vpa)

