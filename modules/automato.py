from .estado import Estado
from .transicao import Transicao
import re


class Automato:

    def __init__(self):
        self._states = {}
        self._final_states = {}
        self._transitions = []
        self._start_state = None
        self._log = False
        self._alfabeto_regex = ''

    def enableLogging(self):
        self._log = True

    def disableLogging(self):
        self._log = False

    def log(self, text: str):
        if self._log:
            print('LOG:', text)

    def setState(self, id: int, name: str, label: str = None):
        self._states[id] = Estado(id, name, label)
        self.log(f'Adicionando o {name} no automato.')

    def setFinalState(self, id: int):
        if self._states[id] is None:
            raise Exception('Adicione o estado antes de setar como final')

        self._final_states[id] = self._states[id]

        self.log(f'{self._states[id].getNome()} agora é final')

    def setStartState(self, id: int):
        if self._states[id] is None:
            raise Exception('Adicione o estado antes de setar como inicial')

        self._start_state = self._states[id]

        self.log(f'{self._states[id].getNome()} agora é inicial')

    def setTransition(self, origem: int, destino: int, simbolo: str):
        estado_origem = self._states[origem]
        estado_destino = self._states[destino]

        self._transitions.append(
            Transicao(estado_origem, estado_destino, simbolo))

        self.log((
            f'Transição do estado {origem} para {destino} '
            f'com simbolo "{simbolo}" criada'))

    def getTransition(self, origem: int, simbolo: str) -> Transicao:
        for transition in self._transitions:
            if transition.getOrigem().getId() == origem and \
               self.checkSymbol(transition.getSimbolo(), simbolo):
                return transition

        return None

    def getStartState(self) -> Estado:
        return self._start_state

    def getState(self, id: int) -> Estado:
        return self._states[id]

    def getFinalState(self, id: int) -> bool:
        return self._final_states[id]

    def setAlfabeto(self, alfabeto: str):
        self._alfabeto_regex = alfabeto

    def getAlfabeto(self) -> str:
        return self._alfabeto_regex

    def isStartState(self, id: int) -> bool:
        return self._states[id] == self._start_state

    def isFinalState(self, id: int) -> bool:
        return self._final_states.get(id) is not None

    def getFinalStateSize(self):
        return len(self._final_states)

    def checkIfInAlphabet(self, symbol: str):
        return Automato.checkSymbol(self._alfabeto_regex, symbol)

    def test(self, entrada: str) -> (bool, str):
        
        self.log('Iniciando teste')

        origem = self.getStartState()

        contador = -1  # Conta em qual posićão da string de entrada o autômato está. Utilizado no analizador lexico

        for posicao, letra in enumerate(entrada):
            contador += 1

            if not self.checkIfInAlphabet(letra):
                return (False, 'Caractere não está no alfabeto', contador)

            transicao = self.getTransition(origem.getId(), letra)

            # Nao encontrou a transicao
            if transicao is None:
                if self.isFinalState(origem.getId()):
                    self.log((
                        f'Fim do token '
                        f'\'{origem.getLabel()}\' na posicao \'{contador}\'. '
                        f'Estado atual: {origem.getNome()}.'))

                    return (True, origem.getLabel(), contador)
                else:
                    self.log((
                        f'Nao foi possivel encontrar uma transicao '
                        f'para a letra \'{letra}\' na posicao \'{contador}\'. '
                        f'Estado atual: {origem.getNome()}.'))
                    return (False, 'Erro Léxico', contador)

            destino = transicao.getDestino()

            self.log((
                f'{origem.getNome()} leu "{letra}" '
                f'foi para {destino.getNome()}'))

            origem = destino

        if not self.isFinalState(origem.getId()):
            return (False, 'Erro Léxico', contador)
        return (True, origem.getLabel(), contador)

    @staticmethod
    def checkSymbol(regex, symbol):
        return re.compile(regex).match(symbol) is not None

    @staticmethod
    def fromFile(path: str, logging=False):
        automato = Automato()

        if logging:
            automato.enableLogging()

        # Gerar automato de um arquivo preestabelecido
        tipo = -1

        with open(path, 'r') as fp:
            linhas = fp.readlines()

            for linha in linhas:
                linha = linha[:-1]

                if len(linha) == 0:
                    continue

                if linha.lower() == '[states]':
                    tipo = 0
                    continue

                elif linha.lower() == '[transitions]':
                    tipo = 1
                    continue

                elif linha.lower() == '[automata]':
                    tipo = 2
                    continue

                if tipo == 0:  # Estado
                    opcoes = linha.split(';')

                    id = int(opcoes[0])
                    name = opcoes[1]

                    automato.setState(id, name)

                    i = 2
                    while i < len(opcoes):
                        if opcoes[i].lower() == 'i':
                            automato.setStartState(id)
                        elif opcoes[i].lower() == 'f':
                            automato.setFinalState(id)
                            i += 1
                            label = opcoes[i]
                            automato.getState(id).setLabel(label)

                        i += 1

                elif tipo == 1:  # Transicao
                    opcoes = linha.split(';', 2)

                    origem = int(opcoes[0])
                    destino = int(opcoes[1])
                    symbol = opcoes[2]

                    automato.setTransition(origem, destino, symbol)

                elif tipo == 2:  # Automato
                    automato.setAlfabeto(linha)

        automato.disableLogging()
        return automato
