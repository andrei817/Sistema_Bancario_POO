from abc import ABC, abstractmethod

class Conta:

    def __init__(self, numero, cliente, agencia="001"):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    

    def sacar(self, valor):
        if valor > self._saldo:
            print("Saldo insuficiente")
            return False

        self._saldo -= valor
        print("saque realizado com sucesso!")
        return True

    def depositar(self, valor):
        self._saldo += valor
        print("depósito realizado com sucesso!")
        return True

    def __str__(self):
        return f"""
    Agência: {self._agencia}
    Número: {self._numero}
    Saldo: R$ {self._saldo:.2f}
    """

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento

    def __str__(self):
        return f"""
    Nome: {self._nome}
    CPF: {self._cpf}
    Data de Nascimento: {self._data_nascimento}
    Endereço: {self._endereco}
    """


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacoes(self, tipo, valor):
        self.transacoes.append({
            "Tipo": tipo,
            "Valor": valor
        })

    def mostrar_transacoes(self):
        print("\n=== Histórico de Transações ===")
        for transacao in self.transacoes:
            print(f"{transacao['Tipo']}: R$ {transacao['Valor']:.2f}")
    
class Transacoes(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

# A classe deposito herda de trasação
class Deposito(Transacoes):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta._historico.adicionar_transacoes("Depósito", self.valor)

class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite, limite_saque):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque

    def sacar(self, valor):
        if valor > self._limite:
            print("Valor excede o limite permitido")
            return False
    
        return super().sacar(valor)


cliente = PessoaFisica(
    nome="Andrei",
    cpf="12345678900",
    data_nascimento="01-01-2000",
    endereco="Rua A"
)

conta = Conta(numero=1, cliente=cliente)
cliente.adicionar_conta(conta)

conta.depositar(500)
conta.sacar(200)


print(cliente)
print(conta)
conta._historico.mostrar_transacoes()