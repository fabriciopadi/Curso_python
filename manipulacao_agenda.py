import json

contatos_suportados = ("telefone", "email", "endereco")
agenda = {}

def agenda_para_txt(nome_arquivo:str, agenda):
    if ".txt" not in nome_arquivo:
        nome_arquivo = f"{nome_arquivo}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(agenda_para_texto(**agenda))
        print("Agenda exportada com sucesso!")

def agenda_para_json(nome_arquivo:str, agenda):
    if ".json" not in nome_arquivo:
        nome_arquivo = f"{nome_arquivo}.json"
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(agenda, indent=4, ensure_ascii=False))
            print("Agenda exportada com sucesso!")

def json_para_agenda(nome_arquivo:str):
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
        print("Agenda carregada com sucesso!")
        return json.loads(conteudo)
def contato_para_texto(nome_contato:str, **formas_contato):
    """Recebe um nome de contato com string e
     um dicionario com as formas de contato.
      Retorna uma string com os dados recebidos"""
    formato_texto = f"{nome_contato}"
    for meio_contato, contato in formas_contato.items():
        formato_texto = (f"{formato_texto}\n{meio_contato.upper()}")
        contador_formas = 1
        for valor in contato:
            formato_texto = (f"{formato_texto}\n{contador_formas} - {valor.upper()}")
            contador_formas = contador_formas + 1
    return  formato_texto

def agenda_para_texto(**agenda_completa):
    """Recebe um dicionario de dicionarios com a agenda que sera exibida
     e retorna uma string com este dicionario formatado"""
    formato_texto = ""
    for nome_contato, formas_contato in agenda_completa.items():
        formato_texto = (f"{formato_texto}\n{contato_para_texto(nome_contato, **formas_contato)}")
        formato_texto = f"{formato_texto}\n------------------------"
    return formato_texto

def altera_nome_contato(agenda_original:dict, nome_original:str, nome_atualizado:str):
    """Recebe a agenda original em forma de dicionario, o nome_original
    e o nome_atualizado em forma de string.
    Busca o nome original no dicionario e retorna False se nao encontrar.
    Retorna True se encontrar o nome original no dicionario
    e fizer a exclusao do contato antigo e inclusao do novo"""
    if nome_original in agenda_original.keys():
        copia_contatos = agenda_original[nome_original].copy()
        agenda_original.pop(nome_original)
        agenda_original[nome_atualizado] = copia_contatos
        return True
    return False
def altera_forma_contato(lista_contatos:list, valor_antigo:str, novo_valor:str):
    """Recebe uma list lista_contatos o valor antigo que sera substituido e o novo valor
    caso o valor antigo ainda nao esteja na lista, retornara False.
    Caso o valor antigo esteja na lista, sera removido, o novo valor sera incluido
     e retornara True"""
    if valor_antigo in lista_contatos:
        posicao_valor_antigo = lista_contatos.index(valor_antigo)
        lista_contatos.pop(posicao_valor_antigo)
        lista_contatos.insert(posicao_valor_antigo, novo_valor)
        return True
    return False

def exclui_contato(agenda:dict, nome_contato:str):
    """Recebe uma agenda completa como dicionario e o nome do contato como string.
    Caso o nome dos contatos nao esteja nas chaves do dicionario, retornara False.
    Caso o nome do contato esteja nas chaves, o registro correspondente sera
    removido e retornara True."""
    if nome_contato in agenda.keys():
        agenda.pop(nome_contato)
        return True
    return False
def inclui_contato(agenda:dict, nome_contato:str, **formas_contato):
    """Recebe uma agenda completa como dicionario, o nome do novo contato como string
    e as formas de contato em um dicionario como **kwargs.
    Nao e feita nenhuma verificacao, portanto se ja existir um contato com o mesmo nome,
    sera sobrescrito"""
    agenda[nome_contato] = formas_contato

def inclui_forma_contato(formas_contato:dict, forma_incluida:str, valor_incluido:str):
    """Recebe um dicionário com as formas de contato, a forma de contato
     que será incluida ou alterada e o valor que será incluído.
    Caso a forma de contato já possua valores, o novo valor será
    adicionado na lista e retornará True.
    Caso a forma de contato ainda não exista e estiver presente na
    tupla de formas de contatos suportados será incluída e
     o novo valor será incluído em uma lista, retornando True.
     Caso a forma de contato ainda não exista e não estiver presente na tupla de
    formas de contato suportados, retornará False"""
    if forma_incluida in formas_contato.keys():
        formas_contato[forma_incluida].append(valor_incluido)
        return True
    elif forma_incluida in contatos_suportados:
        formas_contato[forma_incluida] = [valor_incluido]
        return True
    return False

def usuario_inclui_contato(agenda:dict):
    nome = input("Informe o nome do novo contato que sera incluido na agenda: ")
    dicionario_formas = {}
    for forma in contatos_suportados:
        resposta = input(f"Deseja inserir um {forma} para {nome.upper()}? "
                         f"SIM ou NAO -> ")
        lista_contatos = []
        while "S" in resposta.upper():
            lista_contatos.append(input(f"Informe um {forma}: "))
            resposta = input(f"Deseja inserir outro {forma} para {nome.upper()}? "
                             f"SIM ou NAO -> ")
        if len(lista_contatos) > 0:
            dicionario_formas[forma] = lista_contatos.copy()
            lista_contatos.clear()
    if len(dicionario_formas.keys()) > 0:
        inclui_contato(agenda, nome, **dicionario_formas)
        print("Inclusao bem sucedida!")
    else:
        print("E necessario incluir pelo menos uma forma de contato!"
              "A agenda nao foi alterada.")

def usuario_inclui_forma_contato(agenda:dict):
    nome = input("Informe o nome do contato para qual deseja incluir formas de contato: ")
    if nome.upper() in agenda.keys():
        print(f"As formas de contato suportadas pelo sistema sao: {contatos_suportados} ")
        forma_incluida = input("Qual forma de contato deseja incluir? ")
        if forma_incluida in contatos_suportados:
            valor_incluido = input(f"Informe o {forma_incluida} que deseja incluir: ")
            if inclui_forma_contato(agenda[nome], forma_incluida, valor_incluido):
                print("Operacao bem sucedida! A nova forma de contato foi incluida!")
            else:
                print("Ocorreu um erro durante a insercao. A agenda nao foi alterada.")
        else:
            print("A forma de contato indicada nao e suportada pelo sistema. A agenda nao foi alterada")
    else:
        print("O contato informado nao existe na agenda. Nao foram feitas as alteracoes")

def usuario_altera_nome_contato(agenda:dict):
    nome_original = input("Informe o nome do contato que deseja alterar: ")
    nome_atualizado = input("Informe o nome do novo contato: ")
    if altera_nome_contato(agenda, nome_original, nome_atualizado):
        print(f"O contato foi atualizado e agora se chama {nome_atualizado}")
    else:
        print("O contato nao foi localizado. A agenda nao foi alterada.")

def usuario_altera_forma_contato(agenda:dict):
    nome = input("Informe o nome do contato que deseja alterar: ")
    if nome in agenda.keys():
        print(f"As formas suportadas pelo sistema sao: {contatos_suportados}")
        forma_incluida = input("Qual a forma de contato que deseja incluir? ")
        if forma_incluida in contatos_suportados:
            print(contato_para_texto(nome, **agenda[nome]))
            valor_antigo = input(f"Informe o {forma_incluida} que deseja alterar ")
            novo_valor = input(f"Informe o novo {forma_incluida}")
            if altera_forma_contato(agenda[nome][forma_incluida], valor_antigo, novo_valor):
                print("Contato alterado com sucesso!")
            else:
                print("Ocorreu um erro durante a alteracao do contato. A agenda nao foi alterada ")
        else:
            print(f"{forma_incluida} nao e uma forma de contato suportada pelo sistema.")
    else:
        print(f"O contato {nome} nao esta na agenda. A agenda nao foi alterada. ")

def usuario_contato_para_texto(agenda:dict):
    nome = input("Informe o nome do contato que deseja exibir: ")
    if nome in agenda.keys():
        print(contato_para_texto(nome, **agenda[nome]))
    else:
        print("O contato informado nao esta na agenda. ")

def usuario_exclui_contato(agenda:dict):
    nome = input("Informe o nome do contato que deseja excluir: ")
    if exclui_contato(agenda, nome):
        print("Usuario excluido com sucesso! ")
    else:
        print("Nome do usuario nao foi localizado na agenda. Nao foram feitas alteracoes ")
def exibe_menu():
    print("\n\n")
    print("1 - Incluir contato na agenda")
    print("2 - Incluir uma forma de contato")
    print("3 - Alterar o nome de um contao")
    print("4 - Alterar uma forma de contato")
    print("5 - Exibir um contato")
    print("6 - Exibir toda a agenda")
    print("7 - Excluir um contato")
    print("8 - Exportar uma agenda para txt")
    print("9 - Exportar uma agenda para JSON")
    print("10 - Importar agenda de JSON")
    print("11 - Sair")
    print("\n")

def manipulador_agenda():
    agenda = {}
    op = 1
    while op != 11:
        exibe_menu()
        op = int(input("Informe a opcao desejada: "))
        if op == 1:
            usuario_inclui_contato(agenda)
        elif op == 2:
            usuario_inclui_forma_contato(agenda)
        elif op == 3:
            usuario_altera_nome_contato(agenda)
        elif op == 4:
            usuario_altera_forma_contato(agenda)
        elif op == 5:
            usuario_contato_para_texto(agenda)
        elif op == 6:
            print(agenda_para_texto(**agenda))
        elif op == 7:
            usuario_exclui_contato(agenda)
        elif op == 8:
            nome_arquivo = input("Informe o nome ou caminho do arquivo: ")
            agenda_para_txt(nome_arquivo, agenda)
        elif op == 9:
            nome_arquivo = input("Informe o nome ou caminho do arquivo: ")
            agenda_para_json(nome_arquivo, agenda)
        elif op == 10:
            nome_arquivo = input("Informe o nome ou caminho do arquivo: ")
            agenda = json_para_agenda(nome_arquivo)
        elif op == 11:
            print("Saindo do sistema")
            break
        else:
            print("Opcao invalida! Informe uma opcao existente.")

manipulador_agenda()