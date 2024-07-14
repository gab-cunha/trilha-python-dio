import textwrap
from abc import ABC, abstractmethod

# Classes

class Cliente:
    def __init__(self):
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, dtNasc):
        super().__init__()
        self.cpf = cpf
        self.nome = nome
        self.dtNasc = dtNasc
    
    def __str__(self):
        return f"""\
            CPF: {self.cpf}
            Nome: {self.nome}
            Data de Nascimento: {self.dtNasc}
        """


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._agencia = "0001"
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        if (valor <= 0):
            print("Erro! Valor inválido para realizar o saque")
        elif (valor > saldo):
            print("Saldo insuficiente")
        else:
            self._saldo -= valor
            print("--- Saque realizado com sucesso! ---")
            return True
        return False

    def depositar(self, valor):
        if valor <= 0:
            print("Erro! Valor inválido para realizar o depósito") 
        else:
            self._saldo += valor
            print("+++ Depósito realizado com sucesso! +++")
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self.limite = 500
        self.limite_saques = 3
        
    def sacar(self, valor):
        num_saques = 0
        for t in self.historico.transacoes:
            if t["tipo"] == "Saque":
                num_saques += 1
        
        if (valor > self.limite):
            print(f"O valor do saque não pode ultrapassar R$ {self.limite:.2f}")
        elif (num_saques > self.limite_saques):
            print(f"Erro! Você já atingiu o limite de {self.limite_saques} saques diários")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
            Agência: {self.agencia}
            Número: {self.numero}
            cliente: {self.cliente.nome}
        """
            

class Historico:
    def __init__(self):
        self.transacoes = []
        
    def adicionar_transacao(self, transacao):
        self.transacoes.append({"tipo": transacao.__class__.__name__, "valor": transacao.valor})


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if (conta.sacar(self.valor)):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if (conta.depositar(self.valor)):
            conta.historico.adicionar_transacao(self)


# Funções

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)
    if not cliente:
        print("Nenhum cliente cadastrado com esse CPF")
        return
    
    if not cliente.contas:
        print("Esse cliente não tem nenhuma conta disponível")
        return
    else:
        conta = cliente.contas[0]
        if not conta:
            return
    
    valor = float(input("Informe o valor que deseja depositar na conta: "))
    transacao = Deposito(valor)
        
    cliente.realizar_transacao(conta, transacao)
        
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)
    if not cliente:
        print("Nenhum cliente cadastrado com esse CPF")
        return
    
    if not cliente.contas:
        print("Esse cliente não tem nenhuma conta disponível")
        return
    else:
        conta = cliente.contas[0]
        if not conta:
            return
        
    valor = float(input("Informe o valor que deseja sacar da conta: "))
    transacao = Saque(valor)
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)
    if not cliente:
        print("Nenhum cliente cadastrado com esse CPF")
        return
    
    if not cliente.contas:
        print("Esse cliente não tem nenhuma conta disponível")
        return
    else:
        conta = cliente.contas[0]
        if not conta:
            return

    print("========== Extrato ==========")
    for transacao in conta.historico.transacoes:
        if transacao['tipo'] == 'Saque':   
            print(f"\t- R$ {transacao['valor']:.2f}")
        elif transacao['tipo'] == 'Deposito':
            print(f"\t+ R$ {transacao['valor']:.2f}")
    print(f"Saldo:\tR$ {conta.saldo:.2f}")
    print("=============================")
                

def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    if (encontrar_cliente(cpf, clientes)):
        print("Um cliente com esse CPF já foi cadastrado")
        return
    
    nome = input("Informe o nome do cliente: ")
    dtNasc = input("Informe a data de nascimento (dd/mm/yyyy): ")
    cliente = PessoaFisica(cpf, nome, dtNasc)
    clientes.append(cliente)

def encontrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def listar_clientes(clientes):
    for cliente in clientes:
        print("=" * 100)        
        print(textwrap.dedent(str(cliente)))


def criar_conta(num_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente desejado para criar uma conta corrente: ")
    cliente = encontrar_cliente(cpf, clientes)
    if not cliente:
        print("Nenhum cliente cadastrado com esse CPF")
        return
    
    conta = ContaCorrente.nova_conta(numero=num_conta, cliente=cliente)
    contas.append(conta)
    cliente.adicionar_conta(conta)

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)        
        print(textwrap.dedent(str(conta)))

def menu(): 
    menu = """

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Novo cliente
    [5] Listar clientes
    [6] Nova conta
    [7] Listar contas
    [0] Sair

    => """
    return input(textwrap.dedent(menu))


def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()

        if opcao == "1":
            print(" === Depósito === ")
            depositar(clientes)

        elif opcao == "2":
            print(" === Saque === ")
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            listar_clientes(clientes)

        elif opcao == "6":
            num_conta = len(contas) + 1
            criar_conta(num_conta, clientes, contas)

        elif opcao == "7":
            listar_contas(contas)


        elif opcao == "0":
            break

        else:
            print("Operação inválida, favor selecionar a operação desejada novamente")

main()