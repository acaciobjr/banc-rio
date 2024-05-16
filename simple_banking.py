import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

menu = 'Digite:\n- [d] para Depositar\n- [s] para Sacar\n- [e] para ver o Extrato\n- [o] para Sair\n'
saldo = 0
transacoes = []
saques_hoje = 0

def deposito():
    global saldo, transacoes
    while True:
        try:
            valor = int(input('Qual valor deseja depositar? R$ '))
            if valor < 0:
                print('A operação se trata de um depósito. Favor utilize um valor positivo.')
                continue
            saldo += valor
            transacoes.append((locale.currency(valor), 'Depósito'))
            print('Depósito realizado com sucesso.')
            break
        except ValueError:
            print('Por favor, digite um número inteiro.')

def sacar():
    global saldo, transacoes, saques_hoje
    if saques_hoje >= 3:
        print('Limite de saques diários alcançado.')
        return
    while True:
        try:
            valor = int(input('Qual valor deseja sacar? R$ '))
            if valor > saldo:
                print('Valor solicitado maior que saldo. Operação impossível.')
            elif valor > 500:
                print('Valor solicitado superior a 500 reais. Operação não realizada.')
            else:
                saldo -= valor
                saques_hoje += 1
                transacoes.append((locale.currency(valor), 'Saque'))
                print('Saque realizado com sucesso.')
                break
        except ValueError:
            print('Por favor, digite um número inteiro.')

def mostrar_extrato():
    print('Extrato de transações:')
    for valor, tipo in transacoes:
        print(f'{tipo}: {valor}')
    print(f'Saldo atual: {locale.currency(saldo)}')

while True:
    operacao = input(menu).lower()
    if operacao == 'd':
        deposito()
    elif operacao == 's':
        sacar()
    elif operacao == 'e':
        mostrar_extrato()
    elif operacao == 'o':
        print('Saindo do sistema...')
        break
    else:
        print('Opção inválida, tente novamente.')
