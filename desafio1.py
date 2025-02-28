''' 
Para ler e escrever dados em Python, utilizamos as seguintes funções: 
- input: lê UMA linha com dado(s) de Entrada do usuário;
- print: imprime um texto de Saída (Output), pulando linha.  
'''

class ContaBancaria:
    # TODO: Inicialize a conta bancária com o nome do titular, saldo 0 e  liste para armazenar as operações realizadas:
    def __init__(self, titular):
        self._titular = titular
        self._saldo = 0
        self._operacoes = []

    # TODO: Implemente o método para realizar um depósito, adicione o valor ao saldo e registre a operação:
    def depositar(self, valor):
      self._saldo += valor
      self._operacoes.append('+'+str(valor))

    # TODO: Implemente o método para realizar um saque:
    def sacar(self, valor):
        # TODO: Verifique se há saldo suficiente para o saque
        if (self._saldo > 0 and self._saldo >= -valor): 
            # TODO: Subtraia o valor do saldo (valor já é negativo)
            self._saldo += valor
            self._operacoes.append(str(valor))
        elif (valor == 0):
            self._operacoes.append(str(valor))
        else:
            # TODO: Registre a operação e retorne a  mensagem de saque negado
            self._operacoes.append("Saque não permitido")

    # TODO: Crie o método para exibir o extrato da conta e junte as operações no formato correto:
    def extrato(self):
      texto = "Operações: "
      texto += ', '.join(self._operacoes)
      texto += "; Saldo: "+ str(self._saldo)
      print(texto)

nome_titular = input().strip()  
conta = ContaBancaria(nome_titular)  

entrada_transacoes = input().strip() 
transacoes = [int(valor) for valor in entrada_transacoes.split(",")]  

for valor in transacoes:
    if valor > 0:
        conta.depositar(valor)  
    else:
        conta.sacar(valor)  

conta.extrato()