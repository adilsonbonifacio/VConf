from copy import deepcopy
from transfmodel import TransfModel
from iovpts import IOVPTS
from vpa import VPA

class CompModel:
    def __init__(self, transfmodel:TransfModel,iovpts:IOVPTS):
        self.transfmodel = transfmodel
        self.states = deepcopy(transfmodel.states)
        self.finals = deepcopy(transfmodel.states)
        self.Z = iovpts.stack_symbols[0]
        self.setofstacks = deepcopy(iovpts.stack_symbols)
        if "*" not in self.setofstacks:
            self.setofstacks.append("*")
        #self.initial_state = None
        self.transitions = deepcopy(transfmodel.transitions)
        self.calls = deepcopy(iovpts.calls)
        self.returns = deepcopy(iovpts.returns)
        self.internals = deepcopy(iovpts.internals)
        self.setofstates_comp = []
        self.static_trans = []
        self.setoffinals_comp = []
        self.initial_state = iovpts.initial_state
        
    #def compute_complement(self,pu, po, inte, setofstacks, setofstates, setoffinals, setoftrans):
    def compute_complement(self):
        pu = deepcopy(self.calls)
        po = deepcopy(self.returns)
        inte = deepcopy(self.internals)
        setofstacks = deepcopy(self.setofstacks) 
        #print(setofstacks)
        setofstates = deepcopy(self.states)
        setoffinals = deepcopy(self.finals)
        setoftrans = deepcopy(self.transitions)
        
        static_trans = deepcopy(setoftrans)
        setofstates_comp = deepcopy(setofstates)
        setofstates_comp.append("comp")
        #setofstacks.append("*")
        W = setofstacks[0]
        indice = {}
        s = 0
        for i in setofstates_comp:
            indice[i] = s
            s += 1

        comp_trans = deepcopy(static_trans)
        comp_states = deepcopy(setofstates)
        set_pu = deepcopy(pu)
        set_po = deepcopy(po)
        set_inte = deepcopy(inte)
        set_stack = deepcopy(setofstacks)
        symbols = []
        symbols = set_pu + set_po + set_inte

        while comp_states != []:
            s = comp_states[0]
            comp_states.remove(s)
            cur_symbols = deepcopy(symbols)
            while cur_symbols != []:
                a = cur_symbols[0]
                cur_symbols.remove(a)
                cur_stacks = deepcopy(set_stack)
                while cur_stacks != []:
                    Z = cur_stacks[0]
                    cur_stacks.remove(Z)
                    cur_trans = deepcopy(comp_trans)
                    for t in cur_trans:
                        # t = cur_trans[0]
                        trans_exist = False
                        if s == t[0] and a == t[1] and Z == t[2]:
                            trans_exist = True
                            break
                    if trans_exist == False:
                        if a in set_pu and Z != '*' and Z != '@':
                            trt = []
                            trt = [s, a, Z, setofstates_comp[indice['comp']]]
                            if not trt in static_trans:
                                static_trans.append(trt)
                        elif a in set_po and Z != '@':
                            trt = []
                            trt = [s, a, Z, setofstates_comp[indice['comp']]]
                            if not trt in static_trans:
                                static_trans.append(trt)
                        elif a in set_inte and Z == '@':
                            trt = []
                            trt = [s, a, '@', setofstates_comp[indice['comp']]]
                            if not trt in static_trans:
                                static_trans.append(trt)

        for a in pu:
            trt = []
            trt = [setofstates_comp[indice['comp']],
                a, W, setofstates_comp[indice['comp']]]
            static_trans.append(trt)
        for a in po:
            for Z in setofstacks:
                if Z != '@':
                    trt = []
                    trt = [setofstates_comp[indice['comp']],
                        a, Z, setofstates_comp[indice['comp']]]
                    static_trans.append(trt)
        for a in inte:
            trt = []
            trt = [setofstates_comp[indice['comp']], a,
                '@', setofstates_comp[indice['comp']]]
            static_trans.append(trt)

        setoffinals_comp = []
        for s in setofstates_comp:
            if s in setoffinals:
                continue
            else:
                setoffinals_comp.append(s)

        self.setofstates_comp = setofstates_comp 
        self.static_trans = static_trans 
        self.setoffinals_comp = setoffinals_comp
        return [self.setofstates_comp, self.static_trans, self.setoffinals_comp]

    def save_comp_model(self):
        import logging
        logging.info(f'Began to save a VPA that accepts the complementation of S (comp-otr(S))')
        vpa = VPA()
        vpa.calls = self.calls
        vpa.returns = self.returns
        vpa.internals = self.internals
        vpa.stack_symbols = self.setofstacks
        vpa.states = self.setofstates_comp
        vpa.transitions = self.static_trans
        vpa.finals = self.setoffinals_comp
        vpa.initial_state = self.initial_state
        return (vpa)

    def save_compmodel_info_to_list(self,list):
        #trans = oktrans
        trans = deepcopy(self.static_trans)
        states = deepcopy(self.setofstates_comp)
        finals = deepcopy(self.setoffinals_comp)
        #states = self.nok
        #faultstates = states
        list.append("The set of states for the VPA that accepts the complementation of S is:")
        list.append(states)
        list.append("The set of finals for the VPA that accepts the complementation of S is:")
        list.append(finals)
        list.append("The set of transitions for the VPA that accepts the complementation of S is:")
        trans_list = []
        for transition in trans:  # Unpack tuples
            trans_list.append(f"t{len(trans_list)}: {transition[0]} --{transition[1]}/{transition[2]}-> {transition[3]}")
        for trans in trans_list:
            list.append(trans)
        return list
    