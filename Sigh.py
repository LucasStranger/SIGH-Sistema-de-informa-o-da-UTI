import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
from datetime import datetime, timedelta
import threading
import time
import pandas as pd
import os
import sqlite3

# Configurações do servidor de e-mail
email_host = "lucas.limoeiro@souunit.com.br"
email_port = 587
email_user = "lucas.limoeiro@souunit.com.br"
email_password = "Lucas19032008@"
destinatario = "lucasstranger32@gmail.com"
# Capacidade máxima de ocupação de leitos
capacidade_maxima = {
    "UTI": 10,
    "Ala A": 20,
    "Ala B": 20
}

# Dicionário para rastrear os leitos no hospital
hospital = {
    "UTI": [],
    "Ala A": [],
    "Ala B": []
}

# Função para enviar e-mail de notificação
def enviar_email_notificacao(destinatario, mensagem):
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = destinatario
    msg["Subject"] = "Leito Disponível"

    corpo_mensagem = mensagem
    msg.attach(MIMEText(corpo_mensagem, "plain"))

    try:
        servidor_smtp = smtplib.SMTP(email_host, email_port)
        servidor_smtp.starttls()
        servidor_smtp.login(email_user, email_password)
        servidor_smtp.sendmail(email_user, destinatario, msg.as_string())
        servidor_smtp.quit()
        print(f"E-mail de notificação enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar e-mail de notificação: {str(e)}")

# Função para listar a ocupação dos leitos em uma ala
def listar_leitos_ala(ala):
    leitos = hospital.get(ala, [])
    for i, leito in enumerate(leitos):
        status = "Ocupado" if leito["Ocupado"] else "Livre"
        prioridade = leito["Prioridade"]
        print(f"Leito {i + 1}: {status} (Prioridade: {prioridade})")

# Função para listar a ocupação dos leitos na UTI
def listar_leitos_uti():
    listar_leitos_ala("UTI")

# Função para alocar um paciente em um leito
def alocar_paciente(ala, leito_index):
    leitos = hospital.get(ala, [])
    if 0 <= leito_index < len(leitos):
        leito = leitos[leito_index]
        if not leito["Ocupado"]:
            leito["Ocupado"] = True
            print(f"Paciente alocado no Leito {leito_index + 1} na {ala}.")
            notificar_equipe_saude()
            registrar_ocupacao_leito(ala, leito_index)
        else:
            print(f"Leito {leito_index + 1} na {ala} já está ocupado.")
    else:
        print(f"Leito {leito_index + 1} na {ala} não existe.")

# Função para liberar um leito
def liberar_leito(ala, leito_index):
    leitos = hospital.get(ala, [])
    if 0 <= leito_index < len(leitos):
        leito = leitos[leito_index]
        if leito["Ocupado"]:
            leito["Ocupado"] = False
            print(f"Leito {leito_index + 1} na {ala} foi liberado.")
            notificar_equipe_saude()
            registrar_ocupacao_leito(ala, leito_index)
        else:
            print(f"Leito {leito_index + 1} na {ala} já está vazio.")
    else:
        print(f"Leito {leito_index + 1} na {ala} não existe.")

# Função para notificar a equipe de saúde sobre a disponibilidade de leitos
def notificar_equipe_saude():
    equipe_saude_emails = ["enfermeiro@example.com", "medico@example.com", "admin@example.com"]
    mensagem = "Um leito está disponível. Por favor, acomode o paciente o mais rápido possível."
    
    for destinatario in equipe_saude_emails:
        enviar_email_notificacao(destinatario, mensagem)

# Função para registrar a ocupação do leito no histórico
def registrar_ocupacao_leito(ala, leito_index):
    data_hora = datetime.datetime.now()
    with open("historico_ocupacao_leitos.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([ala, leito_index, "Ocupado", data_hora])

# Função para verificar a ocupação dos leitos
def verificar_ocupacao_leitos():
    while True:
        for ala, leitos in hospital.items():
            ocupados = sum(1 for leito in leitos if leito["Ocupado"])
            capacidade = capacidade_maxima.get(ala, 0)
            if ocupados >= 0.9 * capacidade:
                mensagem = f"A ocupação na {ala} está próxima da capacidade máxima. Ocupados: {ocupados}, Capacidade: {capacidade}"
                enviar_email_notificacao(destinatario, mensagem)
        time.sleep(3600)

# Função para gerar um relatório CSV com estatísticas de ocupação
def gerar_relatorio_ocupacao_leitos():
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"relatorio_ocupacao_leitos_{data_hora}.csv"

    # Crie um DataFrame a partir dos dados
    data = []
    for ala, leitos in hospital.items():
        ocupados = sum(1 for leito in leitos if leito["Ocupado"])
        capacidade = capacidade_maxima.get(ala, 0)
        percentagem_ocupacao = (ocupados / capacidade) * 100 if capacidade > 0 else 0
        data.append([ala, ocupados, capacidade, percentagem_ocupacao])

    # Crie o DataFrame
    df = pd.DataFrame(data, columns=["Ala", "Leitos Ocupados", "Capacidade Máxima", "Percentagem de Ocupação"])

    # Salve o DataFrame como um arquivo CSV
    df.to_csv(nome_arquivo, index=False)

    print(f"Relatório de ocupação de leitos gerado em {nome_arquivo}")

# Função para consultar o histórico de ocupação de leitos
def consultar_historico_ocupacao_leitos():
    nome_arquivo = "historico_ocupacao_leitos.csv"

    # Leia o histórico de ocupação como um DataFrame
    df = pd.read_csv(nome_arquivo)

    print("Histórico de ocupação de leitos:")
    print(df)

# Função para adicionar um leito à UTI com prioridade
def adicionar_leito_uti(prioridade):
    leito = {
        "Ocupado": False,
        "Prioridade": prioridade
    }
    hospital["UTI"].append(leito)
    hospital["UTI"] = sorted(hospital["UTI"], key=lambda x: x["Prioridade"], reverse=True)

# Função para adicionar um leito a uma Ala
def adicionar_leito_ala(ala, prioridade):
    if ala in hospital:
        leito = {
            "Ocupado": False,
            "Prioridade": prioridade
        }
        hospital[ala].append(leito)
        hospital[ala] = sorted(hospital[ala], key=lambda x: x["Prioridade"], reverse=True)
    else:
        print(f"A ala {ala} não existe no hospital.")

# Função principal que exibe o menu de gestão de leitos
def menu_gestao_leitos():
    while True:
        print("\n--- Menu de Gestão de Leitos ---")
        print("1. Listar Leitos da UTI")
        print("2. Listar Leitos de uma Ala")
        print("3. Alocar Paciente em Leito")
        print("4. Liberar Leito")
        print("5. Adicionar Leito à UTI")
        print("6. Adicionar Leito a uma Ala")
        print("7. Gerar Relatório de Ocupação de Leitos")
        print("8. Consultar Histórico de Ocupação de Leitos")
        print("9. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            listar_leitos_uti()
        elif escolha == '2':
            ala = input("Digite a ala (Ala A, Ala B, etc.): ")
            listar_leitos_ala(ala)
        elif escolha == '3':
            ala = input("Digite a ala (Ala A, Ala B, UTI, etc.): ")
            leito_index = int(input("Digite o número do leito: "))
            alocar_paciente(ala, leito_index)
        elif escolha == '4':
            ala = input("Digite a ala (Ala A, Ala B, UTI, etc.): ")
            leito_index = int(input("Digite o número do leito: "))
            liberar_leito(ala, leito_index)
        elif escolha == '5':
            prioridade = int(input("Digite a prioridade do leito na UTI: "))
            adicionar_leito_uti(prioridade)
        elif escolha == '6':
            ala = input("Digite a ala (Ala A, Ala B, etc.): ")
            prioridade = int(input("Digite a prioridade do leito na ala: "))
            adicionar_leito_ala(ala, prioridade)
        elif escolha == '7':
            gerar_relatorio_ocupacao_leitos()
        elif escolha == '8':
            consultar_historico_ocupacao_leitos()
        elif escolha == '9':
            print("Saindo do Menu de Gestão de Leitos.")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Inicie a verificação da ocupação dos leitos em segundo plano
verificacao_thread = threading.Thread(target=verificar_ocupacao_leitos)
verificacao_thread.daemon = True
verificacao_thread.start()

# Configurações do banco de dados
db_file = "prontuario.db"

# Capacidade máxima de visitantes por paciente
capacidade_maxima = 2

# Restrições de horário
horario_inicial = datetime.time(10, 0)  # Horário de início das visitas
horario_final = datetime.time(18, 0)  # Horário de término das visitas

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect(db_file)
    return conn

# Função para criar as tabelas no banco de dados
def criar_tabelas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            data DATE,
            horario TIME,
            instrucoes TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            documento_identificacao TEXT,
            relacao_paciente TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Função para agendar uma visita
def agendar_visita(paciente_id, data, horario, instrucoes):
    conn = conectar_bd()
    cursor = conn.cursor()

    # Verificar capacidade máxima de visitantes por paciente
    cursor.execute('SELECT COUNT(*) FROM visitas WHERE paciente_id = ?', (paciente_id,))
    visitas_agendadas = cursor.fetchone()[0]

    if visitas_agendadas >= capacidade_maxima:
        conn.close()
        return "Capacidade máxima de visitantes excedida."

    # Verificar restrições de horário
    horario_agendado = datetime.datetime.strptime(horario, "%H:%M").time()
    if not horario_inicial <= horario_agendado <= horario_final:
        conn.close()
        return "Horário não permitido para visitas."

    cursor.execute('''
        INSERT INTO visitas (paciente_id, data, horario, instrucoes)
        VALUES (?, ?, ?, ?)
    ''', (paciente_id, data, horario, instrucoes))
    conn.commit()
    conn.close()
    return "Visita agendada com sucesso."

# Função para registrar um visitante
def registrar_visitante(nome, documento_identificacao, relacao_paciente):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO visitantes (nome, documento_identificacao, relacao_paciente)
        VALUES (?, ?, ?)
    ''', (nome, documento_identificacao, relacao_paciente))
    conn.commit()
    conn.close()

# Função para listar visitantes autorizados
def listar_visitantes():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM visitantes')
    visitantes = cursor.fetchall()
    conn.close()
    return visitantes

# Função para cancelar uma visita agendada
def cancelar_visita(visita_id):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM visitas WHERE id = ?', (visita_id,))
    conn.commit()
    conn.close()
    return "Visita cancelada com sucesso."

# Função para reagendar uma visita agendada
def reagendar_visita(visita_id, nova_data, novo_horario, novas_instrucoes):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE visitas
        SET data = ?, horario = ?, instrucoes = ?
        WHERE id = ?
    ''', (nova_data, novo_horario, novas_instrucoes, visita_id))
    conn.commit()
    conn.close()
    return "Visita reagendada com sucesso."

# Função para enviar e-mail de notificação
def enviar_email_notificacao(destinatario, mensagem):
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = destinatario
    msg["Subject"] = "Detalhes da Visita"

    corpo_mensagem = mensagem
    msg.attach(MIMEText(corpo_mensagem, "plain"))

    try:
        servidor_smtp = smtplib.SMTP(email_host, email_port)
        servidor_smtp.starttls()
        servidor_smtp.login(email_user, email_password)
        servidor_smtp.sendmail(email_user, destinatario, msg.as_string())
        servidor_smtp.quit()
        return "E-mail de notificação enviado com sucesso."
    except Exception as e:
        return f"Erro ao enviar e-mail de notificação: {str(e)}"

# Função para verificar se a visita está dentro do horário permitido
def verificar_horario_visita(horario):
    horario_visita = datetime.datetime.strptime(horario, "%H:%M").time()
    return horario_inicial <= horario_visita <= horario_final

# Função para agendar uma visita e notificar o visitante
def agendar_e_notificar_visita(paciente_id, data, horario, instrucoes, visitante_id):
    if not verificar_horario_visita(horario):
        return "Horário não permitido para visitas."
    
    resultado_agendamento = agendar_visita(paciente_id, data, horario, instrucoes)
    
    if resultado_agendamento != "Visita agendada com sucesso.":
        return resultado_agendamento

    visitantes = listar_visitantes()
    visitante = visitantes[visitante_id]

    mensagem = f"Visita agendada para o paciente. Data: {data}, Horário: {horario}, Instruções: {instrucoes}"
    resultado_notificacao = enviar_email_notificacao(visitante[1], mensagem)

    if resultado_notificacao != "E-mail de notificação enviado com sucesso.":
        return resultado_notificacao

    return resultado_agendamento

# Função para exibir o menu
def Agendamento_Controle_visitas():
    while True:
        print("\nOpções:")
        print("1. Agendar Visita")
        print("2. Listar Visitantes Autorizados")
        print("3. Registrar Visitante Autorizado")
        print("4. Cancelar Visita Agendada")
        print("5. Reagendar Visita")
        print("6. Sair")

        escolha = input("Escolha a opção desejada: ")

        if escolha == '1':
            paciente_id = int(input("ID do Paciente: "))
            data = input("Data da Visita (aaaa-mm-dd): ")
            horario = input("Horário da Visita (HH:MM): ")
            instrucoes = input("Instruções: ")
            visitante_id = int(input("ID do Visitante: "))
            resultado = agendar_e_notificar_visita(paciente_id, data, horario, instrucoes, visitante_id)
            print(resultado)

        elif escolha == '2':
            visitantes = listar_visitantes()
            if visitantes:
                print("\nVisitantes Autorizados:")
                for visitante in visitantes:
                    print(f"ID: {visitante[0]}, Nome: {visitante[1]}, Documento de Identificação: {visitante[2]}, Relação: {visitante[3]}")
            else:
                print("Nenhum visitante autorizado registrado.")

        elif escolha == '3':
            nome = input("Nome do Visitante: ")
            documento_identificacao = input("Documento de Identificação: ")
            relacao_paciente = input("Relação com o Paciente: ")
            registrar_visitante(nome, documento_identificacao, relacao_paciente)
            print("Visitante autorizado registrado com sucesso.")

        elif escolha == '4':
            visita_id = int(input("ID da Visita a ser Cancelada: "))
            resultado = cancelar_visita(visita_id)
            print(resultado)

        elif escolha == '5':
            visita_id = int(input("ID da Visita a ser Reagendada: "))
            nova_data = input("Nova Data (aaaa-mm-dd): ")
            novo_horario = input("Novo Horário (HH:MM): ")
            novas_instrucoes = input("Novas Instruções: ")
            resultado = reagendar_visita(visita_id, nova_data, novo_horario, novas_instrucoes)
            print(resultado)

        elif escolha == '6':
            print("Saindo do programa.")
            break

        else:
            print("Opção inválida. Tente novamente.")

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


class UTI:
    def __init__(self, nome, capacidade_leitos):
        self.nome = nome
        self.capacidade_leitos = capacidade_leitos
        self.pacientes = []

    def adicionar_paciente(self, paciente):
        if len(self.pacientes) < self.capacidade_leitos:
            self.pacientes.append(paciente)
            return True
        else:
            return False

    def remover_paciente(self, paciente):
        if paciente in self.pacientes:
            self.pacientes.remove(paciente)
            return True
        else:
            return False

    def taxa_ocupacao(self):
        return len(self.pacientes) / self.capacidade_leitos

    def eficiencia_equipamentos(self, equipamento):
        total_pacientes = len(self.pacientes)
        utilizacao_equipamento = sum(1 for paciente in self.pacientes if equipamento in paciente.equipamentos)
        return utilizacao_equipamento / total_pacientes if total_pacientes > 0 else 0

class Paciente:
    def __init__(self, nome, idade, genero):
        self.nome = nome
        self.idade = idade
        self.genero = genero
        self.equipamentos = set()

    def adicionar_equipamento(self, equipamento):
        self.equipamentos.add(equipamento)

class Equipamento:
    def __init__(self, nome):
        self.nome = nome

def exportar_relatorio_txt(nome_arquivo, conteudo):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(conteudo)

def exportar_relatorio_csv(nome_arquivo, dados):
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerows(dados)

def menu_relatorios(uti, equipamento1, equipamento2):
    while True:
        print("\n### Menu de Relatórios e Análises ###")
        print("1. Gerar Relatório de Ocupação de Leitos")
        print("2. Gerar Relatório de Eficiência no Uso de Equipamentos")
        print("3. Exportar Relatórios")
        print("4. Sair")

        opcao_relatorios = input("Escolha a opção desejada: ")

        if opcao_relatorios == "1":
            relatorio_ocupacao = f"Taxa de Ocupação de Leitos da {uti.nome}: {uti.taxa_ocupacao() * 100:.2f}%"
            print(relatorio_ocupacao)
        elif opcao_relatorios == "2":
            relatorio_eficiencia = "Relatório de Eficiência no Uso de Equipamentos:\n"
            relatorio_eficiencia += f"Respirador: {uti.eficiencia_equipamentos(equipamento1) * 100:.2f}%\n"
            relatorio_eficiencia += f"Monitor Cardíaco: {uti.eficiencia_equipamentos(equipamento2) * 100:.2f}%"
            print(relatorio_eficiencia)
        elif opcao_relatorios == "3":
            # Exportar relatórios para .txt e .csv
            exportar_relatorio_txt("relatorio.txt", f"{relatorio_ocupacao}\n\n{relatorio_eficiencia}")
            exportar_relatorio_csv("relatorio.csv", [("Equipamento", "Eficiência"), (equipamento1.nome, uti.eficiencia_equipamentos(equipamento1) * 100), (equipamento2.nome, uti.eficiencia_equipamentos(equipamento2) * 100)])
            print("Relatórios exportados com sucesso.")
        elif opcao_relatorios == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")

def Relatórios_analise():
    uti = UTI("UTI Central", 10)

    equipamento1 = Equipamento("Respirador")
    equipamento2 = Equipamento("Monitor Cardíaco")

    paciente1 = Paciente("João", 45, "Masculino")
    paciente1.adicionar_equipamento(equipamento1)
    paciente1.adicionar_equipamento(equipamento2)

    paciente2 = Paciente("Maria", 60, "Feminino")
    paciente2.adicionar_equipamento(equipamento1)

    uti.adicionar_paciente(paciente1)
    uti.adicionar_paciente(paciente2)

    menu_relatorios(uti, equipamento1, equipamento2)

while True:
    print(' 1 - Gestão de leitos/Prontuários')
    print(' 2 - Controle de equipamentos')
    print(' 3 - Administração de medicamentos')
    print(' 4 - Agendamento e Controle de Visitas')
    print(' 5 - Cadastro de Visitantes')
    print(' 6 - Gestão de Equipes')
    print(' 7 - Relatórios e Análises')

    escolha = int(input('Digite o módulo correspondente:'))

    if escolha == 1:
        menu_gestao_leitos()
    elif escolha == 2:
        controle_equipamentos()
    elif escolha == 3:
        administração_medicamentos()
    elif escolha == 4:
        criar_tabelas()
        Agendamento_Controle_visitas()
    elif escolha == 5:
        cadastro_visitante()
    elif escolha == 6:
        data_inicial = datetime(2023, 11, 1)
        data_final = datetime(2023, 11, 7)
        escala = gerar_escala(data_inicial, data_final)
        menu_gestao_equipes()
    elif escolha == 7:
        Relatórios_analise()
    else:
        print('Digite novamente!')