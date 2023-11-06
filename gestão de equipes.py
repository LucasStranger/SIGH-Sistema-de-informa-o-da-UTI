from datetime import datetime, timedelta

# Dados fictícios de profissionais
profissionais = {
    "Enfermeiro1": {
        "Cargo": "Enfermeiro",
        "Experiência": "5 anos",
        "Contato": "enfermeiro1@example.com",
        "Disponibilidade": ["Manhã", "Tarde", "Noite"],
        "Escala": {},
        "HorasTrabalhadas": {}
    },
    "Tecnico1": {
        "Cargo": "Técnico",
        "Experiência": "3 anos",
        "Contato": "tecnico1@example.com",
        "Disponibilidade": ["Manhã", "Tarde"],
        "Escala": {},
        "HorasTrabalhadas": {}
    }
}

# Função para alocar profissionais em plantões
def alocar_profissional(profissional, data, turno):
    if data not in profissionais[profissional]["Escala"]:
        profissionais[profissional]["Escala"][data] = []
    if turno in profissionais[profissional]["Disponibilidade"]:
        profissionais[profissional]["Escala"][data].append(turno)
        return "Profissional alocado com sucesso"
    else:
        return "Turno indisponível para este profissional"

# Função para gerar escala de trabalho
def gerar_escala(data_inicial, data_final):
    escala = {}
    for data in date_range(data_inicial, data_final):
        escala[data.strftime("%d/%m/%Y")] = {"Manhã": [], "Tarde": [], "Noite": []}
    return escala

# Função para registrar a entrada de um profissional
def registrar_entrada(profissional, data, turno):
    if data in profissionais[profissional]["Escala"] and turno in profissionais[profissional]["Escala"][data]:
        agora = datetime.now()
        hora_atual = agora.strftime("%H:%M")
        profissionais[profissional]["HorasTrabalhadas"].setdefault(data, {})[turno] = {"Inicio": hora_atual}
        return "Entrada registrada com sucesso"
    else:
        return "Data ou turno inválido"

# Função para registrar a saída de um profissional
def registrar_saida(profissional, data, turno):
    if data in profissionais[profissional]["Escala"] and turno in profissionais[profissional]["Escala"][data]:
        agora = datetime.now()
        hora_atual = agora.strftime("%H:%M")
        profissionais[profissional]["HorasTrabalhadas"][data][turno]["Termino"] = hora_atual
        return "Saída registrada com sucesso"
    else:
        return "Data ou turno inválido"

# Função para calcular horas trabalhadas
def calcular_horas_trabalhadas(profissional, data):
    horas_trabalhadas = 0

    if data in profissionais[profissional]["HorasTrabalhadas"]:
        for turno, registro in profissionais[profissional]["HorasTrabalhadas"][data].items():
            inicio = datetime.strptime(registro["Inicio"], "%H:%M")
            termino = datetime.strptime(registro["Termino"], "%H:%M")
            diferenca = termino - inicio
            horas_trabalhadas += diferenca.total_seconds() / 3600

    return horas_trabalhadas

# Função para criar uma faixa de datas
def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

# Menu para gestão de equipes
def menu_gestao_equipes():
    while True:
        print("\n### Menu de Gestão de Equipes ###")
        print("1. Alocar Profissional em Plantão")
        print("2. Registrar Entrada de Profissional")
        print("3. Registrar Saída de Profissional")
        print("4. Calcular Horas Trabalhadas de um Profissional")
        print("5. Voltar ao Menu Principal")

        opcao_gestao_equipes = input("Escolha a opção desejada: ")

        if opcao_gestao_equipes == "1":
            profissional = input("Nome do profissional: ")
            data = input("Data (dd/mm/aaaa): ")
            turno = input("Turno (Manhã/Tarde/Noite): ")
            resultado_alocacao = alocar_profissional(profissional, data, turno)
            print(resultado_alocacao)
        elif opcao_gestao_equipes == "2":
            profissional = input("Nome do profissional: ")
            data = input("Data (dd/mm/aaaa): ")
            turno = input("Turno (Manhã/Tarde/Noite): ")
            resultado_entrada = registrar_entrada(profissional, data, turno)
            print(resultado_entrada)
        elif opcao_gestao_equipes == "3":
            profissional = input("Nome do profissional: ")
            data = input("Data (dd/mm/aaaa): ")
            turno = input("Turno (Manhã/Tarde/Noite): ")
            resultado_saida = registrar_saida(profissional, data, turno)
            print(resultado_saida)
        elif opcao_gestao_equipes == "4":
            profissional = input("Nome do profissional: ")
            data = input("Data (dd/mm/aaaa): ")
            horas_trabalhadas = calcular_horas_trabalhadas(profissional, data)
            print(f"Horas trabalhadas: {horas_trabalhadas:.2f} horas")
        elif opcao_gestao_equipes == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    data_inicial = datetime(2023, 11, 1)
    data_final = datetime(2023, 11, 7)
    escala = gerar_escala(data_inicial, data_final)
    menu_gestao_equipes()
