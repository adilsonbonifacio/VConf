import logging

class BalancedRunChecker:
    def __init__(self, push, pop, internal, original_states, states, transitions, start_state, end_state):
        """
        Initializes the vectors V, In, Out, and R, and the transition matrix based on the automaton definition.
        """
        self.push = push
        self.pop = pop
        self.internal = internal
        self.states = states
        self.transitions = transitions
        self.original_states = original_states

        # self.indice = {}
        # s = 0
        # for i in states:
        #     self.indice[i] = s
        #     s += 1

        self.V = []
        self.In = [[] for _ in range(len(self.states))]
        self.Out = [[] for _ in range(len(self.states))]
        self.R = [[[] for _ in range(len(self.states))] for _ in range(len(self.states))]
        self.str_global = []  # Store the balanced run string
        
        self.si = start_state
        self.se = end_state

        self._initialize_vectors_()

    def _initialize_vectors_(self):
        """
        Initialize the vectors based on the push, pop, internal transitions, and states.
        """

        for dic_p in self.states:
            p = self.states.get(dic_p)
            for t in self.transitions:
                if t[0] == p:
                    if (t[1] in self.internal) and (t[3] != p) and not self.R[t[0]][t[3]]:
                        self.R[t[0]][t[3]].append(f"{t[0]};{t[1]};{t[3]}")
                        self.V.append([t[0], t[3]])
                    elif t[1] in self.pop:
                        self.Out[p].append(f"{t[1]};{t[2]};{t[3]}")
                    else:
                        q = t[3]
                        #self.In[self.indice[q]].append(f"{t[0]};{t[1]};{t[2]}")
                        self.In[q].append(f"{t[0]};{t[1]};{t[2]}")
                        for r in self.transitions:
                            if q == r[0] and (t[2] == r[2]) and (r[1] in self.pop) and (t[0] != r[3]) and not self.R[t[0]][r[3]]:
                                self.R[t[0]][r[3]].append(f"{t[1]};{r[0]};{r[0]};{r[1]}")
                                self.V.append([t[0], r[3]])
                            # if q == r[0]:
                                # if (t[2] == r[2]) and (r[1] in self.pop) and (t[0] != r[3]) and not self.R[self.indice[t[0]]][self.indice[r[3]]]:
                                #     self.R[self.indice[t[0]]][self.indice[r[3]]].append(f"{t[1]};{r[0]};{r[0]};{r[1]}")
                                #     self.V.append([t[0], r[3]])

    def _get_balanced_run_string_(self, si, se, R, pu, po, inte, setofstates):
        """
        Recursive function that builds the string corresponding to a balanced run.
        """

        
        # Get the first valid transition between si and se
        tripla = R[int(si)][int(se)]
        p = tripla[0].split(";")  # Parse the first valid transition

        # Process transitions based on their length
        if len(p) == 3:
            p1, p2, p3 = p
        else:
            p1, p2, p3, p4 = p

        # Handling for 3-part transition
        if len(p) == 3:
            if p2 in pu or p2 in po or p2 in inte:
                # print("Entrou aqui?", p2)
                print(p2)
                self.str_global.append(p2)  # Append to global string
            elif int(p2) in setofstates.values():
                # Recursively handle transitions
                self._get_balanced_run_string_(si, p2, R, pu, po, inte, setofstates)
                self._get_balanced_run_string_(p2, se, R, pu, po, inte, setofstates)

        # Handling for 4-part transition
        else:
            if p2 != p3:
                print(p1)
                self.str_global.append(p1)  # Append the first part of the transition
                self._get_balanced_run_string_(p2, p3, R, pu, po, inte, setofstates)  # Recursive call for the middle part
                print(p4)
                self.str_global.append(p4)  # Append the last part of the transition
            else:
                print(p1)
                self.str_global.append(p1)  # Append the first part of the transition
                print(p4)
                self.str_global.append(p4)  # Append the last part of the transition

        return ','.join(self.str_global)  # Join the list into a single string
    
    def check_balanced_run(self):
        """
        Main function that checks if a balanced run exists from start_state (si) to end_state (se).
        """
        #while self.V and not self.R[str(self.si)][str(self.se)]:
        while self.V and not self.R[self.si][self.se]:
            par = self.V.pop(0)
            p = par[0]
            q = par[1]

            for dic_s in self.states:
                s = self.states.get(dic_s)
                if self.R[s][p] and s != q and not self.R[s][q]:
                    self.R[s][q].append(f"{s};{p};{q}")
                    self.V.append([s, q])

            for dic_t in self.states:
                t = self.states.get(dic_t)
                if self.R[q][t] and p != t and not self.R[p][t]:
                    self.R[p][t].append(f"{p};{q};{t}")
                    self.V.append([p, t])

            for tr1 in self.In[p]:
                s, a, Z = tr1.split(";")
                for tr2 in self.Out[q]:
                    b, W, t = tr2.split(";")
                    if Z == W and s != t and not self.R[int(s)][int(t)]:
                        self.R[int(s)][int(t)].append(f"{a};{p};{q};{b}")
                        self.V.append([int(s), int(t)])

        
        
        try:
            # If no invalid run found
            if len(self.R[self.si][self.se]) == 0 and not self.R[self.si][self.se]:
                return False, ""
            else:
                # If invalid run found, build the string representing it
                # mystring = "Um caso de teste que mostra essa condição é: " + self._get_balanced_run_string_(self.si, self.se, self.R, self.push, self.pop, self.internal, self.states)
                mystring = self._get_balanced_run_string_(self.si, self.se, self.R, self.push, self.pop, self.internal, self.states)
                return True, mystring
        except:
            return True, "Problema de sincronização dos modelos"
