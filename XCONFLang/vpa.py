import logging

class VPA:
    def __init__(self):
        self.calls = [] # push
        self.returns = [] # pop
        self.internals = []
        # self.input = []
        # self.output = []
        self.stack_symbols = []
        self.states = []
        self.finals = []
        self.initial_state = []
        self.transitions = []



    def add_state(self, state):
        self.states.append(state)

    def set_initial_state(self, state):
        self.initial_state = state

    def set_finals(self, state):
        self.states.append(state)

    def add_transition(self, from_state, action, stack_symbol, to_state):
        self.transitions.append((from_state, action, stack_symbol, to_state))

    def save_vpa_info_to_list(self, list):    
        list.append(f"Push symbols = {self.calls}")
        list.append(f"Pop symbols = {self.returns}")
        list.append(f"Internal symbols = {self.internals}")
        # list.append(f"Input symbols = {self.input}")
        # list.append(f"Output symbols = {self.output}")
        list.append(f"Stack symbols = {self.stack_symbols}")
        list.append(f"States =  {self.states}\n")
        list.append(f"Finals =  {self.finals}\n")
        list.append(f"Transitions:")
        transition_count = 0

        # Iterate over the flat list of transitions
        for from_state, action, stack_symbol, to_state in self.transitions:
            list.append(f"t{transition_count}: {from_state} --{action}/{stack_symbol}-> {to_state}")
            transition_count += 1

def read_vpa_file(file):
    import logging
    logging.info(f'Began reading vpa file')
    vpa = VPA()
    
    # Read file content from the file-like object
    content = file.read().decode("utf-8")  # Read and decode file content
    lines = [line.strip() for line in content.splitlines()]
    logging.info(lines)
    
    vpa.calls = lines[0].split(',') if lines[0] else []
    vpa.returns = lines[1].split(',') if lines[1] else []
    vpa.internals = lines[2].split(',') if lines[2] else ['@']
    # iovpts.input = lines[3].split(',') if lines[3] else []
    # iovpts.output = lines[4].split(',') if lines[4] else []
    vpa.stack_symbols = lines[3].split(',')
    states = lines[4].split(',')
    logging.info(states)
    vpa.finals = lines[5].split(',')

    for state in states:
        vpa.add_state(state)
    logging.info(vpa.states)
    
    transition_lines = lines[6:]
    for line in transition_lines:
        if line == "#":
            break
        parts = line.split(',')
        vpa.add_transition(parts[0], parts[1], parts[2], parts[3])

    vpa.set_initial_state(transition_lines[transition_lines.index("#") + 1])

    return vpa
