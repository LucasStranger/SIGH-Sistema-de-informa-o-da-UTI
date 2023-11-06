import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import datetime
import threading
import time
import pandas as pd

# Configurações do servidor de e-mail
email_host = "smtp.example.com"
email_port = 587
email_user = "seu_email@example.com"
email_password = "sua_senha"
destinatario = "admin@example.com"  # Endereço de e-mail para envio de alertas

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

# Exemplo de uso:
if __name__ == "__main__":
    menu_gestao_leitos()
