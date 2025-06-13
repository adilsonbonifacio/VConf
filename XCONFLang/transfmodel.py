from copy import deepcopy
from contracted import Contracted
from vpa import VPA
from iovpts import IOVPTS
import logging

class TransfModel:

    def __init__(self, contracted:Contracted):
        self.contracted = contracted
        self.states = deepcopy(contracted.states)
        self.finals = deepcopy(contracted.states)
        self.initial_state = deepcopy(contracted.initial_state)
        #self.initial_state = None
        self.transitions = deepcopy(contracted.transitions)
        #self.stacks = deepcopy(contracted.setofstacks)

    def save_vpa_contracted(self,iovpts:IOVPTS):
        import logging
        logging.info(f'Began to save a VPA from the IOVPTS contracted')
        vpa = VPA()
        vpa.calls = iovpts.calls
        vpa.returns = iovpts.returns
        vpa.internals = iovpts.internals
        vpa.stack_symbols = iovpts.stack_symbols
        vpa.states = self.states
        vpa.transitions = self.transitions
        vpa.finals = self.finals
        vpa.initial_state = self.initial_state
        return (vpa)
    
    def save_vpa_from_iovpts_to_list(self,list):
        #trans = oktrans
        trans = deepcopy(self.transitions)
        states = deepcopy(self.states)
        finals = deepcopy(self.finals) 
        #states = self.nok
        #faultstates = states
        list.append("The set of states for the vpa from iovpts contracted model is:")
        list.append(states)
        list.append("The set of finals for the vpa from iovpts contracted model is:")
        list.append(finals)
        list.append("The set of transitions for the vpa from iovpts contracted model is:")
        trans_list = []
        for transition in trans:  # Unpack tuples
            trans_list.append(f"t{len(trans_list)}: {transition[0]} --{transition[1]}/{transition[2]}-> {transition[3]}")
        for trans in trans_list:
            list.append(trans)
        return list

