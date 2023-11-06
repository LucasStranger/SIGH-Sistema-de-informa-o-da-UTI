import datetime

class Medicamento:
    def __init__(self, nome, principio_ativo, dosagem, forma_administracao):
        self.nome = nome
        self.principio_ativo = principio_ativo
        self.dosagem = dosagem
        self.forma_administracao = forma_administracao
        self.lotes = []
        self.administracoes = []

    def cadastrar_lote(self, quantidade, data_validade, fornecedor):
        lote = {
            'quantidade': quantidade,
            'data_validade': data_validade,
            'fornecedor': fornecedor
        }
        self.lotes.append(lote)

    def alerta_estoque_baixo(self, quantidade_critica):
        for lote in self.lotes:
            if lote['quantidade'] <= quantidade_critica:
                print(f"Alerta: Estoque baixo para {self.nome}. Lote com data de validade {lote['data_validade']} está abaixo do nível crítico.")

    def rastrear_lote(self, lote_id):
        for lote in self.lotes:
            if lote_id == lote:
                return lote
        return None

    def registrar_administracao(self, paciente, dosagem, responsavel):
        data_administracao = datetime.datetime.now()
        administracao = {
            'data': data_administracao,
            'paciente': paciente,
            'dosagem': dosagem,
            'responsavel': responsavel
        }
        self.administracoes.append(administracao)

    def historico_administracoes(self):
        for administracao in self.administracoes:
            print(f"Data: {administracao['data'].strftime('%d/%m/%Y %H:%M')}, Paciente: {administracao['paciente']}, Dosagem: {administracao['dosagem']}, Responsável: {administracao['responsavel']}")

class EstoqueMedicamentos:
    def __init__(self):
        self.medicamentos = []

    def cadastrar_medicamento(self, medicamento):
        self.medicamentos.append(medicamento)

    def obter_medicamento_por_nome(self, nome):
        for medicamento in self.medicamentos:
            if medicamento.nome == nome:
                return medicamento
        return None

    def obter_medicamentos_em_estoque(self):
        medicamentos_em_estoque = []
        for medicamento in self.medicamentos:
            if medicamento.lotes:
                medicamentos_em_estoque.append(medicamento)
        return medicamentos_em_estoque

def obter_data_validade():
    while True:
        data_validade = input("Data de Validade (dd/mm/aaaa): ")
        try:
            return datetime.datetime.strptime(data_validade, "%d/%m/%Y")
        except ValueError:
            print("Data de Validade inválida. Use o formato dd/mm/aaaa.")

def menu_administracao_medicamentos(estoque_medicamentos):
    while True:
        print("\n--- Menu de Administração de Medicamentos ---")
        print("1. Cadastrar Medicamento")
        print("2. Cadastrar Lote de Medicamento")
        print("3. Alerta de Estoque Baixo")
        print("4. Rastrear Lote de Medicamento")
        print("5. Registrar Administração de Medicamento")
        print("6. Visualizar Histórico de Administrações")
        print("7. Sair")

        escolha = input("Escolha a opção desejada: ")

        if escolha == '1':
            nome = input("Nome do medicamento: ")
            principio_ativo = input("Princípio Ativo: ")
            dosagem = input("Dosagem: ")
            forma_administracao = input("Forma de Administração: ")
            medicamento = Medicamento(nome, principio_ativo, dosagem, forma_administracao)
            estoque_medicamentos.cadastrar_medicamento(medicamento)
            print("Medicamento cadastrado com sucesso!")

        elif escolha == '2':
            nome = input("Nome do medicamento: ")
            medicamento = estoque_medicamentos.obter_medicamento_por_nome(nome)
            if medicamento:
                quantidade = int(input("Quantidade: "))
                data_validade = obter_data_validade()
                fornecedor = input("Fornecedor: ")
                medicamento.cadastrar_lote(quantidade, data_validade, fornecedor)
                print("Lote de medicamento cadastrado com sucesso!")
            else:
                print("Medicamento não encontrado.")

        elif escolha == '3':
            medicamentos_em_estoque = estoque_medicamentos.obter_medicamentos_em_estoque()
            quantidade_critica = int(input("Quantidade Crítica: "))
            for medicamento in medicamentos_em_estoque:
                medicamento.alerta_estoque_baixo(quantidade_critica)

        elif escolha == '4':
            nome = input("Nome do medicamento: ")
            medicamento = estoque_medicamentos.obter_medicamento_por_nome(nome)
            if medicamento:
                lote_id = int(input("ID do Lote: "))
                lote = medicamento.rastrear_lote(lote_id)
                if lote:
                    print(f"Origem do Lote: Quantidade: {lote['quantidade']}, Data de Validade: {lote['data_validade'].strftime('%d/%m/%Y')}, Fornecedor: {lote['fornecedor']}")
                else:
                    print("Lote não encontrado.")
            else:
                print("Medicamento não encontrado.")

        elif escolha == '5':
            nome = input("Nome do medicamento: ")
            medicamento = estoque_medicamentos.obter_medicamento_por_nome(nome)
            if medicamento:
                paciente = input("Paciente: ")
                dosagem = input("Dosagem: ")
                responsavel = input("Responsável: ")
                medicamento.registrar_administracao(paciente, dosagem, responsavel)
                print("Administração registrada com sucesso!")
            else:
                print("Medicamento não encontrado.")

        elif escolha == '6':
            nome = input("Nome do medicamento: ")
            medicamento = estoque_medicamentos.obter_medicamento_por_nome(nome)
            if medicamento:
                print("\nHistórico de Administrações:")
                medicamento.historico_administracoes()
            else:
                print("Medicamento não encontrado.")

        elif escolha == '7':
            print("Saindo do Menu de Administração de Medicamentos.")
            break

        else:
            print("Opção inválida. Tente novamente.")

def administração_medicamentos():
    estoque_medicamentos = EstoqueMedicamentos()
    menu_administracao_medicamentos(estoque_medicamentos)

if __name__ == "__main__":
    administração_medicamentos()
