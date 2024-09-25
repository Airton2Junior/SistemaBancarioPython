menu = """

[d] Depositar
[s] Sacar
[p] Saldo
[e] Extrato
[q] Sair

=> """

saldo = 0
extrato = ""
numero_saques = 0
LIMITE = 500
LIMITE_SAQUES = 3


def efetuar_deposito():
    global saldo
    global extrato

    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito de R$ {valor:.2f}\n"

def efetuar_saque():
    global saldo
    global extrato
    global numero_saques
    global LIMITE
    global LIMITE_SAQUES

    valor = float(input("Informe o valor do saque: "))

    if valor > LIMITE:
        print("Valor superior ao limite máximo de saque.")
        return

    if numero_saques >= LIMITE_SAQUES:
        print("Número máximo de saques atingido.")
        return

    if valor > 0 and valor <= saldo:
        saldo -= valor
        extrato += f"Saque de R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operação inválida, por favor tente novamente.")

def exibir_saldo():
    print(f"\nSaldo: R$ {saldo:.2f}")

def exibir_extrato():
    print("\n================ EXTRATO ================")
    print(extrato)

while True:

    opcao = input(menu)

    if opcao == "d":
        efetuar_deposito()
    elif opcao == "s":
        efetuar_saque()
    elif opcao == "p":
        exibir_saldo()
    elif opcao == "e":
        exibir_extrato()
    elif opcao == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
