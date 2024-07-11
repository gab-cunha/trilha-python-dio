menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> """

saldo = 0
limite = 500
extrato = ""
num_depositos = 0
num_saques = 0
LIMITE_SAQUES = 3
valor = 0

while True:
    opcao = input(menu)

    if opcao == "1":
        print(" -- Depósito -- ")
        valor = int(input("Informe o valor que deseja depositar na conta: "))
        if valor <= 0:
            print("Valor inválido para realizar o depósito!") 
        else:
            num_depositos += 1
            saldo += valor
            extrato += f"+ R$ {valor:.2f}\n"


    elif opcao == "2":
        print(" -- Saque -- ")
        if (num_saques == LIMITE_SAQUES):
            print("Erro! Você já atingiu o limite de 3 saques diários")
        else:
            valor = int(input("Informe o valor que deseja sacar na conta: "))
            if (valor > saldo):
                print("Saldo insuficiente")
            elif (valor > limite):
                print("O valor não pode ultrapassar R$ 500.00")
            else:
                num_saques += 1
                saldo -= valor
                extrato += f"- R$ {valor:.2f}\n"


    elif opcao == "3":
        print("==== Extrato ====")
        extrato += f"Saldo: R$ {saldo:.2f}"
        print(extrato)

    elif opcao == "0":
        break

    else:
        print("Operação inválida, favor selecionar a operação desejada novamente")