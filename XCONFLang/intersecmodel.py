import logging
import pandas as pd 
from copy import deepcopy
from compmodel import CompModel
from iovpts import IOVPTS
from vpa import VPA

class IntersecModel:
    def __init__(self, compmodel: CompModel, vpa: VPA):
        self.vpa = vpa
        self.compmodel = compmodel
        self.prod_setofstates = None
        self.prod_setoftrans = None
        self.prod_setofstacks = None
        self.prod_pu = None
        self.prod_po = None
        self.prod_inte = None
        self.prod_setoffinals = None
        self.prod_setofinitials = None
        self.productComputed = False 

    # Construct the product between two VPAs

    def _update_states_(self, transition1, transition2, prod_setofinitials, prod_setofstates,prod_setoffinals):
        """Atualiza o conjunto de estados com base nas transições."""
        if transition1[1]=='@':
            source = [transition1[0], transition2[0]]
            target = [transition1[3], transition2[0]]
        elif transition2[1]=='@':
            source = [transition1[0], transition2[0]]
            target = [transition1[0], transition2[3]]
        else:
            source = [transition1[0], transition2[0]]
            target = [transition1[3], transition2[3]]
        setoffinals1 = self.vpa.finals
        setoffinals2 = self.compmodel.finals
        setofinitials1 = self.vpa.initial_state
        setofinitials2 = self.compmodel.initial_state
        
        if not prod_setofstates:
            prod_setofstates.append(source)
            if source[0] in setoffinals1 and source[1] in setoffinals2 and source not in prod_setoffinals:
                prod_setoffinals.append(source)
            if source[0] in setofinitials1 and source[1] in setofinitials2 and source not in prod_setofinitials:
                prod_setofinitials.append(source)
            if source != target:
                prod_setofstates.append(target)
                if target[0] in setoffinals1 and target[1] in setoffinals2 and target not in prod_setoffinals:
                    prod_setoffinals.append(target)
                if target[0] in setofinitials1 and target[1] in setofinitials2 and target not in prod_setofinitials:
                    prod_setofinitials.append(target)
        else:
            if source not in prod_setofstates:
                prod_setofstates.append(source)
                if source[0] in setoffinals1 and source[1] in setoffinals2 and source not in prod_setoffinals:
                    prod_setoffinals.append(source)
                if source[0] in setofinitials1 and source[1] in setofinitials2 and source not in prod_setofinitials:
                    prod_setofinitials.append(source)
            if target not in prod_setofstates:
                prod_setofstates.append(target)
                if target[0] in setoffinals1 and target[1] in setoffinals2 and target not in prod_setoffinals:
                    prod_setoffinals.append(target)
                if target[0] in setofinitials1 and target[1] in setofinitials2 and target not in prod_setofinitials:
                    prod_setofinitials.append(target)

        return source, target
    
    def _update_transitions_(self, transition1, transition2, pu1, po1, inte1, prod_pu, prod_po, prod_inte, source, target):
        """Atualiza o conjunto de transições com base nas transições e conjuntos de estados."""
        if transition1[1]=='@' or transition1[2]=='*':
            newstack = [transition1[2], transition1[2]]
        elif transition2[1]=='@' or transition2[2]=='*':
            newstack = [transition2[2], transition2[2]]
        else:
            newstack = [transition1[2], transition2[2]]
        if transition1[1] in pu1 or transition1[1] in inte1:
            if transition1[1] in pu1 and not transition1[1] in prod_pu:
                prod_pu.append(transition1[1])
            if transition1[1] in inte1 and not transition1[1] in prod_inte:
                prod_inte.append(transition1[1])
            t = [source, transition1[1], newstack, target]
            if t not in self.prod_setoftrans: 
                self.prod_setoftrans.append(t)
        elif transition1[1] in po1:
            if not transition1[1] in prod_po:
                prod_po.append(transition1[1])
            if transition1[2] != '*' and transition2[2] != '*':
                t = [source, transition1[1], newstack, target]
                if t not in self.prod_setoftrans: 
                    self.prod_setoftrans.append(t)
            elif transition1[2] == '*' and transition2[2] == '*':
                t = [source, transition1[1], newstack, target]
                if t not in self.prod_setoftrans: 
                    self.prod_setoftrans.append(t)

    def compute_intersec(self):
        """Computa o produto (interserção) entre dois modelos (entre D e comp-otr(S) e entre F e otr(S)), e armazena o resultado."""
        pu1 = self.compmodel.calls
        po1 = self.compmodel.returns
        inte1 = self.compmodel.internals
        prod_pu = self.vpa.calls
        prod_po = self.vpa.returns
        prod_inte = self.compmodel.internals
        # pu2 = self.compmodel.calls
        # po2 = self.compmodel.returns
        # inte2 = self.compmodel.internals
        #setoffinals1 = self.transfmodel.finals
        setoftrans1 = self.vpa.transitions
        #setoffinals2 = self.compmodel.finals
        setoftrans2 = self.compmodel.transitions

        prod_setofstacks = []
        prod_setofstates = []
        prod_setoffinals = []
        prod_setofinitials = []
        self.prod_setoftrans = []

        logging.info(f"setoftrans1={setoftrans1}")
        logging.info(f"setoftrans2={setoftrans2}")
        
        df = pd.DataFrame(setoftrans2, columns=['state', 'event', 'stack_symbol', 'next_state'])
        for transition1 in setoftrans1:
            if transition1[1]!='@': 
                filtered_df = df[df['event'] == transition1[1]]
            else:
                filtered_df = df
            filtered_items = list(filtered_df.itertuples(index=False, name=None))

            for transition2 in filtered_items:
                if transition1[1]=='@' or transition1[2]=='*':
                    newstack = [transition1[2], transition1[2]]
                elif transition2[1]=='@' or transition2[2]=='*':
                    newstack = [transition2[2], transition2[2]]
                else:
                    newstack = [transition1[2], transition2[2]]
                if newstack not in prod_setofstacks:
                    prod_setofstacks.append(newstack)
        
                # Atualiza o conjunto de estados
                source, target = self._update_states_(transition1, transition2,  prod_setofinitials, prod_setofstates, prod_setoffinals)
                # Atualiza as transições
                self._update_transitions_(transition1, transition2, pu1, po1, inte1, prod_pu, prod_po, prod_inte, source, target)

        # Armazenando o resultado no atributo da classe
        self.productComputed = True
        self.prod_setofstates = prod_setofstates
        self.prod_setofstacks = prod_setofstacks
        self.prod_pu = prod_pu
        self.prod_po = prod_po
        self.prod_inte = prod_inte
        self.prod_setoffinals = prod_setoffinals
        self.prod_setofinitials = prod_setofinitials

    def save_intersec_info_to_list(self, list):
        list.append("\nThe set of initials for the intersection is:")
        list.append(self.prod_setofinitials)
        list.append("\nThe set of states for the intersection is:")
        list.append(self.prod_setofstates)
        list.append("\nThe set of transitions for the intersection is:")
        list.append(self.prod_setoftrans)
        list.append("\nThe set of finals for the intersection is:")
        list.append(self.prod_setoffinals)
        list.append("\nThe set of stack symbols for the intersection is:")
        list.append(self.prod_setofstacks)

def compute_estados(product: IntersecModel, compmodel:CompModel, vpa: VPA):
    newstates = deepcopy(product.prod_setofstates)
    newfinals = deepcopy(product.prod_setoffinals)
    newinitials = deepcopy(product.prod_setofinitials)

    inicial1 = compmodel.initial_state
    inicial2 = vpa.initial_state

    estados = {}
    finais = {}
    iniciais = {}
    s = 1
    savenewstates = deepcopy(newstates)
    f = len(savenewstates) - len(newfinals)
    while newstates:
        par = newstates[0]
        if (par[0] == inicial1 and par[1] == inicial2):
            estados[par[0], par[1]] = 0
            iniciais[par[0], par[1]] = 0
            newinitials.remove(par)
            newstates.remove(par)
            if (par in newfinals):
                    finais[par[0], par[1]] = 0
                    newfinals.remove(par)
        elif (par[0] == inicial2 and par[1] == inicial1):
            aux = inicial1
            inicial1 = inicial2
            inicial2 = aux
            estados[par[0], par[1]] = 0
            iniciais[par[0], par[1]] = 0
            newinitials.remove(par)
            newstates.remove(par)
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

def compute_pilha(product: IntersecModel):
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

def compute_transicoes(product: IntersecModel, iniciais, estados, pilha, finais):
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
        novatrans = [str(novoestado1), trans[1], str(novapilha1), str(novoestado2)]
        if novatrans not in transicoes:
            transicoes.append(novatrans)

    for inicio in newinitials:
        i1 = inicio[0]
        i2 = inicio[1]
        novoinicio = iniciais[i1,i2]
        if novoinicio not in novosiniciais:
            novosiniciais.append(novoinicio)

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
def save_intersec_vpa(vpa1: IntersecModel, str_iniciais, str_estados, transicoes, str_finais, str_pilha):
    import logging
    logging.info(f'Began to save a VPA that accepts the intersection between D and the complementation of S (comp-otr(S))')
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
    if str_estados != []: 
        vpa.initial_state = str_estados[0]
    else:
        vpa.initial_state = str_iniciais[0]
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
