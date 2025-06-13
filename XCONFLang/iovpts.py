import logging

class IOVPTS:
    def __init__(self):
        self.calls = [] # push
        self.returns = [] # pop
        self.internals = []
        self.input = []
        self.output = []
        self.stack_symbols = []
        self.states = []
        
        self.initial_state = None
        self.finals = None
        self.transitions = []

    def add_state(self, state):
        self.states.append(state)

    def set_initial_state(self, state):
        self.initial_state = state

    def add_transition(self, from_state, action, stack_symbol, to_state):
        self.transitions.append((from_state, action, stack_symbol, to_state))
        if stack_symbol == '@' and stack_symbol not in self.stack_symbols:
            self.stack_symbols.append(stack_symbol)
        if stack_symbol == '*' and stack_symbol not in self.stack_symbols:
            self.stack_symbols.append(stack_symbol)

    def save_iovpts_info_to_list(self, list):    
        list.append(f"Push symbols = {self.calls}")
        list.append(f"Pop symbols = {self.returns}")
        list.append(f"Internal symbols = {self.internals}")
        list.append(f"Input symbols = {self.input}")
        list.append(f"Output symbols = {self.output}")
        list.append(f"Stack symbols = {self.stack_symbols}")
        list.append(f"States =  {self.states}\n")
        list.append(f"Transitions:")
        transition_count = 0

        # Iterate over the flat list of transitions
        for from_state, action, stack_symbol, to_state in self.transitions:
            list.append(f"t{transition_count}: {from_state} --{action}/{stack_symbol}-> {to_state}")
            transition_count += 1

def read_iovpts_file(file):
    import logging
    logging.info(f'Began reading iovpts file')
    iovpts = IOVPTS()
    
    # Read file content from the file-like object
    content = file.read().decode("utf-8")  # Read and decode file content
    lines = [line.strip() for line in content.splitlines()]
    logging.info(lines)
    
    iovpts.calls = lines[0].split(',') if lines[0] else []
    iovpts.returns = lines[1].split(',') if lines[1] else []
    iovpts.internals = lines[2].split(',') if lines[2] else []
#    iovpts.internals = lines[2].split(',') if lines[2] else ['@']
    iovpts.input = lines[3].split(',') if lines[3] else []
    iovpts.output = lines[4].split(',') if lines[4] else []
    iovpts.stack_symbols = lines[5].split(',')
    states = lines[6].split(',')
    logging.info(states)

    for state in states:
        iovpts.add_state(state)
    logging.info(iovpts.states)

    transition_lines = lines[7:]
    for line in transition_lines:
        if line == "#":
            break
        parts = line.split(',')
        iovpts.add_transition(parts[0], parts[1], parts[2], parts[3])

    iovpts.set_initial_state(transition_lines[transition_lines.index("#") + 1])

    return iovpts
