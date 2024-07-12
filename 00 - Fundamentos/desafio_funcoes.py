import textwrap

def menu(): 
    menu = """

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Cadastrar usuário
    [5] Listar usuários
    [6] Criar conta corrente
    [7] Listar contas
    [0] Sair

    => """
    return input(textwrap.dedent(menu))


# positional only
def depositar(saldo, valor, extrato, /):
    if valor <= 0:
        print("Valor inválido para realizar o depósito!") 
    else:
        saldo += valor
        extrato += f" + R$ {valor:.2f}\n"
        print("+++ Depósito realizado com sucesso! +++")
        
    return saldo, extrato

# keyword only
def sacar(*, saldo, valor, extrato, limite, num_saques):
    if (valor > saldo):
        print("Saldo insuficiente")
    elif (valor > limite):
        print("O valor não pode ultrapassar R$ 500.00")
    else:
        num_saques += 1
        saldo -= valor
        extrato += f" - R$ {valor:.2f}\n"
        print("--- Saque realizado com sucesso! ---")
    
    return num_saques, saldo, extrato

# positional only (saldo) e keyword only (extrato)
def exibir_extrato(saldo, /, *, extrato):
    print("_____ Extrato _____")
    print(extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF do usuário: ")
    if (encontrar_usuario(cpf, usuarios)):
        print("Um usuário com esse CPF já foi cadastrado")
        return
    
    nome = input("Informe o nome do usuário: ")
    dtNasc = input("Informe a data de nascimento (dd/mm/yyyy): ")
    usuarios.append({"cpf": cpf, "nome": nome, "dtNasc": dtNasc})
    print(" !! Usuário criado com sucesso !! ")

def encontrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def listar_usuarios(usuarios):
    t = ""
    for usuario in usuarios:
        t += f" CPF: {usuario["cpf"]} -\tNome: {usuario["nome"]},\tData de Nascimento: {usuario["dtNasc"]}"
        t += "\n"
    print(t)

def criar_contaCorrente(agencia, contas, usuarios):
    cpf = input("Informe o CPF do usuário desejado para criar uma conta corrente: ")
    usuario = encontrar_usuario(cpf, usuarios)
    if not usuario:
        print("Nenhum usuário cadastrado com esse CPF")
        return
    
    num_conta = len(contas) + 1
    contas.append({"agencia": agencia, "num_conta": num_conta, "usuario": usuario})
    print(" !!! Conta criada com sucesso !!! ")


def listar_contas(contas):
    t = ""
    for conta in contas:
        t += f"- Agência: {conta["agencia"]},\tNúmero: {conta["num_conta"]},\tUsuário: {conta["usuario"]["nome"]}"
        t += "\n"
    print(t)

 
def main():
    AGENCIA = "0001"
    LIMITE_SAQUES = 3

    saldo = 0
    limite = 500
    extrato = ""
    num_saques = 0
    valor = 0

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            print(" === Depósito === ")
            valor = float(input("Informe o valor que deseja depositar na conta: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            print(" === Saque === ")
            if (num_saques == LIMITE_SAQUES):
                print("Erro! Você já atingiu o limite de 3 saques diários")
            else:
                valor = float(input("Informe o valor que deseja sacar na conta: "))
                num_saques, saldo, extrato = sacar(
                                        saldo=saldo, valor=valor, extrato=extrato, 
                                        limite=limite, num_saques=num_saques
                                    )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            listar_usuarios(usuarios)

        elif opcao == "6":
            criar_contaCorrente(AGENCIA, contas, usuarios)

        elif opcao == "7":
            listar_contas(contas)


        elif opcao == "0":
            break

        else:
            print("Operação inválida, favor selecionar a operação desejada novamente")

main()