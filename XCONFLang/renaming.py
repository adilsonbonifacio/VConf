from vpa import VPA

class Renaming:
    def __init__(self,vpa:VPA):
        self.calls = vpa.calls
        self.returns = vpa.returns
        self.internals = vpa.internals
        self.stack_symbols = vpa.stack_symbols
        self.states = vpa.states
        self.initial_state = vpa.initial_state
        self.finals = vpa.finals
        self.transitions = vpa.transitions

    #def renaming(intersecfinals1, intersectrans1):
    def renaming(self):

        transicoes = self.transitions
        states = self.states
        
#       Modifying the VPTS according to Theo. 6
#       emptying the stack after reaching a final state

        for f in self.finals:
            itrans = [f,"@","@","f1"]
            transicoes.append(itrans)
        self.internals.append("@")
        self.states.append("f1")

        for st in self.stack_symbols:
            if st!= '*':
                itrans = ['f1', 'b1', st, 'f1']
                transicoes.append(itrans)
        self.returns.append('b1')
        itrans = ['f1', 'b1', '*', 'f2']
        states.append("f2")
        transicoes.append(itrans)

#  eliminating pop moves on an empty stack 

        itrans = ["si","a2","Z2","si"]
        self.calls.append("a2")
        states.append("si")
        self.stack_symbols.append("Z2")
        transicoes.append(itrans)
        #itrans = ["si","@","@","s0"]
        itrans = ["si","@","@",self.initial_state]
        transicoes.append(itrans)

        for t in transicoes:
            if t[1] in self.returns and t[2]== '*':
                t[2] = "Z2"

################## Renaming the VPA model

        #str_estados = {estado: s+1 for s, estado in enumerate(states)}
        str_estados = {'si': 0 }
        s = 1
        for estado in states:
            if estado != 'si':
                str_estados[estado] = s
                s += 1 

        # for estado, novo_numero in str_estados.items():
        #     print(f"{estado} -> {novo_numero}")

        transicoes_renomeadas = []
        while transicoes != []:
            t = transicoes[0]
            source, input, stack, target = t
            transicoes.remove(t)
            
            # Renomeando os estados usando o mapa
            new_source = str_estados.get(source, source)
            new_target = str_estados.get(target, target)
            
            # Adicionando a transição com os estados renomeados
            transicoes_renomeadas.append((new_source, input, stack, new_target))

        return [str_estados,transicoes_renomeadas]
