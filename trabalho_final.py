#___BIBLIOTECAS___________________________________________________________________#
import json  # Manipula arquivos JSON (gravação e leitura do histórico)           #
from datetime import datetime # Para registrar a data e hora dos orçamentos       #
from collections import defaultdict # Cria dicionários com listas automaticamente #
import os # Verifica existência de arquivos e manipula arquivos no sistema        #
#_________________________________________________________________________________#

class ItemSeguranca:
    def __init__(self, codigo, nome, categoria, preco, especificacoes, prioridade=1):
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.especificacoes = especificacoes
        self.prioridade = prioridade  # 1 a 5 (5 é mais prioritário)
#_______________________________________________________________________________________________________
    def __str__(self):
        return f"{self.codigo}: {self.nome} - R${self.preco:.2f} [ESPECIFICAÇÕES]-> {self.especificacoes} "
#_______________________________________________________________________________________________________
    def info_completa(self):
        return (f"{self.codigo}: {self.nome} ({self.categoria})\n"
                f"Preço: R${self.preco:.2f}\n"
                f"Especificações: {self.especificacoes}\n"
                f"Prioridade: {self.prioridade}/5")

#_______________________________________________________________________________________________________
class Orcamento:
    def __init__(self, itens):
        self.data = datetime.now()
        self.itens = [(item, qtd) for item, qtd in itens.items()]
        self.total = sum(item.preco * qtd for item, qtd in self.itens)

#_______________________________________________________________________________________________________
class Historico:
    def __init__(self):
        self.orcamentos = [] # Lista de orçamentos armazenados
        self.arquivo = "historico_orcamentos.json" # Caminho do arquivo
        self._carregar_historico()  # Carrega o histórico existente ao iniciar
#_______________________________________________________________________________________________________
    def _carregar_historico(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r') as f: # Verifica se há o arquivo .json no sistema
                dados = json.load(f)
                for orc in dados: # Lê o arquivo Jonson e carrega como lista de dicionários
                    itens = [(ItemSeguranca(**item['item']), item['qtd']) for item in orc['itens']]
                    novo_orc = Orcamento({}) # Cria e armazena os objetovos do Orçamento como os dados lidos
                    novo_orc.itens = itens
                    novo_orc.total = orc['total']
                    novo_orc.data = datetime.strptime(orc['data'], '%Y-%m-%d %H:%M:%S.%f')
                    self.orcamentos.append(novo_orc)
#_______________________________________________________________________________________________________
    def _salvar_historico(self):
        dados = []
        for orc in self.orcamentos: # Prepara os dados para salvar em Jonson
            itens = [{'item': {'codigo': item.codigo, 'nome': item.nome, 'categoria': item.categoria,
                               'preco': item.preco, 'especificacoes': item.especificacoes,
                               'prioridade': item.prioridade}, 'qtd': qtd} for item, qtd in orc.itens]
            dados.append({'data': str(orc.data), 'itens': itens, 'total': orc.total}) #Pega todos os dados do obajeto para armazenar

        with open(self.arquivo, 'w') as f:
            json.dump(dados, f) # Salva o Jonson
#_______________________________________________________________________________________________________
    def adicionar_orcamento(self, orcamento): # Adiciona cada orçamento inserido e armazena
        self.orcamentos.append(orcamento)
        self._salvar_historico()
#_______________________________________________________________________________________________________
    def listar_orcamentos(self): # Retorna a lista de orçamentos de forma ordenada por data
        return sorted(self.orcamentos, key=lambda x: x.data, reverse=True)
#_______________________________________________________________________________________________________
    def comparar_orcamentos(self, idx1, idx2):
        try:
            orc1 = self.orcamentos[idx1]
            orc2 = self.orcamentos[idx2]

            print("\nCOMPARAÇÃO DE ORÇAMENTOS:")
            print(f"\nOrçamento 1 ({orc1.data}): R${orc1.total:.2f}")
            for item, qtd in orc1.itens:
                print(f"  {qtd}x {item.nome}")

            print(f"\nOrçamento 2 ({orc2.data}): R${orc2.total:.2f}")
            for item, qtd in orc2.itens:
                print(f"  {qtd}x {item.nome}")

            diferenca = orc1.total - orc2.total
            if diferenca > 0:
                print(f"\nO Orçamento 1 é R${diferenca:.2f} mais caro que o Orçamento 2")
            elif diferenca < 0:
                print(f"\nO Orçamento 1 é R${-diferenca:.2f} mais barato que o Orçamento 2")
            else:
                print("\nOs orçamentos têm o mesmo valor")

        except IndexError:
            print("Índice inválido no histórico")

#_______________________________________________________________________________________________________
class SistemaSeguranca:
    def __init__(self):
        self.itens = self._carregar_itens()
        self.categorias = list(set(item.categoria for item in self.itens))
        self.historico = Historico()
        self.categorias_selecionadas = []
        self.orcamento_cliente = 0
#_______________________________________________________________________________________________________
    def _carregar_itens(self):# Retorna todos os itens de segurança listados no programa para serem usados
        """Carrega todos os itens de segurança disponíveis"""
        return [
            # Câmeras -> Tipo A
            ItemSeguranca("CAM0", "Câmeras Básicas de monitoramento", "Câmera", 70.90, "infravermelho, Detecção de movimento", 1),
            ItemSeguranca("CAM1", "Câmera Simples 720p", "Câmera", 129.90, "Resolução 720p, visão noturna 5m", 2),
            ItemSeguranca("CAM2", "Câmera Full HD 1080p", "Câmera", 249.90, "Resolução 1080p, visão noturna 10m, áudio", 3),
            ItemSeguranca("CAM3", "Câmera 360° 4K", "Câmera", 499.90, "Resolução 4K, visão 360°, reconhecimento facial", 4),
            ItemSeguranca("CAM4", "Câmera com IA", "Câmera", 699.90, "Detecção de movimento inteligente, reconhecimento facial", 5),

            # Sensores -> Tipo B
            ItemSeguranca("SEN1", "Sensor de Porta/Janela", "Sensor", 59.90, "Detecta abertura de portas e janelas", 3),
            ItemSeguranca("SEN2", "Sensor de Movimento PIR", "Sensor", 89.90, "Detecta movimento em 90° até 8m", 4),
            ItemSeguranca("SEN3", "Sensor de Vidro Quebrado", "Sensor", 129.90, "Detecta som de vidro quebrando", 4),
            ItemSeguranca("SEN4", "Sensor de Inundação", "Sensor", 149.90, "Detecta vazamentos de água", 2),

            # Alarmes -> Tipo C
            ItemSeguranca("ALA1", "Alarme de incêndio", "Alarme", 49.90, "110dB, controle remoto", 5),
            ItemSeguranca("ALA2", "Alarme Sonoro Básico", "Alarme", 99.90, "110dB, controle remoto", 3),
            ItemSeguranca("ALA3", "Alarme com Monitoramento", "Alarme", 199.90, "Inclui serviço de monitoramento 24h", 4),
            ItemSeguranca("ALA4", "Alarme Sem Fio", "Alarme", 599.90, "Sistema completo sem fio, 4 sensores incluídos", 5),

            # Fechaduras -> Tipo D
            ItemSeguranca("FEC1", "Tranca de janela", "Fechadura", 15.90, "Fechadura básica com abertura manual", 2),
            ItemSeguranca("FEC2", "Trava de porta", "Fechadura", 34.90, "Fechadura básica com abertura manual", 2),
            ItemSeguranca("FEC3", "Fechadura Digital", "Fechadura", 349.90, "Abertura por senha e chave", 4),
            ItemSeguranca("FEC4", "Fechadura Biométrica", "Fechadura", 899.90, "Abertura por digital e reconhecimento facial", 5),

            # Acessórios -> Tipo E
            ItemSeguranca("ACES1", "Luminária com Sensor", "Acessório", 79.90, "Acende ao detectar movimento", 2),
            ItemSeguranca("ACES2", "Interfone Inteligente", "Acessório", 399.90, "Tela 7'', comunicação bidirecional", 3),
        ]

#_______________________________________________________________________________________________________
    def apresentacao_da_empresa(self):# APRESENTAÇÃO DA EMPRESA E OBJETIVOS
        print("=" * 60)
        print("               👨‍🚒BEM-VINDO À CALCULANDO COM SEGURANÇA👩‍🚒")
        print("=" * 60)
        print("🔒 Somos uma empresa focada em proteger o que é seu.")
        print("🏡 Atuamos no planejamento inteligente da segurança residencial.")
        print("💡 Nosso foco é a combinação entre economia, praticidade e tecnologia.")
        print("🛠️  Vamos juntos encontrar a melhor solução para sua moradia!")
        print("=" * 60)

#_______________________________________________________________________________________________________
    def mostrar_menu_principal(self):# OPÇÕES DE AÇÕES DO SISTEMA POR NÚMERO
        print("\n" + "="*50)
        print("SISTEMA DE ORÇAMENTO DE SEGURANÇA RESIDENCIAL👌")
        print("="*50)
        print("\n[1]. Ver todos os itens disponíveis🧾")
        print("[2]. Selecionar categoria dos itens🔖")
        print("[3]. Definir orçamento e ver itens dentro do valor💸")
        print("[4]. Gerar orçamento com itens selecionados🛒")
        print("[5]. Consultar histórico🔙")
        print("[6]. Comparar orçamentos💱")
        print("[7]. Sair💨")

#_______________________________________________________________________________________________________
    def mostrar_todos_itens(self):#[1] = VER TODOS OS INTENS DISPONÍVEIS
        print("\nITENS DISPONÍVEIS:")

        itens_por_categoria = defaultdict(list)
        for item in self.itens:
            itens_por_categoria[item.categoria].append(item)

        for categoria, itens in itens_por_categoria.items():
            print(f"\n[{categoria.upper()}]")
            for item in sorted(itens, key=lambda x: x.codigo, reverse=True):
                print(f"  {item}")

#_______________________________________________________________________________________________________
    def mostrar_itens_dentro_orcamento(self):#[3] = MOSTRA OS ITENS DENTRO DO ORÇAMENTO OBTIDO
        if self.orcamento_cliente <= 0:
            print("\nPor favor, defina primeiro um orçamento válido (opção 3 no menu)")
            return

        print(f"\nITENS DENTRO DO ORÇAMENTO (R$ {self.orcamento_cliente:.2f}):")

        itens_por_categoria = defaultdict(list)
        for item in self.itens:
            # Mostra apenas itens com preço menor ou igual ao orçamento
            if item.preco <= self.orcamento_cliente:
                itens_por_categoria[item.categoria].append(item)

        if not itens_por_categoria:
            print("\nNenhum item disponível dentro deste orçamento.")
            print("Sugerimos aumentar seu orçamento ou ver itens mais básicos.")
            return

        for categoria, itens in itens_por_categoria.items():
            print(f"\n[{categoria.upper()}]")
            for item in sorted(itens, key=lambda x: (-x.prioridade, x.preco)):
                print(f"  {item}")

#_______________________________________________________________________________________________________
    def definir_orcamento_cliente(self):#[3] = DEFINE O ORÇAMENTO A SER USADO
        while True:
            preco_input = input("\nInforme o valor que pretende investir em segurança: R$ ")
            preco_input = preco_input.replace(',', '.').replace(' ', '')

            try:
                self.orcamento_cliente = float(preco_input)
                if self.orcamento_cliente <= 0:
                    print("O valor deve ser maior que zero.")
                    continue

                print(f"\nOrçamento definido: R$ {self.orcamento_cliente:.2f}")
                self.mostrar_itens_dentro_orcamento()
                break

            except ValueError:
                print("Por favor, insira um valor numérico válido.")

#_______________________________________________________________________________________________________
    def selecionar_categorias(self):# [2] =  SELECIONA CATEGORIAS ESPECIFICAS DEFINIDAS
        print("\nCATEGORIAS DISPONÍVEIS:")
        for i, categoria in enumerate(self.categorias, 1):
            print(f"{i}. {categoria}")

        selecao = input("\nDigite os números das categorias (ex: 1,3): ")
        self.categorias_selecionadas = []

        try:
            indices = [int(i.strip()) - 1 for i in selecao.split(",") if i.strip().isdigit()]
            for idx in indices:
                if 0 <= idx < len(self.categorias):
                    self.categorias_selecionadas.append(self.categorias[idx])

            if self.categorias_selecionadas:
                print("\nCategorias selecionadas:")
                for cat in self.categorias_selecionadas:
                    print(f"- {cat}")
            else:
                print("...")
        except ValueError:
            print("Entrada inválida. Use números separados por vírgula.")

#_______________________________________________________________________________________________________
    def mostrar_itens_categorias_selecionadas(self):#[2] = MOSTRA OS ITENS DAS CATEGORIAS ESPECIFICAS
        if not self.categorias_selecionadas:
            print("Nenhuma categoria selecionada. Mostrando todos os itens.")
            self.mostrar_todos_itens()
            return

        print("\nITENS DAS CATEGORIAS SELECIONADAS:")
        for categoria in self.categorias_selecionadas:
            print(f"\n[{categoria.upper()}]")
            itens_cat = [item for item in self.itens if item.categoria == categoria]
            for item in sorted(itens_cat, key=lambda x: (-x.prioridade, x.preco)):
                print(f"  {item}")

#_______________________________________________________________________________________________________
    def selecionar_quantidades(self):#[4] = PERMITE SELECIONAR A QUATIDADE DE CERTOS ITENS DENTRO DO ORÇAMENTO
        if self.orcamento_cliente <= 0:
            print("\nPor favor, defina primeiro um orçamento (opção 3 no menu)")
            return {}

        selecao = {}
        saldo_disponivel = self.orcamento_cliente
        self.mostrar_itens_dentro_orcamento()

        while True:
            print(f"\nSaldo disponível: R$ {saldo_disponivel:.2f}")
            codigo = input("\nDigite o código do item (ou 'fim' para terminar): ").upper()

            if codigo == 'FIM':
                break

            item = next((i for i in self.itens if i.codigo == codigo), None)
            if not item:
                print("Código inválido. Tente novamente.")
                continue

            if item.preco > saldo_disponivel:
                print(f"Este item custa R$ {item.preco:.2f} e excede seu saldo disponível.")
                continue

            try:
                max_qtd = min(10, int(saldo_disponivel // item.preco))
                if max_qtd < 1:
                    print("Não há saldo suficiente para este item.")
                    continue

                quantidade = int(input(f"Quantidade para {item.nome} (max {max_qtd}): "))
                if quantidade <= 0 or quantidade > max_qtd:
                    print(f"Quantidade deve ser entre 1 e {max_qtd}.")
                    continue

                custo_total = item.preco * quantidade
                if custo_total > saldo_disponivel:
                    print(f"Isso excede seu saldo disponível em R$ {custo_total - saldo_disponivel:.2f}")
                    continue

                selecao[item] = quantidade
                saldo_disponivel -= custo_total
                print(f"Adicionado: {quantidade}x {item.nome} (R$ {custo_total:.2f})")
                print(f"Novo saldo: R$ {saldo_disponivel:.2f}")

            except ValueError:
                print("Por favor, digite um número válido.")

        return selecao

#_______________________________________________________________________________________________________
    def gerar_orcamento(self, itens):#[4] = # GERA O ORÇAMENTO A SER USANDO E SALVA
        if not itens:
            print("\nNenhum item selecionado para o orçamento.")
            return

        orcamento = Orcamento(itens)
        self.historico.adicionar_orcamento(orcamento)

        print("\n" + "="*50)
        print("ORÇAMENTO GERADO COM SUCESSO!")
        print("="*50)
        print(f"Data: {orcamento.data.strftime('%d/%m/%Y %H:%M')}")
        print("\nITENS SELECIONADOS:")
        for item, qtd in orcamento.itens:
            print(f"  {qtd}x {item.nome} - R$ {item.preco:.2f} cada")
        print("\n" + "="*50)
        print(f"TOTAL: R$ {orcamento.total:.2f}")
        print(f"SALDO RESTANTE: R$ {self.orcamento_cliente - orcamento.total:.2f}")
        print("="*50)

        self.forma_pagamento(orcamento.total)

#_______________________________________________________________________________________________________
    def consultar_historico(self):#[5] MOSTRA TODOS OS ORÇAMENTOS NO HISTÓRICO
        historico = self.historico.listar_orcamentos()

        if not historico:
            print("\nNenhum orçamento no histórico")
            return

        print("\nHISTÓRICO DE ORÇAMENTOS:")
        for i, orcamento in enumerate(historico):
            print(f"\n[{i}] {orcamento.data.strftime('%d/%m/%Y %H:%M')}")
            for item, qtd in orcamento.itens:
                print(f"  {qtd}x {item.nome}")
            print(f"  TOTAL: R${orcamento.total:.2f}")

#_______________________________________________________________________________________________________
    def comparar_orcamentos(self):#[6] = COMPARA OS ULTIMOS DOIS ORÇAMENTOS DO HISTÓRICO
        historico = self.historico.listar_orcamentos()

        if len(historico) < 2:
            print("\nÉ necessário ter pelo menos 2 orçamentos para comparar")
            return

        self.consultar_historico()

        try:
            idx1 = int(input("\nÍndice do primeiro orçamento: "))
            idx2 = int(input("Índice do segundo orçamento: "))
            self.historico.comparar_orcamentos(idx1, idx2)
        except ValueError:
            print("Digite números válidos")

#_______________________________________________________________________________________________________
    def forma_pagamento(self, total):#[4] = PERGUNTA A FORMA DE PAGAMENTO DESEJADAS
        print("\nBem-vindo ao sistema de pagamento!")
        print("========================")
        print("      [1] - CRÉDITO       ")
        print("      [2] - DÉBITO        ")
        print("      [3] - PIX           ")
        print("      [4] - COMBINAR      ")
        print("========================\n")
        while True:
                forma = input("\nQual a forma de pagamento? (1-4): ").strip().lower()
                if forma == "1":
                 self.calcular_parcelas(total)
                 break
                elif forma == "2":
                 print(f"Pagamento no débito: R$ {total:.2f}")
                 break
                elif forma == "3":
                  print(f"Pagamento via PIX: R$ {total:.2f}")
                  break
                elif forma == "4":
                 self.dividir_pagamento(total)
                 break
                else:
                 print("Forma de pagamento não reconhecida.")

#_______________________________________________________________________________________________________
    def calcular_parcelas(self, total):#[4] = CALCULA AS PARCELAS QUANDO FOR CRÉDITO
        while True:
            parcelas = input("Deseja parcelar em quantas vezes? (até 3x): ").strip()
            if parcelas in ["1", "2", "3"]:
                parcelas = int(parcelas)
                valor_parcela = total / parcelas
                print(f"\nPagamento no crédito: {parcelas}x de R$ {valor_parcela:.2f}")
                break
            else:
                print("Número de parcelas inválido. Máximo permitido é 3x.")

#_______________________________________________________________________________________________________
    def dividir_pagamento(self, total):#[4] = DIVIDE O PAGAMENTO EM MULTIPLAS FORMAS
        print("\nVocê escolheu combinar formas de pagamento (Ex: crédito e débito)")
        while True:
            try:
                valor_credito = float(input("Quanto deseja pagar no crédito? R$ ").replace(",", "."))
                valor_debito = float(input("Quanto deseja pagar no débito? R$ ").replace(",", "."))
                valor_pix = float(input("Quanto deseja pagar via PIX? R$ ").replace(",", "."))

                soma = valor_credito + valor_debito + valor_pix

                if abs(soma - total) <= 0.05:
                    if valor_credito > 0:
                        self.calcular_parcelas(valor_credito)
                    if valor_debito > 0:
                        print(f"Pagamento no débito: R$ {valor_debito:.2f}")
                    if valor_pix > 0:
                        print(f"Pagamento via PIX: R$ {valor_pix:.2f}")
                    break
                else:
                    print(f"A soma dos valores ({soma:.2f}) não bate com o valor total ({total:.2f}). Tente novamente.")
            except ValueError:
                print("Entrada inválida. Use números.")

#====================================================================================================================
    def executar(self):# EXECUÇÃO DO FLUxO PRINCIPAL DO SISTEMA
        """Executa o fluxo principal do sistema"""
        self.apresentacao_da_empresa()
        while True:
          while True:
            self.mostrar_menu_principal()
            opcao = input("\nEscolha uma opção numérica: ")

            if opcao == '1':
                self.mostrar_todos_itens()
                input("\nPressione Enter para continuar...")
                break
            elif opcao == '2':
                self.selecionar_categorias()
                self.mostrar_itens_categorias_selecionadas()
                input("\nPressione Enter para continuar...")
                break
            elif opcao == '3':
                self.definir_orcamento_cliente()
                input("\nPressione Enter para continuar...")
                break
            elif opcao == '4':
                selecao = self.selecionar_quantidades()
                if selecao:
                    self.gerar_orcamento(selecao)
                input("\nPressione Enter para continuar...")
                break
            elif opcao == "5":
                self.consultar_historico()
                input("\nPressione Enter para continuar...")
                break
            elif opcao == "6":
                self.comparar_orcamentos()
                input("\nPressione Enter para continuar...")
                break
            elif opcao == "7" or opcao == "sair":
                print("\nSaindo do sistema...")
                return
            else:
                print("Opção inválida, tente novamente ")
                continue

if __name__ == "__main__":
    sistema = SistemaSeguranca()
    sistema.executar()
