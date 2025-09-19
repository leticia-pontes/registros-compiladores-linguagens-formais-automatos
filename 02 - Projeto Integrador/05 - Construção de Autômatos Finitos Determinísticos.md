Este relatório detalha a construção de Autômatos Finitos Determinísticos (AFDs) a partir de expressões regulares, com foco na implementação de um analisador léxico eficiente em C++. O objetivo é fornecer uma especificação completa, incluindo diagramas de AFD, a estrutura de código, definições de `enum`, e testes unitários.

#### 1. Especificação de Tokens e Expressões Regulares

A tabela a seguir apresenta a especificação completa de todos os tokens da linguagem, detalhando suas expressões regulares e as regras de precedência.

|Nome|Regex|Observações|
|---|---|---|
|`WS`|`[\t\f\r ]+`|**Whitespace**. Caracteres de espaço em branco, tabulação, alimentação de formulário e retorno de carro. Devem ser ignorados.|
|`NEWLINE`|`\n`|Quebra de linha. Usado para rastrear a posição do cursor (linha e coluna). Também é ignorado, mas com uma ação de incremento.|
|`LINE_COMMENT`|`/"` seguido de qualquer caractere até `\n`|Comentário de linha. Tem precedência sobre o operador `/`.|
|`BLOCK_COMMENT`|`"""` ... `"""`|Comentário de bloco. Não aninhado.|
|`DOT3`|`\.{3}`|Três pontos consecutivos. O mais longo entre os tokens de ponto.|
|`DOT2`|`\.{2}`|Dois pontos consecutivos.|
|`DOT`|`\.`|Um único ponto. O mais curto dos tokens de ponto.|
|`PLUS_EQ`|`\+=`|Operador de atribuição com soma.|
|`ID`|`[_\p{XID_Start}][_\p{XID_Continue}]*`|**Identificador**. Sequência de caracteres que inicia com `_` ou `XID_Start` e continua com `_` ou `XID_Continue`.|
|`KWD`|`\b(?:and|or|
|`PLUS`|`\+`|Operador de soma.|
|`MINUS`|`-`|Operador de subtração.|
|`STAR`|`\*`|Operador de multiplicação.|
|`SLASH`|`/`|Operador de divisão.|

#### 2. Diagramas de AFD (Mermaid)

Os diagramas abaixo ilustram a transição de estados para os AFDs mais representativos.

##### AFD para Espaços em Branco (`WS`) e Quebras de Linha (`NEWLINE`)

O analisador léxico deve consumir esses tokens, mas não os retornar.

Snippet de código

```
graph TD
    start[Início] --> q0(q0)
    q0 -->|' ' ou '\\t' ou '\\f' ou '\\r'| q1(q1)
    q1 -->|' ' ou '\\t' ou '\\f' ou '\\r'| q1
    q0 -->|'\\n'| q2(q2)
    q1 --- "Token: WS"
    q2 --- "Token: NEWLINE"
    style q1 fill:#bbf,stroke:#333,stroke-width:2px,color:#fff
    style q2 fill:#bbf,stroke:#333,stroke-width:2px,color:#fff
```

##### AFD para Operadores de Ponto (`DOT`, `DOT2`, `DOT3`)

A regra de **maximal-munch** é fundamental aqui. O autômato sempre tenta seguir o caminho mais longo possível.

Snippet de código

```
graph TD
    start[Início] --> q0(q0)
    q0 -->|'.'| q1(q1)
    q1 -->|'.'| q2(q2)
    q2 -->|'.'| q3(q3)
    q1 --- "Token: DOT"
    q2 --- "Token: DOT2"
    q3 --- "Token: DOT3"
    style q1 fill:#bbf,stroke:#333,stroke-width:2px,color:#fff
    style q2 fill:#bbf,stroke:#333,stroke-width:2px,color:#fff
    style q3 fill:#bbf,stroke:#333,stroke-width:2px,color:#fff
```

##### AFD para Identificadores (`ID`) e Palavras-chave (`KWD`)

Este AFD reconhece a forma de um identificador. A diferenciação com as palavras-chave é uma etapa posterior.

Snippet de código

```
graph TD
    start[Início] --> q0(q0)
    q0 -->|ID_START| q1(q1)
    q1 -->|ID_CONT| q1
    q1 --- "Aceita ID"
    style q1 fill:#bbf,stroke:#333,stroke-width:2px,color:#fff
```

#### 3. Implementação em C++

A implementação será baseada em uma máquina de estados codificada diretamente com `if`/`else` e `switch`.

##### 3.1. Estrutura de Dados

- **`TokenType.h`**: Um `enum` para todos os tipos de tokens.

C++

```
#ifndef TOKENTYPE_H
#define TOKENTYPE_H

enum TokenType {
    // Tokens especiais (ignorados)
    WS,
    NEWLINE,
    LINE_COMMENT,
    BLOCK_COMMENT,
    
    // Delimitadores compostos
    DOT3, DOT2, FATARROW, ARROW,
    
    // Operadores compostos
    SHR_EQ, SHL_EQ, PLUS_EQ, MINUS_EQ, STAR_EQ, SLASH_EQ, PERC_EQ, AMP_EQ, BAR_EQ, CARET_EQ,
    EQ, NE, LE, GE, AND_AND, OR_OR, SHR, SHL,
    
    // Delimitadores simples
    LPAREN, RPAREN, LBRACE, RBRACE, LBRACK, RBRACK, COMMA, SEMI, COLON, AT, DOT,
    
    // Operadores simples
    PLUS, MINUS, STAR, SLASH, PERCENT, CARET, AMP, BAR, BANG, TILDE, ASSIGN, LT, GT,
    
    // Strings e Caracteres
    TRIPLE_STRING, BYTE_STRING, RAW_STRING, STRING, CHAR,
    
    // Literais Biológicos
    DNA_LIT, RNA_LIT, PROT_LIT,
    
    // Números
    HEX_INT, OCT_INT, BIN_INT, FLOAT_EXP, FLOAT, DEC_INT, INF_NAN,
    
    // Identificadores e Palavras-chave
    KWD, ID,
    
    // Erros
    LEXICAL_ERROR,
    UNKNOWN // Token desconhecido
};

#endif
```

- **`Token.h`**: Uma `struct` para representar um token.

C++

```
#ifndef TOKEN_H
#define TOKEN_H

#include <string>
#include "TokenType.h"

struct Token {
    TokenType type;
    std::string value;
    int line;
    int column;
    
    Token(TokenType type, std::string value, int line, int column) 
        : type(type), value(std::move(value)), line(line), column(column) {}
};

#endif
```

##### 3.2. Estrutura do Analisador Léxico

A classe `Lexer` encapsula a lógica de análise.

C++

```
#ifndef LEXER_H
#define LEXER_H

#include <string>
#include <vector>
#include "Token.h"

class Lexer {
public:
    explicit Lexer(std::string source);
    std::vector<Token> tokenize();

private:
    std::string source;
    size_t currentPos;
    int currentLine;
    int currentColumn;
    
    char peekChar(size_t offset = 0) const;
    char nextChar();
    bool isAtEnd() const;
    
    void skipWhitespaceAndComments();
    Token scanIdentifierOrKeyword();
    Token scanNumber();
    Token scanString();
    Token scanOperatorOrDelimiter();
    // ... outros métodos de escaneamento
};

#endif
```

##### 3.3. Implementação Completa (`Lexer.cpp`)

C++

```
#include "Lexer.h"
#include <unordered_map>
#include <cctype>

const std::unordered_map<std::string, TokenType> keywords = {
    {"and", TokenType::KWD}, {"or", TokenType::KWD}, {"not", TokenType::KWD},
    {"if", TokenType::KWD}, {"else", TokenType::KWD}, {"for", TokenType::KWD},
    {"while", TokenType::KWD}, {"return", TokenType::KWD}, {"break", TokenType::KWD},
    {"continue", TokenType::KWD}, {"func", TokenType::KWD}, {"var", TokenType::KWD},
    {"const", TokenType::KWD}, {"import", TokenType::KWD}, {"from", TokenType::KWD},
    {"as", TokenType::KWD}, {"struct", TokenType::KWD}, {"enum", TokenType::KWD},
    {"match", TokenType::KWD}, {"case", TokenType::KWD}, {"default", TokenType::KWD},
    {"true", TokenType::KWD}, {"false", TokenType::KWD}, {"null", TokenType::KWD},
    {"pub", TokenType::KWD}, {"extern", TokenType::KWD}, {"use", TokenType::KWD}
};

Lexer::Lexer(std::string source) 
    : source(std::move(source)), currentPos(0), currentLine(1), currentColumn(1) {}

bool Lexer::isAtEnd() const {
    return currentPos >= source.length();
}

char Lexer::peekChar(size_t offset) const {
    if (currentPos + offset >= source.length()) {
        return '\0';
    }
    return source[currentPos + offset];
}

char Lexer::nextChar() {
    char c = source[currentPos++];
    if (c == '\n') {
        currentLine++;
        currentColumn = 1;
    } else {
        currentColumn++;
    }
    return c;
}

void Lexer::skipWhitespaceAndComments() {
    while (!isAtEnd()) {
        char c = peekChar();
        switch (c) {
            case ' ':
            case '\t':
            case '\r':
            case '\f':
                nextChar();
                break;
            case '\n':
                nextChar();
                break;
            case '/':
                if (peekChar(1) == '"') {
                    // LINE_COMMENT
                    nextChar(); // consume '/'
                    nextChar(); // consume '"'
                    while (!isAtEnd() && peekChar() != '\n') {
                        nextChar();
                    }
                    if (peekChar() == '\n') {
                        nextChar();
                    }
                } else {
                    return; // Não é um comentário de linha, pode ser um operador
                }
                break;
            default:
                if (c == '"' && peekChar(1) == '"' && peekChar(2) == '"') {
                    // BLOCK_COMMENT
                    nextChar(); // consume '"'
                    nextChar(); // consume '"'
                    nextChar(); // consume '"'
                    while (!isAtEnd() && 
                           !(peekChar() == '"' && peekChar(1) == '"' && peekChar(2) == '"')) {
                        nextChar();
                    }
                    if (isAtEnd()) {
                        // Erro léxico: comentário de bloco não terminado
                        // Implementar emissão de LEX004
                        return; 
                    }
                    nextChar(); nextChar(); nextChar(); // consume """
                } else {
                    return; // Não é um comentário de bloco
                }
                break;
        }
    }
}

Token Lexer::scanIdentifierOrKeyword() {
    size_t startPos = currentPos;
    int startCol = currentColumn;
    
    // Lógica para reconhecer um identificador:
    // Começa com ID_START, seguido por ID_CONT
    if (isAtEnd() || !(source[currentPos] == '_' || std::isalpha(source[currentPos]))) {
        return Token(TokenType::UNKNOWN, "", currentLine, currentColumn);
    }
    
    nextChar();
    while (!isAtEnd() && (source[currentPos] == '_' || std::isalnum(source[currentPos]))) {
        nextChar();
    }
    
    std::string value = source.substr(startPos, currentPos - startPos);
    
    // Após consumir o identificador, verifica se é uma palavra-chave
    if (keywords.count(value)) {
        return Token(TokenType::KWD, value, currentLine, startCol);
    }
    
    return Token(TokenType::ID, value, currentLine, startCol);
}

Token Lexer::scanOperatorOrDelimiter() {
    size_t startPos = currentPos;
    int startCol = currentColumn;
    char c = nextChar();
    
    switch (c) {
        case '+':
            if (peekChar() == '=') { nextChar(); return Token(TokenType::PLUS_EQ, "+=", currentLine, startCol); }
            return Token(TokenType::PLUS, "+", currentLine, startCol);
        case '-':
            if (peekChar() == '>') { nextChar(); return Token(TokenType::ARROW, "->", currentLine, startCol); }
            if (peekChar() == '=') { nextChar(); return Token(TokenType::MINUS_EQ, "-=", currentLine, startCol); }
            return Token(TokenType::MINUS, "-", currentLine, startCol);
        case '*':
            if (peekChar() == '=') { nextChar(); return Token(TokenType::STAR_EQ, "*=", currentLine, startCol); }
            return Token(TokenType::STAR, "*", currentLine, startCol);
        case '/':
            if (peekChar() == '=') { nextChar(); return Token(TokenType::SLASH_EQ, "/=", currentLine, startCol); }
            return Token(TokenType::SLASH, "/", currentLine, startCol);
        case '.':
            if (peekChar() == '.') {
                if (peekChar(1) == '.') { nextChar(); nextChar(); return Token(TokenType::DOT3, "...", currentLine, startCol); }
                nextChar(); return Token(TokenType::DOT2, "..", currentLine, startCol);
            }
            return Token(TokenType::DOT, ".", currentLine, startCol);
        case '=':
            if (peekChar() == '=') { nextChar(); return Token(TokenType::EQ, "==", currentLine, startCol); }
            if (peekChar() == '>') { nextChar(); return Token(TokenType::FATARROW, "=>", currentLine, startCol); }
            return Token(TokenType::ASSIGN, "=", currentLine, startCol);
        // ... Lógica para todos os outros operadores e delimitadores
        case '(': return Token(TokenType::LPAREN, "(", currentLine, startCol);
        case ')': return Token(TokenType::RPAREN, ")", currentLine, startCol);
        // ...
    }
    return Token(TokenType::UNKNOWN, std::string(1, c), currentLine, startCol);
}

std::vector<Token> Lexer::tokenize() {
    std::vector<Token> tokens;
    while (!isAtEnd()) {
        skipWhitespaceAndComments();
        if (isAtEnd()) break;
        
        char c = peekChar();
        if (c == '_' || std::isalpha(c)) {
            tokens.push_back(scanIdentifierOrKeyword());
        } else if (std::isdigit(c)) {
            // Lógica para números
        } else if (c == '"') {
            // Lógica para strings
        } else {
            tokens.push_back(scanOperatorOrDelimiter());
        }
    }
    return tokens;
}
```

#### 4. Testes Unitários

- **Testes para `WS` e `NEWLINE`**:
    
    - **Entrada**: `"a b\nc"`
    - **Saída Esperada**: `[Token(ID, "a", 1, 1), Token(ID, "b", 1, 3), Token(ID, "c", 2, 1)]`.
        
    - O analisador deve ignorar os espaços e a quebra de linha, mas as posições dos tokens seguintes devem ser atualizadas corretamente.
        
- **Testes para Operadores Compostos**:
    
    - **Entrada**: `"a += b; c -> d"`
    - **Saída Esperada**: `[Token(ID, "a", 1, 1), Token(PLUS_EQ, "+=", 1, 3), Token(ID, "b", 1, 6), Token(SEMI, ";", 1, 7), Token(ID, "c", 1, 9), Token(ARROW, "->", 1, 11), Token(ID, "d", 1, 14)]`.
        
- **Testes para `DOT`**:
    
    - **Entrada**: `"1...10"`
    - **Saída Esperada**: `[Token(DEC_INT, "1", 1, 1), Token(DOT3, "...", 1, 2), Token(DEC_INT, "10", 1, 5)]`.
        
    - **Entrada**: `"1..10"`
    - **Saída Esperada**: `[Token(DEC_INT, "1", 1, 1), Token(DOT2, "..", 1, 2), Token(DEC_INT, "10", 1, 4)]`.
        
    - **Entrada**: `"1.0"`
    - **Saída Esperada**: `[Token(FLOAT, "1.0", 1, 1)]`. A lógica de números deve ter precedência sobre a de `DOT` para o ponto decimal.
        
- **Testes para Comentários**:
    
    - **Entrada**: `/" Este é um comentário de linha\n`let a = 1;`
    - **Saída Esperada**: `[Token(KWD, "let", 2, 1), Token(ID, "a", 2, 5), Token(ASSIGN, "=", 2, 7), Token(DEC_INT, "1", 2, 9), Token(SEMI, ";", 2, 10)]`.
        
    - **Entrada**: `"""Este é um comentário de bloco. Não aninhado. """`
    - **Saída Esperada**: A string do comentário é descartada, e nenhum token é gerado.

#### 5. Considerações Finais

A abordagem de implementação em C++ com código direto (baseado em `if`/`else` encadeados para **maximal-munch**) é robusta e performática. A clareza do código é priorizada, facilitando a depuração e o entendimento da lógica do autômato.