import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

AGENCIA = "0001"
LIMITE = 500
LIMITE_SAQUES = 3

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


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def contas(self):
        return self._contas

    def __str__(self):
        pass


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf
    
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def data_nascimento(self):
        return self._data_nascimento
    
    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf
    
    def __str__(self):
        return f"{self._nome} - {self._data_nascimento} - {self._cpf} - {self._endereco}"

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero_saques = 0
        self._numero = numero
        global AGENCIA
        self._agencia = AGENCIA
        self._cliente = cliente
        self._historico = Historico()      

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero_saques(self):
        return self._numero_saques

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
            return False
        else:
            self._saldo -= valor
            self._numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False
        else:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        return True
    
    def __str__(self):
        return f"Conta: {self._numero} - Agência: {self._agencia} - Saldo: {self._saldo}"

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
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "transacao": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data/hora": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def __str__(self):
        return "\n".join(
            f"{transacao['transacao']} - \tR$ {transacao['valor']:.2f} - \t{transacao['data/hora']}"
            for transacao in self._transacoes
        )

def depositar(clientes):
    cpf = input("Informe o cpf do cliente:")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ cliente não cadastrado! @@@")
        return
    numero_conta = int(input("Informe o número da conta:"))
    conta = filtrar_conta(numero_conta, cliente)
    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return
    valor = float(input("Informe o valor do depósito: "))
    deposito = Deposito(valor)
    cliente.realizar_transacao(conta, deposito)    

def sacar(clientes):
    cpf = input("Informe o cpf do cliente:")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ cliente não cadastrado! @@@")
        return
    numero_conta = int(input("Informe o número da conta:"))
    conta = filtrar_conta(numero_conta, cliente)
    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return
    global LIMITE_SAQUES
    if conta.numero_saques+1 > LIMITE_SAQUES:
        print("\n@@@ Limite de saques atingido! @@@")
        return
    valor = float(input("Informe o valor do saque: "))
    global LIMITE
    if valor > LIMITE:
        print("\n@@@ Saque superior ao limite! @@@")
        return
    saque = Saque(valor)
    cliente.realizar_transacao(conta, saque)    
    


def exibir_extrato(clientes):
    cpf = input("Informe o cpf do cliente:")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ cliente não cadastrado! @@@")
        return
    print("\n================ EXTRATO ================")
    contas = cliente.contas
    for conta in contas:
        linha = f"""\
            Agência:\t{conta.agencia}
            C/C:\t{conta.numero}
            Titular:\t{cliente.nome}
            Saldo:\tR$ {conta.saldo:.2f}
            Histórico:\n{conta.historico}
        """
        linha += ("=" * 100)
        print(textwrap.dedent(linha))


def criar_cliente(clientes):
    cpf = input("Informe o cpf do cliente:")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\n@@@ cliente já cadastrado! @@@")
        return
    nome = input("Informe o nome completo:")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa):")
    endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado):")
    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)
    print(f"=== Usuário ({cliente}) criado com sucesso! ===")


def filtrar_conta(numero_conta, cliente):
    # Retorna o primeiro usuário que possui o CPF informado ou None caso nenhum seja encontrado.
    contas = cliente.contas
    conta_filtrada = [conta for conta in contas if conta.numero == numero_conta]
    return conta_filtrada[0] if conta_filtrada else None


def filtrar_cliente(cpf, clientes):
    # Retorna o primeiro usuário que possui o CPF informado ou None caso nenhum seja encontrado.
    cliente_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrado[0] if cliente_filtrado else None


def criar_conta(clientes):
    cpf = input("Informe o cpf do cliente:")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ cliente não cadastrado! @@@")
        return
    contas = cliente.contas
    numero_conta = len(contas) + 1
    conta = Conta.nova_conta(cliente, numero_conta)
    cliente.adicionar_conta(conta)
    print(f"=== Conta ({conta}) criada com sucesso! ===")

def listar_contas(clientes):
    cpf = input("Informe o cpf do cliente:")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ cliente não cadastrado! @@@")
        return
    contas = cliente.contas
    for conta in contas:
        print("=" * 100)
        print(f"Agência:\t{conta.agencia}")
        print(f"C/C:\t{conta.numero}")
        print(f"Saldo:\tR$ {conta.saldo:.2f}")


def main():
    clientes = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes=clientes)

        elif opcao == "s":
            sacar(clientes=clientes)

        elif opcao == "e":
            exibir_extrato(clientes=clientes)

        elif opcao == "nu":
            criar_cliente(clientes=clientes)

        elif opcao == "nc":
            criar_conta(clientes=clientes)

        elif opcao == "lc":
            listar_contas(clientes=clientes)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
