import datetime

class EquipamentoMedico:
    def __init__(self, nome, modelo, numero_serie, data_aquisicao):
        self.nome = nome
        self.modelo = modelo
        self.numero_serie = numero_serie
        self.data_aquisicao = data_aquisicao
        self.manutencoes = []

    def registrar_manutencao(self, tipo_manutencao, intervencao):
        data_manutencao = datetime.datetime.now()
        self.manutencoes.append({
            'data': data_manutencao,
            'tipo': tipo_manutencao,
            'intervencao': intervencao
        })

    def programar_manutencao_preventiva(self, tipo_manutencao, data_agendada):
        self.manutencoes.append({
            'data': data_agendada,
            'tipo': tipo_manutencao,
            'intervencao': 'Manutenção preventiva agendada'
        })

    def historico_manutencoes(self):
        for manutencao in self.manutencoes:
            print(f"Data: {manutencao['data'].strftime('%d/%m/%Y')}, Tipo: {manutencao['tipo']}, Intervenção: {manutencao['intervencao']}")

def registrar_equipamento(equipamentos):
    nome = input("Nome do equipamento: ")
    modelo = input("Modelo: ")
    numero_serie = input("Número de Série: ")
    data_aquisicao = input("Data de Aquisição (dd/mm/aaaa): ")
    try:
        data_aquisicao = datetime.datetime.strptime(data_aquisicao, "%d/%m/%Y")
        equipamento = EquipamentoMedico(nome, modelo, numero_serie, data_aquisicao)
        equipamentos.append(equipamento)
        print("Equipamento registrado com sucesso!")
    except ValueError:
        print("Data de aquisição inválida. Use o formato dd/mm/aaaa.")

def registrar_manutencao(equipamentos):
    numero_serie = input("Número de Série do equipamento: ")
    tipo_manutencao = input("Tipo de Manutenção: ")
    intervencao = input("Intervenção realizada: ")

    for equipamento in equipamentos:
        if equipamento.numero_serie == numero_serie:
            equipamento.registrar_manutencao(tipo_manutencao, intervencao)
            print("Manutenção registrada com sucesso.")
            return  # Encerra a função após encontrar o equipamento

    print("Equipamento não encontrado.")

def programar_manutencao_preventiva(equipamentos):
    numero_serie = input("Número de Série do equipamento: ")
    tipo_manutencao = input("Tipo de Manutenção Preventiva: ")
    data_agendada = input("Data de Manutenção Preventiva (dd/mm/aaaa): ")

    for equipamento in equipamentos:
        if equipamento.numero_serie == numero_serie:
            try:
                data_agendada = datetime.datetime.strptime(data_agendada, "%d/%m/%Y")
                equipamento.programar_manutencao_preventiva(tipo_manutencao, data_agendada)
                print("Manutenção preventiva agendada com sucesso.")
                return  # Encerra a função após encontrar o equipamento
            except ValueError:
                print("Data de agendamento inválida. Use o formato dd/mm/aaaa.")

    print("Equipamento não encontrado.")

def controle_equipamentos():
    equipamentos = []

    while True:
        print("\nOpções:")
        print("1. Registrar Equipamento")
        print("2. Registrar Manutenção")
        print("3. Programar Manutenção Preventiva")
        print("4. Visualizar Histórico de Manutenções")
        print("5. Sair")

        escolha = input("Escolha a opção desejada: ")

        if escolha == '1':
            registrar_equipamento(equipamentos)

        elif escolha == '2':
            registrar_manutencao(equipamentos)

        elif escolha == '3':
            programar_manutencao_preventiva(equipamentos)

        elif escolha == '4':
            numero_serie = input("Número de Série do equipamento: ")
            for equipamento in equipamentos:
                if equipamento.numero_serie == numero_serie:
                    print("\nHistórico de Manutenções:")
                    equipamento.historico_manutencoes()
                    break  # Encerra o loop após encontrar o equipamento

            else:
                print("Equipamento não encontrado.")

        elif escolha == '5':
            print("Saindo do programa.")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    controle_equipamentos()

