
"""
Citizen Assist AI - módulo de decisão lógica (GS26_2)

AVISO: protótipo acadêmico. NÃO é um canal oficial e NÃO confirma a
concessão de serviços ou direitos. Nenhum dado pessoal é coletado:
apenas respostas de 0/1 sobre as condições do atendimento.

Variáveis (1 = Sim, 0 = Não):
A = é homem e completa 19 anos neste ano
B = tem documento oficial de identificação com foto
C = tem comprovante de residência recente
D = tem comprovante de quitação do serviço militar

Saída S = 1: reúne os documentos para solicitar o título.

Fonte das regras: TSE, "Eleitor em Dia: confira quais documentos são
necessários para tirar o título até 6 de maio" (05/03/2026, atualizada
em 08/07/2026). Consultada em 09/11/2026.
"""

from itertools import product


AVISO = (
    "AVISO: protótipo acadêmico. Não é um canal oficial e não confirma "
    "a concessão de serviços ou direitos. Nenhum dado pessoal é coletado."
)


TABELA_VERDADE = {
    (0, 0, 0, 0): 0,
    (0, 0, 0, 1): 0,
    (0, 0, 1, 0): 0,
    (0, 0, 1, 1): 0,
    (0, 1, 0, 0): 0,
    (0, 1, 0, 1): 0,
    (0, 1, 1, 0): 1,
    (0, 1, 1, 1): 1,
    (1, 0, 0, 0): 0,
    (1, 0, 0, 1): 0,
    (1, 0, 1, 0): 0,
    (1, 0, 1, 1): 0,
    (1, 1, 0, 0): 0,
    (1, 1, 0, 1): 0,
    (1, 1, 1, 0): 0,
    (1, 1, 1, 1): 1,
}


def pedir_bit(pergunta):
    """Solicita uma entrada binária e valida a resposta."""
    while True:
        resposta = input(
            f"{pergunta} (1 = Sim e 0 = Não): "
        ).strip()

        if resposta in ("0", "1"):
            return int(resposta)

        print("Entrada inválida. Digite apenas 0 ou 1.")


def nao(x):
    """Retorna o complemento de uma variável binária."""
    return 1 - x


def regra_original(A, B, C, D):
    """Regra original representada por estruturas condicionais."""

    if B == 0 or C == 0:
        return 0

    if A == 1 and D == 0:
        return 0

    return 1


def forma_canonica(A, B, C, D):
    """
    Soma de mintermos:
    S = A'BCD' + A'BCD + ABCD
    S = m6 + m7 + m15
    """

    m6 = nao(A) & B & C & nao(D)
    m7 = nao(A) & B & C & D
    m15 = A & B & C & D

    return m6 | m7 | m15


def expressao_simplificada(A, B, C, D):
    """
    Expressão simplificada:
    S = B . C . (A' + D)
    """

    return B & C & (nao(A) | D)


def decidir(A, B, C, D):
    """Executa a decisão utilizando a expressão simplificada."""
    return expressao_simplificada(A, B, C, D)


def faltando(A, B, C, D):
    """Identifica as condições documentais pendentes."""

    itens = []

    if B == 0:
        itens.append(
            "Documento oficial de identificação com foto"
        )

    if C == 0:
        itens.append(
            "Comprovante de residência recente"
        )

    if A == 1 and D == 0:
        itens.append(
            "Comprovante de quitação do serviço militar"
        )

    return itens


def validar_tudo():
    """Compara as cinco representações nas 16 combinações."""

    print("\n==== VALIDAÇÃO DA LÓGICA ====")
    print("A B C D | regra | canônica | simplificada | tabela | execução")
    print("-" * 68)

    for A, B, C, D in product((0, 1), repeat=4):

        r = regra_original(A, B, C, D)
        c = forma_canonica(A, B, C, D)
        s = expressao_simplificada(A, B, C, D)
        t = TABELA_VERDADE[(A, B, C, D)]
        x = decidir(A, B, C, D)

        print(
            f"{A} {B} {C} {D} |"
            f"   {r}   |"
            f"    {c}     |"
            f"      {s}       |"
            f"   {t}    |"
            f"    {x}"
        )

        assert r == c == s == t == x, (
            A, B, C, D, r, c, s, t, x
        )

    print("\nTodas as 16 combinações conferem!")
    print("As representações são equivalentes.")


def exibir_mapa_karnaugh():
    """Exibe o mapa de Karnaugh utilizando a tabela-verdade."""

    print("\n==== MAPA DE KARNAUGH ====")
    print("     CD")
    print("AB | 00 | 01 | 11 | 10")
    print("-------------------------")

    # Sequência Gray das linhas e colunas
    ordem_gray = ("00", "01", "11", "10")

    for ab in ordem_gray:

        A, B = map(int, ab)
        valores = []

        for cd in ordem_gray:

            C, D = map(int, cd)

            resultado = TABELA_VERDADE[(A, B, C, D)]
            valores.append(resultado)

        print(f"{ab} |  " + " |  ".join(map(str, valores)))

    print("\n==== AGRUPAMENTOS ====")
    print("Grupo 1: m6 e m7  -> A' . B . C")
    print("Grupo 2: m7 e m15 -> B . C . D")

    print("\n==== EXPRESSÃO SIMPLIFICADA ====")
    print("S = A'BC + BCD")
    print("S = BC(A' + D)")


def atendimento():
    """Executa o atendimento interativo."""

    print("\n==== PRIMEIRA VIA DO TÍTULO DE ELEITOR ====")
    print(AVISO + "\n")

    A = pedir_bit(
        "É homem e completa 19 anos neste ano?"
    )

    B = pedir_bit(
        "Tem documento oficial de identificação com foto?"
    )

    C = pedir_bit(
        "Tem comprovante de residência recente?"
    )

    D = pedir_bit(
        "Tem comprovante de quitação do serviço militar?"
    )

    if decidir(A, B, C, D) == 1:

        print(
            "\nPelas respostas, você reúne os documentos "
            "para solicitar o título."
        )

        print(
            "Procure o cartório eleitoral ou o Autoatendimento "
            "do TSE. A biometria precisa ser coletada presencialmente."
        )

    else:

        print("\nPelas respostas, ainda falta:")

        itens = faltando(A, B, C, D)

        if itens:
            for item in itens:
                print(" -", item)
        else:
            print(
                " - Verifique as condições do atendimento "
                "junto à Justiça Eleitoral."
            )

    print("\n" + AVISO)


def menu():
    """Menu principal do Citizen Assist AI."""

    while True:

        print("\n========== CITIZEN ASSIST AI ==========")
        print("1 = Atendimento")
        print("2 = Validar as 16 combinações")
        print("3 = Exibir mapa de Karnaugh")
        print("0 = Sair")
        print("=======================================")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            atendimento()

        elif escolha == "2":
            validar_tudo()

        elif escolha == "3":
            exibir_mapa_karnaugh()

        elif escolha == "0":
            print("\nEncerrando o Citizen Assist AI...")
            break

        else:
            print("\nOpção inválida. Digite 0, 1, 2 ou 3.")


if __name__ == "__main__":
    menu()
