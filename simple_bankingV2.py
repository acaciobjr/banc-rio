import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

menu = 'Digite:\n- [d] para Depositar\n- [s] para Sacar\n- [e] para ver o Extrato\n- [nc] para Nova conta\n- [lc] para Listar contas\n- [nu] para Novo usuário\n- [o] para Sair\n'
saldo = 0
transacoes = []
saques_hoje = 0
usuarios = []
contas = []
numero_conta_atual = 1

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
                continue
            elif valor > 500:
                print('Valor solicitado superior a 500 reais. Operação não realizada.')
                continue
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

def criar_conta():
    global numero_conta_atual
    cpf = input("Informe o CPF do titular (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("Usuário não encontrado. Por favor, crie um usuário primeiro.")
        return
    contas.append({"agencia": "0001", "numero_conta": numero_conta_atual, "usuario": cpf})
    print(f'Conta criada com sucesso. Número da conta: {numero_conta_atual}')
    numero_conta_atual += 1

def listar_contas():
    for conta in contas:
        usuario = filtrar_usuario(conta['usuario'], usuarios)
        if usuario:
            print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Titular: {usuario['nome']}")

def criar_usuario():
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Já existe usuário com esse CPF.")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número, bairro, cidade/sigla do estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print('Usuário criado com sucesso!')

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    return None

while True:
    operacao = input(menu).lower()
    if operacao == 'd':
        deposito()
    elif operacao == 's':
        sacar()
    elif operacao == 'e':
        mostrar_extrato()
    elif operacao == 'nc':
        criar_conta()
    elif operacao == 'lc':
        listar_contas()
    elif operacao == 'nu':
        criar_usuario()
    elif operacao == 'o':
        print('Saindo do sistema.')
        break
    else:
        print('Opção inválida, tente novamente.')
