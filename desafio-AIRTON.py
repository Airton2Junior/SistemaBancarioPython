import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(usuarios, /):
    cpf = input("Informe o cpf do usuario:")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n@@@ Usuario não cadastrado! @@@")
        return
    numero_conta = int(input("Informe o número da conta:"))
    conta = filtrar_conta(numero_conta, usuario)
    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"\tDepósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")


def sacar(*, usuarios, limite, limite_saques):
    cpf = input("Informe o cpf do usuario:")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n@@@ Usuario não cadastrado! @@@")
        return
    numero_conta = int(input("Informe o número da conta:"))
    conta = filtrar_conta(numero_conta, usuario)
    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return
    valor = float(input("Informe o valor do saque: "))
    if valor <= 0:
        print("\n@@@ Saque inválido! @@@")
        return
    if valor > limite:
        print("\n@@@ Saque superior ao limite! @@@")
        return
    if valor > conta["saldo"]:
        print("\n@@@ Saque superior ao saldo! @@@")
        return
    if conta["nro_saques"] +1 > limite_saques:
        print("\n@@@ Limite de saques atingido! @@@")
        return
    conta["saldo"] = conta["saldo"] - valor
    conta["nro_saques"] += 1
    conta["extrato"] += f"\tSaque:\t\tR$ {valor:.2f}\n"


def exibir_extrato(usuarios):
    cpf = input("Informe o cpf do usuario:")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n@@@ Usuario não cadastrado! @@@")
        return
    print("=" * 100)
    contas = usuario["contas"]
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t{conta['numero_conta']}
            Titular:\t{usuario['nome']}
            Saldo:\tR$ {conta['saldo']}
            Extrato:\n{conta['extrato']}
        """
        linha += ("=" * 100)
        print(textwrap.dedent(linha))


def criar_usuario(usuarios):
    cpf = input("Informe o cpf do usuario:")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n@@@ Usuario já cadastrado! @@@")
        return
    nome = input("Informe o nome completo:")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa):")
    endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado):")
    usuario = {"cpf": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco": endereco, "contas":[]}
    usuarios.append(usuario)
    print(f"=== Usuário ({usuario}) criado com sucesso! ===")


def filtrar_conta(numero_conta, usuario):
    # Retorna o primeiro usuário que possui o CPF informado ou None caso nenhum seja encontrado.
    contas = usuario["contas"]
    conta_filtrada = [conta for conta in contas if conta["numero_conta"] == numero_conta]
    return conta_filtrada[0] if conta_filtrada else None


def filtrar_usuario(cpf, usuarios):
    # Retorna o primeiro usuário que possui o CPF informado ou None caso nenhum seja encontrado.
    usuario_filtrado = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None


def criar_conta(agencia, usuarios):
    cpf = input("Informe o cpf do usuario:")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n@@@ Usuario não cadastrado! @@@")
        return
    contas = usuario["contas"]
    numero_conta = len(contas) + 1
    saldo = 0
    nro_saques = 0
    conta = {"agencia":agencia, "numero_conta":numero_conta, "saldo": saldo, "extrato": "", "nro_saques": nro_saques}
    contas.append(conta)
    print(f"=== Conta ({conta}) criada com sucesso! ===")

def listar_contas(usuarios):
    cpf = input("Informe o cpf do usuario:")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n@@@ Usuario não cadastrado! @@@")
        return
    contas = usuario["contas"]
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{usuario['nome']}
            Saldo:\tR$ {conta['saldo']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    AGENCIA = "0001"
    LIMITE = 500
    LIMITE_SAQUES = 3
    usuarios = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(usuarios)

        elif opcao == "s":
            sacar(
                usuarios=usuarios,
                limite=LIMITE,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(usuarios)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            criar_conta(AGENCIA, usuarios)

        elif opcao == "lc":
            listar_contas(usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
