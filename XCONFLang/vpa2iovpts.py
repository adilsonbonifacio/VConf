from vpa import VPA
from iovpts import IOVPTS

class VPA2IOVPTS:
    def __init__(self,vpa:VPA,iovpts:IOVPTS):
        self.calls = vpa.calls
        self.returns = vpa.returns
        self.internals = vpa.internals
        self.input = iovpts.input
        self.output = iovpts.output
        self.stack_symbols = vpa.stack_symbols
        self.states = vpa.states
        self.initial_state = vpa.initial_state
        self.finals = vpa.finals
        self.transitions = vpa.transitions

    def save_vpa2iovpts(self):
        import logging
        logging.info(f'Began to save the IOVPTS from VPA')
        vpa2iovpts = VPA2IOVPTS()
        vpa2iovpts.calls = self.calls
        vpa2iovpts.returns = self.returns
        vpa2iovpts.internals = self.internals
        vpa2iovpts.input = self.input
        vpa2iovpts.output = self.output
        vpa2iovpts.stack_symbols = self.stack_symbols
        vpa2iovpts.states = self.states
        vpa2iovpts.transitions = self.transitions
        vpa2iovpts.finals = self.finals
        vpa2iovpts.initial_state = self.initial_state
        return (vpa2iovpts)
