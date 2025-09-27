import re
import sys
from collections import namedtuple

# 1. Definição do Token (Tipo e Valor)
Token = namedtuple('Token', ['tipo', 'valor', 'linha', 'coluna'])

# 2. Palavras-Chave e Mapeamento de Tipos
# Priorizando a lista mais recente dos documentos (func, var, if, else, etc.)
PALAVRAS_CHAVE = {
    "and": "KWD", "or": "KWD", "not": "KWD",
    "if": "KWD", "else": "KWD", "for": "KWD",
    "while": "KWD", "return": "KWD", "break": "KWD",
    "continue": "KWD", "func": "KWD", "var": "KWD",
    "const": "KWD", "import": "KWD", "from": "KWD",
    "as": "KWD", "struct": "KWD", "enum": "KWD",
    "match": "KWD", "case": "KWD", "default": "KWD",
    "true": "KWD", "false": "KWD", "null": "KWD",
    "pub": "KWD", "extern": "KWD", "use": "KWD",
}

# 3. Definição das Regras Léxicas (Regexes)
# A ordem é crucial para a regra 'Maximal-Munch' e desambiguação
REGRAS = [
    # Espaços e Comentários (Ignorados)
    (r'[\t\f\r ]+', None), # WS
    (r'\n', None),          # NEWLINE (Tratado na contagem de linha/coluna)
    (r'/"[^\n]*', None),    # LINE_COMMENT
    (r'"""[\s\S]*?"""', None), # BLOCK_COMMENT

    # Tokens Compostos (Prioridade sobre os simples)
    (r'\.\.\.', 'DOT3'),     # ...
    (r'\.\.', 'DOT2'),      # ..
    (r'->', 'ARROW'),       # ->
    (r'\+=', 'PLUS_EQ'),    # +=

    # Literais de Texto
    (r'"(\\"|[^"])*"', 'STRING'), # Aspas duplas, aceita escape \"

    # Literais Numéricos (Floats e Inteiros - priorizar Float)
    # Notação científica: 1.0e-3
    (r'\d+(\.\d+)?([eE][+-]?\d+)', 'FLOAT_EXP'),
    (r'\d+\.\d+', 'FLOAT'),
    (r'\d+', 'DEC_INT'),

    # Identificadores e Palavras-chave
    # Começa com letra ou _, seguido por letras, dígitos ou _
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),

    # Operadores Simples
    (r'==', 'EQ'),
    (r'!=', 'NE'),
    (r'<=', 'LE'),
    (r'>=', 'GE'),
    (r'=', 'ASSIGN'),
    (r'\+', 'PLUS'),
    (r'-', 'MINUS'),
    (r'\*', 'STAR'),
    (r'/', 'SLASH'),
    (r'%', 'PERCENT'),
    (r'\^', 'CARET'),
    (r'>', 'GT'),
    (r'<', 'LT'),

    # Delimitadores
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'\{', 'LBRACE'),
    (r'\}', 'RBRACE'),
    (r';', 'SEMI'),
    (r':', 'COLON'),
    (r',', 'COMMA'),
    (r'\.', 'DOT'),
]

# Compila as regexes
regex_regras = [(re.compile(regex), token_tipo) for regex, token_tipo in REGRAS]

def analise_lexica(codigo_fonte):
    """
    Realiza a análise léxica do código-fonte e retorna a lista de tokens.
    Implementa o rastreamento de linha/coluna e o tratamento de erro.
    """
    tokens = []
    linha = 1
    coluna = 1
    pos = 0

    while pos < len(codigo_fonte):
        match = None

        # 1. Tenta casar com as regras de tokenização
        for regex, token_tipo in regex_regras:
            m = regex.match(codigo_fonte, pos)
            if m:
                match = m
                break
        
        if match:
            valor = match.group(0)
            token_tipo = match[0]
            
            # Atualiza a posição
            proxima_pos = match.end()
            tamanho_token = len(valor)

            # 2. Tratamento de Espaços, Comentários e Quebras de Linha
            if token_tipo is None:
                if valor == '\n':
                    linha += 1
                    coluna = 1
                else:
                    # Conta quebras de linha dentro de comentários de bloco
                    for char in valor:
                        if char == '\n':
                            linha += 1
                            coluna = 1
                        else:
                            coluna += 1
                
                pos = proxima_pos
                continue

            # 3. Tratamento de Palavras-Chave (Prioridade sobre ID)
            if token_tipo == 'ID':
                if valor in PALAVRAS_CHAVE:
                    token_tipo = PALAVRAS_CHAVE[valor]

            # 4. Adiciona o Token
            tokens.append(Token(token_tipo, valor, linha, coluna))

            # 5. Atualiza a Coluna
            # Assumindo que o Lexer do seu projeto incrementa a coluna APÓS o token
            coluna += tamanho_token
            pos = proxima_pos
        
        else:
            # 6. Trata Erro Léxico (Requisito da tarefa)
            caractere_invalido = codigo_fonte[pos]
            print(f"\nERRO LÉXICO: Caractere não reconhecido '{caractere_invalido}' "
                  f"encontrado na Linha {linha}, Coluna {coluna}.")
            
            # Estratégia de pânico: consome o caractere e tenta continuar
            if caractere_invalido == '\n':
                linha += 1
                coluna = 1
            else:
                coluna += 1
            
            # Retorna o token de erro e encerra, conforme a exigência do erro ser retornado
            # Você pode escolher consumir o caractere e continuar para encontrar mais erros.
            return [Token("LEXICAL_ERROR", caractere_invalido, linha, coluna)]

    return tokens

def imprimir_tabela(tokens):
    """ Imprime a tabela de tokens (valor e tipo). """
    print("\n--- Tabela de Tokens ---")
    print("{:<25} {:<15} {:<6} {:<6}".format("Token", "Tipo", "Lin", "Col"))
    print("-" * 52)
    for token in tokens:
        print(f"{token.valor:<25} {token.tipo:<15} {token.linha:<6} {token.coluna:<6}")
    print("-" * 52)

# 7. Execução Principal
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python lexer.py sample.cd")
        sys.exit(1)
    
    caminho_arquivo = sys.argv[1]
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        sys.exit(1)

    lista_tokens = analise_lexica(source_code)

    # Imprime a tabela apenas se não for um erro léxico que encerrou
    if not lista_tokens or lista_tokens[0].tipo != "LEXICAL_ERROR":
        imprimir_tabela(lista_tokens)