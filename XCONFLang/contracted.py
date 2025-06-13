from copy import deepcopy
from iovpts import IOVPTS
import logging

class Contracted:
    def __init__(self, iovpts: IOVPTS):
        self.iovpts = iovpts
        #self.setofstates_fail = deepcopy(iovpts.states)
        #self.setofstates_fail.append("fail")
        self.setofstates = deepcopy(iovpts.states)
        self.setoffinals = deepcopy(iovpts.finals)
        self.initial_state = deepcopy(iovpts.initial_state)
        #self.final = deepcopy(self.iovpts.states)
        if iovpts.stack_symbols != []: 
            self.Z = iovpts.stack_symbols[0]
        self.setofstacks = deepcopy(iovpts.stack_symbols)
        if '*' not in self.setofstacks: 
            self.setofstacks.append("*")
        self.indice = {state: idx for idx, state in enumerate(self.setofstates)}
        self.static_trans = deepcopy(iovpts.transitions)
        self.trans = deepcopy(self.static_trans)
        self.push = deepcopy(iovpts.calls)
        self.pop = deepcopy(iovpts.returns)
        self.inte = deepcopy(iovpts.internals) 
        self.LI = deepcopy(iovpts.input)
        self.LU = deepcopy(iovpts.output) 
        
        self.oktrans = []
        self.ok = []
        self.nok = []
        self.delta = []
        self.okleft = []
        self.okpairs = []
        self.oktrans = []
        self.okstates = []
        
    #def getallprods(states, trans, push, pop, inte):
    def getallprods(self):
        states = deepcopy(self.iovpts.states)
        #final = deepcopy(self.iovpts.states)
        trans = deepcopy(self.iovpts.transitions)
        push = deepcopy(self.iovpts.calls)
        pop = deepcopy(self.iovpts.returns)
        inte = deepcopy(self.iovpts.internals)
        prods = []
        ok = []
        nok = [[states[0], '*', '-']]
        # Pick non-terminals in nok
        while len(nok) > 0:
            nt = nok[0]
            nok = nok[1:]
            ok.append(nt)
            for tr in trans:
                if not isinstance(nt, list):
                    break
                if tr[0] != nt[0]:
                    continue
                t = "t"+str(trans.index(tr))
                symb = tr[1]
                if symb in push:
                    # prods, newnts = makepush(prods, states,nt, tr, t)
                    endtr = tr[3]
                    stacktr = tr[2]
                    stacknt = nt[1]
                    endnt = nt[2]
                    nts = []
                    for u in states:
                        nt1 = [endtr, stacktr, u]
                        nt2 = [u, stacknt, endnt]
                        prods.append([nt, t, nt1, nt2])
                        nts = nts+[nt1, nt2]
                elif symb in pop:
                    # prods, newnts = makepop(prods, nt, tr, t)
                    endtr = tr[3]
                    stacktr = tr[2]
                    stacknt = nt[1]
                    endnt = nt[2]
                    nt1 = []
                    # nt1 = ['', '', '']
                    if (stacknt == stacktr) and (endtr == endnt):
                        prods.append([nt, t])
                        # return ([prods])
                    if (stacknt == '*') and (stacktr == '*'):
                        nt1 = [endtr, '*', '-']
                        prods.append([nt, t, nt1])
                        # return ([prods, nt1])
                    # return ([prods])
                elif symb in inte:
                    # prods, newnts = makeint(prods, nt, tr, t)
                    endtr = tr[3]
                    stacknt = nt[1]
                    endnt = nt[2]
                    nt1 = [endtr, stacknt, endnt]
                    prods.append([nt, t, nt1])
                for x in nts+nt1:
                    if x not in (ok+nok):
                        nok.append(x)
        return ([prods, nok, ok])

# Which non terminals generate only terminals

    def genterminals(self,prods):
        #states = deepcopy(self.iovpts.states)
        #prods = self.prods
        delta = []
        for pr in prods:
            if len(pr) == 2:
                delta.append(pr[0])
        prev = 0
        prox = len(delta)
        # while delta increases make another pass
        while prev != prox:
            for pr in prods:
                if (len(pr) == 3) and (pr[2] in delta):
                    if pr[0] not in delta:
                        delta.append(pr[0])
                if (len(pr) == 4) and (pr[2] in delta) and (pr[3] in delta):
                    if pr[0] not in delta:
                        delta.append(pr[0])
            prev = prox
            prox = len(delta)
        return (delta)

# leftmost(prods,delta): which non-terminals can appear as leftmost in a derivation?
#  prods = productions; delta = nonterminals that generate a string of terminals

# grab leftmost non-terminals
    def leftmost(self,prods,delta):
        #prods = self.prods
        #delta = self.delta
        okleft = []
        nokleft = [[self.iovpts.states[0], '*', '-']]
        while len(nokleft) > 0:
            nt = nokleft[0]
            okleft.append(nt)
            nokleft = nokleft[1:]
            for pr in prods:
                if (pr[0] == nt) and (len(pr) > 2):
                    if (pr[2] not in okleft) and (pr[2] not in nokleft):
                        nokleft.append(pr[2])
                    if (len(pr) > 3) and (pr[2] in delta):
                        if (pr[3] not in okleft) and (pr[3] not in nokleft):
                            nokleft.append(pr[3])
        return (okleft)

# usefulpairs(okleft): grab unique pairs [state,top] from non-terminals
#   okleft: list of non-terminals

# grab pairs [s,Z] where we reach s with Z on the stack
    def usefulpairs(self,okleft):
        #okleft = self.okleft
        okpairs = []
        for nt in okleft:
            if [nt[0], nt[1]] in okpairs:
                continue
            okpairs.append([nt[0], nt[1]])
        return (okpairs)

# usefultrans(trans,okpairs): grab useful transitions
#   trans = transitions; okpairs = leftmost [state,top]

# grab useful transactions
    def usefultrans(self,trans,okpairs):
        # If  [s,Z] appears as okpairs, check transitions from s
        trans = deepcopy(self.iovpts.transitions)
        finais = deepcopy(self.iovpts.finals)
        #trans = self.trans
        #okpairs = self.okpairs
        oktrans = []
        noktrans = trans
        newstates = []
        newfinals = []
        for p in okpairs:
            # pegando os estados (stat) corretos... 0 e 0
            stat = p[0]
            stack = p[1]
            newtrans = []
            for tr in noktrans:
                if tr[0] != stat:
                    continue
                if (tr[1] in self.iovpts.calls) or (tr[1] in self.iovpts.internals):
                    if tr not in newtrans:
                        newtrans.append(tr)
                if tr[2] == stack:
                    if tr not in newtrans:
                        newtrans.append(tr)
            oktrans = oktrans+newtrans
            noktrans = [x for x in noktrans if x not in newtrans]
            if stat not in newstates:
                newstates.append(stat)
        while finais:
            final = finais[0]
            finais.remove(final)
            if final in newstates:
                newfinals.append(final)
        self.oktrans = oktrans
        self.newstates = newstates
        self.setoffinals = newfinals
        return (self.oktrans,self.newstates,self.setoffinals)

    def save_iovpts_contracted(self):
        import logging
        logging.info(f'Began to save a contracted iovpts')
        iovpts = IOVPTS()
        iovpts.calls = self.push
        iovpts.returns = self.pop
        iovpts.internals = self.inte
        iovpts.input = self.LI
        iovpts.output = self.LU
        iovpts.stack_symbols = self.setofstacks
        iovpts.transitions = self.oktrans
        iovpts.states = self.newstates
        iovpts.finals = self.setoffinals
        iovpts.initial_state = self.initial_state 
        #iovpts.finals = self.newfinals
        return (iovpts)

    def save_contracted_info_to_list(self,list):
        #trans = oktrans
        trans = deepcopy(self.oktrans)
        states = deepcopy(self.newstates)
        #states = self.nok
        #faultstates = states
        list.append("The set of states for the contracted model is:")
        list.append(states)
        list.append("The set of transitions for the contracted model is:")
        trans_list = []
        for transition in trans:  # Unpack tuples
            trans_list.append(f"t{len(trans_list)}: {transition[0]} --{transition[1]}/{transition[2]}-> {transition[3]}")
        for trans in trans_list:
            list.append(trans)
        return list

