import logging
from copy import deepcopy
from vpa import VPA

class UnionModel:
    def __init__(self, vpa1:VPA, vpa2: VPA):
        self.vpa1 = vpa1
        self.vpa2 = vpa2
        self.prod_setofstates = None
        self.prod_setoftrans = None
        self.prod_setofstacks = None
        self.prod_pu = None
        self.prod_po = None
        self.prod_inte = None
        self.prod_setoffinals = None
        self.prod_setofinitials = None
        self.productComputed = False 


    # Construct the union between two VPAs

    #def unionmodel(pu1, po1, inte1, setoffinals1, setoftrans1, setoffinals2, setoftrans2):
    def compute_union(self):
        pu1 = self.vpa1.calls
        po1 = self.vpa1.returns
        inte1 = self.vpa1.internals
        prod_pu = self.vpa2.calls
        prod_po = self.vpa2.returns
        prod_inte = self.vpa1.internals
        # pu2 = self.compmodel.calls
        # po2 = self.compmodel.returns
        # inte2 = self.compmodel.internals
        setoffinals1 = self.vpa1.finals
        setoftrans1 = self.vpa1.transitions
        setoffinals2 = self.vpa2.finals
        setoftrans2 = self.vpa2.transitions

        prod_setofstacks = []
        prod_setofstates = []
        prod_setofinitials = []
        prod_setoffinals = []
        prod_setoftrans = []
        for t1 in setoftrans1:
            for t2 in setoftrans2:
                if t1[1] == t2[1]:
                    source = []
                    target = []
                    newstack = []
                    newstack = [t1[2], t2[2]]
                    if not newstack in prod_setofstacks:
                        prod_setofstacks.append(newstack)
                    if prod_setofstates == []:
                        source = [t1[0], t2[0]]
                        target = [t1[3], t2[3]]
                        if source == target:
                            prod_setofstates.append(source)
                        else:
                            prod_setofstates.append(source)
                            prod_setofstates.append(target)
                    else:
                        add_source = 1
                        add_target = 1
                        for par in prod_setofstates:
                            if (t1[0] == par[0] and t2[0] == par[1]):
                                source = [t1[0], t2[0]]
                                add_source = 0
                            # elif (t2[0] == par[0] and t1[0] == par[1]):
                            #     source = [par[0], par[1]]
                            #     add_source = 0
                            if (t1[3] == par[0] and t2[3] == par[1]):
                                target = [t1[3], t2[3]]
                                add_target = 0
                            # elif (t2[3] == par[0] and t1[3] == par[1]):
                            #     target = [par[0], par[1]]
                            #     add_target = 0

                        if add_source != 0:
                            source = [t1[0], t2[0]]
                            if source not in prod_setofstates:
                                prod_setofstates.append(source)
                                if source[0] in setoffinals1 or source[1] in setoffinals2 and source not in prod_setoffinals:
                                    prod_setoffinals.append(source)
                                # if source[0] == initial1 and source[1] == initial2 and source not in prod_setofinitials:
                                #     prod_setofinitials.append(source)
                        if add_target != 0:
                            target = [t1[3], t2[3]]
                            if target not in prod_setofstates:
                                prod_setofstates.append(target)
                                if target[0] in setoffinals1 or target[1] in setoffinals2 and target not in prod_setoffinals:
                                    prod_setoffinals.append(target)
                                # if target[0] == initial1 and target[1] == initial2 and target not in prod_setofinitials:
                                #     prod_setofinitials.append(target)

                    if (t1[1] in pu1) or (t1[1] in inte1):
                        if (t1[1] in pu1) and not t1[1] in prod_pu:
                            prod_pu.append(t1[1])
                        if (t1[1] in inte1) and not t1[1] in prod_inte:
                            prod_inte.append(t1[1])
                        t = [source, t1[1], newstack, target]
                        prod_setoftrans.append(t)
                    elif (t1[1] in po1):
                        if not t1[1] in prod_po:
                            prod_po.append(t1[1])
                        if (t1[2] != '*' and t2[2] != '*'):
                            t = [source, t1[1], newstack, target]
                            prod_setoftrans.append(t)
                            # print(prod_setoftrans)
                        elif (t1[2] == '*' and t2[2] == '*'):
                            t = [source, t1[1], newstack, target]
                            prod_setoftrans.append(t)
                    # elif (t1[1] in po1) :
                    # move tau does not implemented


        # Armazenando o resultado no atributo da classe
        self.productComputed = True
        self.prod_setofstates = prod_setofstates
        self.prod_setofstacks = prod_setofstacks
        self.prod_pu = prod_pu
        self.prod_po = prod_po
        self.prod_inte = prod_inte
        #self.prod_setofinitials = [initial1, initial2] #prod_setofinitials
        self.prod_setoffinals = prod_setoffinals
        self.prod_setofinitials = prod_setofinitials
        self.prod_setoffinals = prod_setoffinals
        self.prod_setoftrans = prod_setoftrans

        # return [prod_setofstates, prod_setoffinals, prod_setoftrans, prod_setofstacks]


def compute_estados(product: UnionModel, vpa1: VPA, vpa2: VPA):
    newstates = deepcopy(product.prod_setofstates)
    newfinals = deepcopy(product.prod_setoffinals)
    iniciais = deepcopy(product.prod_setofinitials)

    inicial1 = vpa1.initial_state
    inicial2 = vpa2.initial_state

    estados = {}
    finais = {}
    iniciais = {}
    s = 1
    savenewstates = deepcopy(newstates)
    f = len(savenewstates) - len(newfinals)

    while newstates:
        par = newstates[0]
        #print(par)
        if (par[0] == inicial1 and par[1] == inicial2):
            estados[par[0], par[1]] = 0
            newstates.remove(par)
            iniciais[par[0], par[1]] = 0
            #newinitials.remove(par)
            if (par in newfinals):
                    finais[par[0], par[1]] = 0
                    newfinals.remove(par)
        elif (par[0] == inicial2 and par[1] == inicial1):
            aux = inicial1
            inicial1 = inicial2
            inicial2 = aux
            estados[par[0], par[1]] = 0
            newstates.remove(par)
            iniciais[par[0], par[1]] = 0
            #newinitials.remove(par)
            if (par in newfinals):
                    finais[par[0], par[1]] = 0
                    newfinals.remove(par)
        elif (par in newfinals):
            estados[par[0], par[1]] = f
            finais[par[0], par[1]] = f
            newstates.remove(par)
            newfinals.remove(par)
            f += 1
        else:
            if par[1] == par[0]:
                estados[par[0], par[1]] = s
                newstates.remove(par)
                s += 1
            else:
                estados[par[0], par[1]] = s
                s += 1
                newstates.remove(par)

    return iniciais, estados, finais

def compute_pilha(product: UnionModel):
    newstacks = deepcopy(product.prod_setofstacks)
    pilha = {}
    i = 0
    while newstacks:
        par_pilha = newstacks[0]
        newstacks.remove(par_pilha)
        if par_pilha not in newstacks:
            if par_pilha[0]=='*' and par_pilha[1]=='*':
                pilha[par_pilha[0], par_pilha[1]] = '*'
            elif par_pilha[0]=='@' and par_pilha[1]=='@':
                pilha[par_pilha[0], par_pilha[1]] = '@'
            else:
                pilha[par_pilha[0], par_pilha[1]] = i
                i += 1
                
    return pilha

def compute_transicoes(product: UnionModel, iniciais, estados, pilha, finais):
    newtrans = product.prod_setoftrans
    #newstates = product.prod_setofstates
    newfinals = product.prod_setoffinals
    newinitials = product.prod_setofinitials
    novosestados = []
    transicoes = []
    novapilha = []
    novosfinais = []
    novosiniciais = []
    logging.info(f"newtrans={newtrans}")
    logging.info(f"estados={iniciais}")
    logging.info(f"estados={estados}")
    logging.info(f"finais={finais}")
    logging.info(f"pilha={pilha}")
    
    for trans in newtrans:
        sq = trans[0]
        pr = trans[3]
        s = sq[0]
        q = sq[1]
        p = pr[0]
        r = pr[1]
        st = trans[2]
        Z = st[0]
        W = st[1]
        
        novoestado1 = estados[s, q]
        novoestado2 = estados[p, r]
        novapilha1 = pilha[Z,W]
        if novoestado1 not in novosestados:
            novosestados.append(novoestado1)
        if novoestado2 not in novosestados:
            novosestados.append(novoestado2)
        if novapilha1 not in novapilha:
            novapilha.append(novapilha1)
        #novatrans = [str(novoestado1), trans[1], str(pilha[Z, W]), str(novoestado2)]
        novatrans = [str(novoestado1), trans[1], str(novapilha1), str(novoestado2)]
        if novatrans not in transicoes:
            transicoes.append(novatrans)

    novosiniciais = newinitials

    for final in newfinals:
        f1 = final[0]
        f2 = final[1]
        novofinal = finais[f1,f2]
        if novofinal not in novosfinais:
            novosfinais.append(novofinal)

    str_iniciais = [str(s) for s in novosiniciais]
    str_estados = [str(s) for s in novosestados]
    str_finais = [str(s) for s in novosfinais]
    str_pilha = [str(s) for s in novapilha]

    return novosiniciais, novosestados, novosfinais, transicoes, str_iniciais, str_estados, str_finais, str_pilha

#def save_intersec_vpa(vpa1: IntersecModel, novosestados, transicoes, novosfinais, str_pilha):
def save_union_vpa(vpa1: UnionModel, str_iniciais, str_estados, transicoes, str_finais, str_pilha):
    import logging
    logging.info(f'Began to save a VPA that accepts the union between non-blocking VPAs for D cap comp-otr(S) and F cap otr(S)')
    vpa = VPA()
    vpa.calls = vpa1.prod_pu
    vpa.returns = vpa1.prod_po
    vpa.internals = vpa1.prod_inte
    #vpa.stack_symbols = pilha
    vpa.stack_symbols = str_pilha
    vpa.states = str_estados
    vpa.transitions = transicoes
    vpa.initial_state = str_iniciais
    vpa.finals = str_finais
    vpa.initial_state = str_estados[0]

    return (vpa)

def save_dictionaries_info_to_list(iniciais, estados, str_estados, finais, str_finais, pilha, str_pilha, transicoes, list):
    list.append("\nDicionários dos estados iniciais da intersecção:")
    list.append(iniciais)
    list.append("\nDicionários dos estados da intersecção:")
    list.append(estados)
    list.append("\nEstados da intersecção por índices:")
    list.append(str_estados)
    list.append("\nDicionários dos estados finais da intersecção:")
    list.append(finais)
    list.append("\nEstados finais da intersecção por índices:")
    list.append(str_finais)
    list.append("\nDicionários dos símbolos de pilha da intersecção:")
    list.append(pilha)
    list.append("\nSímbolos de pilha da intersecção por índices:")
    list.append(str_pilha)

    # list.append("\nEstados finais da intersecção por índices:")
    # list.append(str_finais)
    list.append("\nTransições da intersecção por índices:")
    for tr in transicoes:
        list.append("t"+str(transicoes.index(tr))+": "+tr[0]+" --"+tr[1]+"/"+tr[2]+"-> "+tr[3])
