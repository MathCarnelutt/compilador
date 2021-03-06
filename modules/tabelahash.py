from sys import stdout
import json

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, TabelaHash):
            newTable = []
            for i, item in enumerate(o.getTable()):
                if item is not None:
                    valor = {
                        'chave': i,
                        'item': item
                    }
                    newTable.append(valor);
            return {
                'tabela': newTable
            }

        return o.__dict__

class TabelaHash:

    def __init__(self, tamanho: int = 211, alpha: int = 10):
        self.__alpha = alpha
        self.__tamanho = tamanho
        self.__tabela = [None for i in range(tamanho)]

    def __setitem__(self, key, value):
        return self.addItem(key, value)

    def __getitem__(self, key):
        return self.getItem(key)

    def getTable(self):
        return self.__tabela

    def __hash(self, chave: str):
        h = 0

        for i, letra in enumerate(chave):
            h = self.__alpha * h + ord(letra)

        return h % self.__tamanho

    def getPos(self, chave: str):
        return self.___hash(chave)

    def print(self, filesrc=stdout, print_none=True):
        json.dump(self, filesrc, cls=MyEncoder, indent=4, sort_keys=True)

    def addItem(self, key, value):
        if type(key) != str:
            raise TypeError('Tipo da chave utilizada deve ser uma string.')

        posicao = self.__hash(key)

        item = {
            'chave': key,
            'valor': value
        }

        if self.__tabela[posicao] is None:
            self.__tabela[posicao] = [item]
            return posicao

        else:
            # Foda-se se ja tem item com mesma chave na tabela
            # for item in self.__tabela[posicao]:
            #     if item['chave'] == key:
            #         raise KeyError('Chave já existente')

            self.__tabela[posicao].append(item)
            return posicao

    def getItem(self, key):
        if type(key) != str:
            raise TypeError('Tipo da chave utilizada deve ser uma string.')

        posicao = self.__hash(key)

        if self.__tabela[posicao] is not None:
            for item in self.__tabela[posicao]:
                if item['chave'] == key:
                    return item

            raise KeyError('Chave nao encontrada')
        raise KeyError('Chave nao encontrada')

    def getItemValue(self, key):
        if type(key) != str:
            raise TypeError('Tipo da chave utilizada deve ser uma string.')

        posicao = self.__hash(key)

        if self.__tabela[posicao] is not None:
            for item in self.__tabela[posicao]:
                if item['chave'] == key:
                    return item['value']

            raise KeyError('Chave nao encontrada')
        raise KeyError('Chave nao encontrada')

if __name__ == '__main__':
    tabela = TabelaHash()

    tabela['teste'] = 'teste'
    tabela['matheus'] = 'matheus'
    tabela['daniel'] = 'daniel'
    tabela['verdade'] = 'verdade'
    tabela['bob'] = 'bob'

    with open('arquivo.txt', 'w') as arquivo:
        tabela.print(arquivo, False)
