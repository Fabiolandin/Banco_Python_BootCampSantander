from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.__endereco = endereco
        self.__contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.__contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, conta, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.__cpf = cpf
        self.__nome = nome
        self.__data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self.__cpf

    @property
    def nome(self):
        return self.__nome

    @property
    def data_nascimento(self):
        return self.__data_nascimento

class Conta():
    def __init__(self, numero, cliente):
        self.__saldo = 0
        self.__numero = numero
        self.__agencia = "001"
        self.__cliente = cliente
        self.__historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self.__saldo
    
    @property
    def numero(self):
        return self.__numero

    @property
    def agencia(self):
        return self.__agencia
    
    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def historico(self):
        return self.__historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n @@@ Operação falhou! Você não tem saldo suficiente '_' ")
            return False
        
        elif valor > 0:
            self.__saldo -= valor
            print("\n === Saque realizado com sucesso!!!")
            return True
        
        else:
            print("\n @@@ Operação falhou! Você não tem saldo suficiente '_' ")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print("\n === Depósito realizado com sucesso!!!")
        else:
            print("\n @@@ Operação falhou! '_' ")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, saldo, numero, agencia, cliente, historico, limite=500, limite_saques=3):
        super().__init__(saldo, numero, agencia, cliente, historico)
        self.__limite = limite
        self.__limite_saques = limite_saques
    
    @property
    def limite(self):
        return self.__limite

    @property
    def limite_saques(self):
        return self.__limite_saques
    
    def sacar(self, valor):
        numero_saques = len([transcao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
                            )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n @@@ Operação falhou! '_' ")

        elif excedeu_saques:
            print("\n @@@ Operação falhou! '_' ")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência: \t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%M:%s"),
            }

        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

