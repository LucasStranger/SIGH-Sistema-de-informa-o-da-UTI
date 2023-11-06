# Função para cadastrar um visitante autorizado
def cadastrar_visitante():
    nome = input("Nome do visitante: ")
    documento_identificacao = input("Documento de identificação: ")
    paciente = input("Paciente a ser visitado: ")
    
    visitante = {
        "Nome": nome,
        "Documento de Identificação": documento_identificacao,
        "Paciente": paciente
    }
    
    visitantes_autorizados.append(visitante)
    print("Visitante autorizado cadastrado com sucesso.")

# Função para listar visitantes autorizados
def listar_visitantes_autorizados():
    print("\nLista de Visitantes Autorizados:")
    for i, visitante in enumerate(visitantes_autorizados, 1):
        print(f"{i}. Nome: {visitante['Nome']}, Documento de Identificação: {visitante['Documento de Identificação']}, Paciente: {visitante['Paciente']}")

# Menu de cadastro de visitantes
def menu_cadastro_visitantes():
    while True:
        print("\nOpções:")
        print("1. Cadastrar Visitante Autorizado")
        print("2. Listar Visitantes Autorizados")
        print("3. Voltar ao Menu Principal")
        
        opcao = input("Escolha a opção desejada: ")

        if opcao == "1":
            cadastrar_visitante()
        elif opcao == "2":
            listar_visitantes_autorizados()
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")

# Lista de visitantes autorizados (pode ser carregada de um arquivo ou banco de dados)
visitantes_autorizados = []

# Função principal
def cadastro_visitante():
    while True:
        print("\n### Menu Principal ###")
        print("1. Cadastro de Visitantes")
        print("2. Sair")

        opcao_principal = input("Escolha a opção desejada: ")

        if opcao_principal == "1":
            menu_cadastro_visitantes()
        elif opcao_principal == "2":
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    cadastro_visitante()
