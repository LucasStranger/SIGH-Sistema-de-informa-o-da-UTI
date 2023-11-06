import csv
from datetime import datetime

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

if __name__ == "__main__":
    Relatorios_analise()
