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
Saída S = 1: reúne os documentos para solicitar o título

Fonte das regras: TSE, "Eleitor em Dia: confira quais documentos são
necessários para tirar o título até 6 de maio" (05/03/2026, atualizada
em 08/07/2026). Consultada em 08/11/2026.
"""
from itertools import product

AVISO = ("AVISO: protótipo acadêmico. Não é um canal oficial e não confirma "
         "a concessão de serviços ou direitos. Nenhum dado pessoal é coletado.")

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
    while True:
        resposta = input(f"{pergunta} (1 = Sim e 0 = Não): ").strip()
        if resposta in ("0", "1"):
            return int(resposta)
        print("Entrada inválida. Digite apenas 0 ou 1.")


def nao(x):
    return 1 - x


def regra_original(A, B, C, D):
    """Regra escrita como na fonte (TSE), com if/else."""
    if B == 0 or C == 0:
        return 0
    if A == 1 and D == 0:
        return 0
    return 1


def forma_canonica(A, B, C, D):
    """Soma de mintermos: S = A'BCD' + A'BCD + ABCD  (Σm(6, 7, 15))"""
    m6 = nao(A) & B & C & nao(D)
    m7 = nao(A) & B & C & D
    m15 = A & B & C & D
    return m6 | m7 | m15


def expressao_simplificada(A, B, C, D):
    """S = B . C . (A' + D)
    Se o seu Karnaugh/álgebra der outra forma equivalente, troque aqui."""
    return B & C & (nao(A) | D)


def decidir(A, B, C, D):
    return expressao_simplificada(A, B, C, D)


def faltando(A, B, C, D):
    itens = []
    if B == 0:
        itens.append("Documento oficial de identificação com foto")
    if C == 0:
        itens.append("Comprovante de residência recente")
    if A == 1 and D == 0:
        itens.append("Comprovante de quitação do serviço militar")
    return itens


def validar_tudo():
    print("A B C D | regra | canônica | simplificada | tabela | execução")
    for A, B, C, D in product((0, 1), repeat=4):
        r = regra_original(A, B, C, D)
        c = forma_canonica(A, B, C, D)
        s = expressao_simplificada(A, B, C, D)
        t = TABELA_VERDADE[(A, B, C, D)]
        x = decidir(A, B, C, D)
        print(f"{A} {B} {C} {D} |   {r}   |    {c}     |      {s}       |   {t}    |    {x}")
        assert r == c == s == t == x, (A, B, C, D, r, c, s, t, x)
    print("Todas as 16 combinações conferem.")


def atendimento():
    print("==== PRIMEIRA VIA DO TÍTULO DE ELEITOR ====")
    print(AVISO + "\n")
    A = pedir_bit("É homem e completa 19 anos neste ano?")
    B = pedir_bit("Tem documento oficial de identificação com foto?")
    C = pedir_bit("Tem comprovante de residência recente?")
    D = pedir_bit("Tem comprovante de quitação do serviço militar?")

    if decidir(A, B, C, D) == 1:
        print("\nPelas respostas, você reúne os documentos para solicitar o título.")
        print("Procure o cartório eleitoral ou o Autoatendimento do TSE. "
              "A biometria precisa ser coletada presencialmente.")
    else:
        print("\nPelas respostas, ainda falta:")
        for item in faltando(A, B, C, D):
            print(" -", item)


if __name__ == "__main__":
    escolha = input("1 = Atendimento | 2 = Validar as 16 combinações: ").strip()
    if escolha == "2":
        validar_tudo()
    else:
        atendimento()