
---

## 1) Visão geral do fluxo

```
fonte (.ar) ──► Lexer (tokens) ──► Parser (AST) ──► Interpreter (execução)

										└─► Env (escopos)
```


1. **Lexer** lê caracteres e produz **tokens** (número, string, `+`, `let`, etc.).

2. **Parser** consome tokens e constrói a **AST** (árvore sintática) seguindo a gramática.

3. **Interpreter** caminha na AST e **avalia/ executa** nós (expressões/declarações).

4. **Env** é a cadeia de escopos (dicionários) onde variáveis e **funções nativas** ficam guardadas.


---

## 2) Léxico (Lexer)

O **lexer** transforma **texto cru** → **tokens**.

### Tabela de tokens

- Lista/Mapa/Dicionário de tokens e suas regras com regex (expressão regular) para cada tipo (`NUMBER`, `STRING`, `MINUS`, ...).

- Palavras chaves(keywords) mapeia lexemas como `let`, `if`, `while` para tipos especiais.

  
### Como o scanner funciona

- Percorre o texto a partir da posição atual/primária.

- Ignora **espaços**, **comentários** e trata `\n` para atualizar **linha/coluna**.

- Converte números para `int` ou `float` e **"desencapar"** strings (`"\n"`, `\"`, etc.).

- Se não houver correspondência, lança **SyntaxError** com trecho/contexto.


> Resultado: `Tokens(kind, lexeme, literal, line, col)`

### Lista/Mapa/Dicionário de Tokens

É uma lista **ordenada** de Tokens. Cada pedaço reconhecido do código é convertido em um **objeto `Token`** com os campos `kind, lexeme, literal, line, col` e terminada por `EOF` :

-  **Kind**
	→ o tipo do token (ex: `NUMBER`, `STRING`, `PLUS`, `LET`, `IF`).
- **Lexeme** 
	→ o texto literal encontrado (ex: `"123"`, `"+"`, `"let"`).
 - **Literal** 
	 → o valor “interpretado” (ex: número `123` em vez da string `"123"`, ou a string sem aspas).
- **Line**
	→ a linha do código onde apareceu.
- **Col**
	→ a coluna inicial (posição horizontal) na linha.

> **`EOF`:**
>→ Significa **End Of File** (fim do arquivo).
>→ É um token especial adicionado no final da lista para indicar que não há mais nada para ler.
>→ Isso ajuda o parser depois a saber claramente onde a entrada terminou.
  

---

## 3) Gramática e Parser

O **parser** transforma **tokens** → **árvore sintática**.

### **EBNF** (Extended Backus–Naur Form) → "trecho essencial"

Serve como **receita** de como construir frases válidas (programas) nessa linguagem.

O **parser** vai usar essa gramática para transformar a lista de `Tokens`(que o lexer produziu) em uma **árvore sintática**.

> **Árvore sintática** (**parse tree** ou **AST – Abstract Syntax Tree**): é a estrutura de dados que o **parser** monta a partir da lista de tokens.

#### 2. Estrutura Geral

- Um programa é uma sequência de **declarações**.
	**"`program := { declaration }`"**  

- Cada declaração pode ser uma **declaração de variável** (`let`...) ou um **comando** (`if`, `while`, `print`, expressão, bloco...).
	**"`declaration := varDecl | statement`"**  

#### 3. Declarações e Statements

- **`varDecl`** → `let x = expr;`
    
- **`printStmt`** → `print expr;`
    
- **`ifStmt`** → `if (expr) stmt [else stmt]`
    
- **`whileStmt`** → `while (expr) stmt`
    
- **`exprStmt`** → `expr;`
    
- **`block`** → `{ decl decl decl }`

---

#### 4. Expressões

As regras seguem a **precedência dos operadores**:

1. **assignment** → `x = expr`
    
2. **logic_or** → `a || b`
    
3. **logic_and** → `a && b`
    
4. **equality** → `==`, `!=`
    
5. **comparison** → `<`, `<=`, `>`, `>=`
    
6. **term** → `+`, `-`
    
7. **factor** → `*`, `/`, `%`
    
8. **unary** → `-expr`, `!expr`
    
9. **call** → `fun(args)`
    
10. **primary** → número, string, booleano, identificador, ou `(expr)`

```

program := { declaration }

declaration := varDecl | statement
	
	varDecl := 'let' IDENT '=' expression ';'
	
	statement := printStmt | ifStmt | whileStmt | exprStmt | block
		
		printStmt := 'print' expression ';'
		
		ifStmt := 'if' '(' expression ')' statement [ 'else' statement ]
		
		whileStmt := 'while' '(' expression ')' statement
		
		exprStmt := expression ';'
		
		block := '{' { declaration } '}'

  
expression := assignment
	
	assignment := IDENT '=' assignment | logic_or
		
		logic_or := logic_and { '||' logic_and }
			
		logic_and := equality { '&&' equality }
			
		equality := comparison { ( '==' | '!=' ) comparison }
			
		comparison := term { ( '>' | '>=' | '<' | '<=' ) term }
			
		term := factor { ( '+' | '-' ) factor }
			
		factor := unary { ( '*' | '/' | '%' ) unary }
			
		unary := ( '!' | '-' ) unary | call
			
		call := primary { '(' [ arguments ] ')' }
			
		arguments := expression { ',' expression }

primary := NUMBER | STRING | 'true' | 'false' | IDENT | '(' expression ')'

```

  

> **Observação:** a edição **Bio (v3)** já suporta **chamada de função** via a regra `call` (ex.: `dna_gc("ACGT")`).

### Estrutura do Parser

- Funções recursivas implementam **precedência** (de `unary` até `logic_or`).

- `consume()` garante tokens esperados e produz erros com linha/coluna.

- Nós da AST são `dataclasses` como `Literal`, `Var`, `Unary`, `Binary`, `Assign`, `Call` e statements (`VarDecl`, `PrintStmt`, `IfStmt`, `WhileStmt`, `Block`).

  

---

## 4) Ambiente (Env) e escopo


`Env` é um dicionário com **encadeamento** (`parent`). Operações:

- `define(nome, valor)` cria/atualiza no **escopo atual**.

- `get(nome)` busca recursivamente até encontrar.

- `assign(nome, valor)` atualiza no escopo **onde foi declarada** (ou erro).

Blocos `{ ... }` criam um **novo Env** filho, permitindo **sombras** de variáveis.


---

## 5) Interpretador (Interpreter)


O interpretador tem dois caminhos principais:

- `eval(expr, env)` → retorna um valor (número, string, boolean, etc.).

- `exec(stmt, env)` → executa efeitos (declara variáveis, imprime, controla fluxo).

### Regras principais

- **Aritmética/booleana:** `+ - * / %`, `== != < <= > >=`, `&& || !`.

- **Atribuição:** `a = expressão` (com verificação de alvo válido).

- **Controle:** `if/else`, `while`, e **blocos**.

- **Print:** statement `print expr;` avalia e mostra o resultado.

- **Chamada de função:** `Call(callee, args)` → avalia `callee` e `args` e chama.

  
### Funções nativas

- Cada builtin é embrulhado em um objeto chamável com aridade conhecida.

- O `Interpreter` registra esses builtins no `globals` ao iniciar.

---

## 6) Biblioteca biológica embutida

Funções disponíveis por padrão (registradas no `globals`):

### Sequências (DNA/RNA)

- `dna_gc(seq) -> float` GC% ignorando caracteres não-ATGC.

- `dna_comp(seq) -> string` complemento (A↔T, C↔G; `N` preservado).

- `dna_revcomp(seq) -> string` reverso do complemento.

- `dna_transcribe(seq) -> string` DNA→RNA (T→U).

- `dna_back_transcribe(seq) -> string` RNA→DNA (U→T).

- `dna_translate(seq) -> string` traduz DNA para proteína (código padrão, frame 0; `*` = stop, `X` = desconhecido).

- `seq_hamming(a,b) -> int` distância de Hamming (tamanhos iguais, senão erro).

- `seq_kmer_count(seq,k) -> dict` contagem de k-mers.

- `seq_motif_find(seq,motif) -> [int]` índices 0-based de ocorrências.

### Modelagem / Bioquímica

- `mm_rate(vmax, s, km) -> float` (Michaelis–Menten).

- `hill(x, k, n) -> float` função de Hill (ativação).

- `logistic(t, K, r, N0) -> float` crescimento logístico.

### Lógica biológica (sinal contínuo 0..1)

- `bio_and(a,b)`, `bio_or(a,b)`, `bio_not(a)`.


> Todas aceitam strings/números; argumentos são normalizados internamente (por exemplo, `dna_gc("atgc")` funciona).

---

### Esqueleto de hierarquia

```

codon/
├── requirements.txt
├── .gitignore
│
├── docs/                               # Documentação geral
│   ├── arquitetura.md                  # Arquitetura do compilador/intérprete
│   ├── contribuicao.md                 # Contribuidores e como contribuir
│   ├── especificacao-sintaxe.md        # Definição da linguagem
│   └── guia.md                         # Guia de compilação e uso da linguagem
│
├── src/                                # Código-fonte
│   ├── codon.py                        # Arquivo principal
│   │
│   ├── lexer/                          # Analisador léxico
│   │   ├── __init__.py
│   │   ├── lexer.py
│   │   ├── token.py
│   │   ├── scanner.py
│   │   └── afds/                       # Autômatos
│   │       ├── afd_identificadores.py
│   │       ├── afd_numeros.py
│   │       └── afd_strings.py
│   │
│   ├── parser/                         # Analisador sintático
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── ast/                        # Árvore sintática abstrata
│   │   │   ├── ast_base.py
│   │   │   ├── expressoes.py
│   │   │   └── declaracoes.py
│   │   └── ll1/                        # Implementação inicial LL(1)
│   │       ├── parser_ll1.py
│   │       └── tabela_ll1.py
│   │
│   ├── semantic/                       # Analisador semântico
│   │   ├── __init__.py
│   │   ├── analisador_semantico.py
│   │   ├── tabela_simbolos.py
│   │   └── verificador_tipos.py
│   │
│   ├── runtime/                        # Execução e funções biológicas
│   │   ├── __init__.py
│   │   ├── runtime.py
│   │   ├── biblioteca_bio.py           # Funções nativas (DNA, RNA, proteínas)
│   │   └── biblioteca_math.py          # Funções matemáticas comuns
│   │
│   └── utils/                          # Utilitários compartilhados
│       ├── __init__.py
│       ├── erros.py
│       ├── source_position.py
│       └── debug.py
│
├── tests/                              # Testes automatizados
│   ├── lexer_test/
│   │   └── test_scanner.py
│   ├── parser_test/
│   │   └── test_parser_ll1.py
│   ├── semantic_test/
│   │   └── test_tipos.py
│   ├── runtime_test/
│   │   └── test_biblioteca_bio.py
│   └── fixtures/                       # Programas de teste
│       ├── validos/
│       │   ├── hello.cn
│       │   ├── gc_content.cn
│       │   └── transcricao.cn
│       └── erros/
│           ├── erro_lexico.cn
│           ├── erro_sintatico.cn
│           └── erro_semantico.cn
│
├── tools/                              # Ferramentas de apoio
│   ├── gerador_tabelas_parsing.py
│   ├── validador_gramatica.py
│   └── formatter_codon.py
│
└── scripts/                            # Scripts de automação
    ├── run_all_tests.sh
    └── build_release.sh


```

  

---