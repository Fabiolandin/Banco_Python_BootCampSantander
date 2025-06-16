menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
"""
valores = 0
saldo = 0
limite_saque = 500
numero_de_saques = 0
limite_de_saques = 3
extrato = []


while True:

    opcao = input(menu)

    if opcao == 'd':
        print("Deposito \n")
        valores = int(input('Quanto deseja depositar?'))
        if valores > 0:
            saldo = saldo + valores
            extrato.append(f'Depósito: R${valores:.2f}')
            print(f"Saldo {saldo}")

    elif opcao == 's':
        print("Saque \n")
        valores = int(input('Quanto deseja sacar?'))

        if valores > limite_saque or numero_de_saques > limite_de_saques or valores > saldo:
            print("Operação invalida")
            print(f"Saldo {saldo}")
        else:
            saldo = saldo - valores
            numero_de_saques = numero_de_saques + 1
            extrato.append(f'Saque: R${valores:.2f}')
            print(f"Saldo {saldo}")


    elif opcao == 'e':
        print("\n====== EXTRATO ======")
        if len(extrato) == 0:
            print("Nenhuma movimentação realizada.")
        else:
            for operacao in extrato:
                print(operacao)
        print(f"\nValor atual da conta R$ {saldo:.2f}")
        print("======================\n")

    elif opcao == 'q':
        print(f'Valor da conta R$ {saldo}')

        break