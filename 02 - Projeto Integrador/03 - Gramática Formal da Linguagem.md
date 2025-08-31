---
tags:
  - projeto
---
# Gramática Formal Desenvolvida

## Gramática G = (V, T, P, S).

#### Conjunto de Variáveis (V)

```
V = {
	Programa, BlocoDeclarações, Declaração, DeclaraçãoVariável,
	DeclaraçãoFuncao, DeclaraçãoClasse,
	BlocoComandos, BlocoComandosPrincipal, Comando, ComandoCondicional,
	ComandoLaço, ComandoAtribuição, ComandoEscrita,
	Expressão, ExpressãoLógica, ExpressãoRelacional, ExpressãoAritmética,
	Termo, Fator, ListaParametros, ListaArgumentos, Tipo
}
```
#### Conjunto de Terminais (T)

```
T = {
    let, mutable, const, print, if, then, elif, else, end,
    while, for, from, to, repeat, until, function, return,
    class, extends, int, float, string, bool,
    and, or, not,
    ==, !=, >, <, >=, <=, +, -, *, /, =,
    (, ), {, }, , , ;
}
```
#### Símbolo inicial: `S = Programa`.

> Observação: alfabetos e tokens detalhados estão na [[02 - Especificação de Alfabetos e Tokens|especificação léxica do projeto]] (tokens e regras de identificação de literais, comentários etc.).

## Principais Regras de Produção Implementadas

```
Programa → BlocoDeclarações BlocoComandosPrincipal

BlocoDeclarações → Declaração BlocoDeclarações | ε
Declaração → DeclaraçãoVariável | DeclaraçãoFuncao | DeclaraçãoClasse

DeclaraçãoVariável → Guarde Mutabilidade Tipo ValorInicial como identificador
Mutabilidade → mutável | imutável | ε
ValorInicial → literal_inteiro | literal_real | literal_texto | identificador | ε

Tipo → Inteiro | Real | Texto | Booleano | Lista | Vetor | Nbase

DeclaraçãoFuncao → Funcao Tipo identificador ( ListaParametros ) BlocoComandos Fim
ListaParametros → Tipo identificador ListaParametrosRest | ε
ListaParametrosRest → , Tipo identificador ListaParametrosRest | ε

DeclaraçãoClasse → Classe identificador BlocoClasse Fim
BlocoClasse → /* regras de membros: propriedades, métodos, construtor */

BlocoComandos → Comando BlocoComandos | ε
BlocoComandosPrincipal → Comando BlocoComandosPrincipal | ε

Comando → ComandoAtribuição | ComandoCondicional | ComandoLaço | ComandoEscrita | DeclaraçãoFuncao

ComandoAtribuição → identificador = Expressão ;
ComandoEscrita → Escreva ExpressãoLista ;
ExpressãoLista → Expressão , ExpressãoLista | Expressão

/" Condicional (forma com else opcional)
ComandoCondicional → Se ExpressãoLógica então BlocoComandos Fim
                  | Se ExpressãoLógica então BlocoComandos Senão BlocoComandos Fim

/" Laços (exemplo)
ComandoLaço → Enquanto ExpressãoLógica BlocoComandos Fim
            | ParaCada identificador de Expressão até Expressão BlocoComandos Fim

/" Expressões: projetadas para controlar precedência e associatividade
Expressão → ExpressãoLógica

ExpressãoLógica → ExpressãoLógica Ou ExpressãoConj | ExpressãoConj
ExpressãoConj → ExpressãoConj E ExpressãoRelacional | ExpressãoRelacional

ExpressãoRelacional → ExpressãoAritmética RelOp ExpressãoAritmética | ExpressãoAritmética
RelOp → == | != | > | < | >= | <=

ExpressãoAritmética → ExpressãoAritmética + Termo
                     | ExpressãoAritmética - Termo
                     | Termo
Termo → Termo * Fator | Termo / Fator | Fator
Fator → ( Expressão ) | identificador | literal_inteiro | literal_real | identificador ( ListaArgumentos )
ListaArgumentos → Expressão , ListaArgumentos | Expressão | ε
```

#### Resumo Visual Mental:
```
Programa
├─ Declarações (variáveis, funções, classes)
└─ Comandos principais
   ├─ Atribuições
   ├─ Escrita
   ├─ Condicionais
   └─ Laços

Expressões
└─ Aritmética → Relacional → Lógica
```

# Classificação na Hierarquia de Chomsky

**Tipo:** **2 - Gramática Livre de Contexto (CFG)**
#### Justificativa

* **Formato das produções:**
	
    - Todas as regras seguem a forma `A → α`, com **um único não-terminal no lado esquerdo**.
    - Essa é a exigência básica para gramáticas livres de contexto.
    
* **Necessidade de recursão e aninhamento:**
	
    - A linguagem suporta estruturas **aninhadas**, como:
        - Condicionais: `Se ... então ... Senão ... Fim`
        - Blocos de função e classe
        - Expressões com parênteses e operadores
    
    - Estruturas desse tipo **não podem ser reconhecidas por autômatos finitos** (gramáticas regulares, Tipo 3).
    
* **Definição de terminais e produções:
	
    - Os terminais e regras de produção foram cuidadosamente definidos com base nos tokens da linguagem e nas convenções do projeto.
#### Verificação

- Garantir que **todas as regras seguem a forma `A → α`**.
- Testar exemplos de programas com **estruturas aninhadas e recursivas** para confirmar que a CFG é suficiente para gerar a linguagem.
#### Limitações

- **Checagens semânticas** não são cobertas pela CFG:
    
    - Escopos de variáveis
    - Tipos e compatibilidade
    - Declaração antes do uso
    - Sobrecarga de funções
    - Consistência de mutabilidade (`mutable` vs `const`)

> Essas verificações exigem **análise semântica adicional** (tabelas de símbolos e análise sensível ao contexto).

# Exemplos de derivações
### Exemplo 1: Declaração de variável + condicional (programa simples)

**Código-fonte:**

```
let int 18 as minimum_age

if minimum_age >= 18 then
	print "Adult"
end
```

**Derivação (parcial, passo a passo):**

```
Programa 
- BlocoDeclarações BlocoComandosPrincipal
- Declaração BlocoDeclarações BlocoComandosPrincipal
- DeclaraçãoVariável BlocoDeclarações BlocoComandosPrincipal

- let Mutabilidade Tipo ValorInicial as identifier BlocoDeclarações BlocoComandosPrincipal
- let int inteiro as identifier BlocoDeclarações BlocoComandosPrincipal
- let int 18 as minimum_age BlocoDeclarações BlocoComandosPrincipal
- ... (em seguida o ComandoCondicional aparece no BlocoComandosPrincipal)

- if ExpressãoLógica then BlocoComandos end
- if ExpressãoRelacional then BlocoComandos end
- if ExpressãoAritmética RelOp ExpressãoAritmética then BlocoComandos end
- if Termo RelOp Termo then BlocoComandos end
- if identifier >= literal_inteiro then BlocoComandos end
- if minimum_age >= 18 then BlocoComandos end
- if minimum_age >= 18 then print ExpressãoLista ; end

- ... -> print "Adult" ;
```
### Exemplo 2: Função, chamada e expressão aritmética

**Código-fonte:**

```
function int add(int a, int b)
	return a + b
end

let int add(5, 3) as result
print "Result:", result
```

**Derivação (resumo):**

```
Programa
- BlocoDeclarações ...
  
- DeclaraçãoFuncao
- function Tipo identifier ( ListaParametros ) BlocoComandos end
- function int add ( Tipo identifier , Tipo identifier ) BlocoComandos end

- ... retorne ExpressãoAritmética
- return Termo + Termo
- return identifier + identifier
- return a + b
```

**Chamada da função:**

```
identifier ( ListaArgumentos )
- add ( Expressão , Expressão )
- add ( literal_inteiro , literal_inteiro )
- add(5, 3)
```

---

### Exemplo 3: Precedência (`a + b * c`)

Queremos que `a + b * c` seja interpretado como `a + (b * c)`.

**Derivação controlando precedência:**

```
ExpressãoAritmética
- ExpressãoAritmética + Termo
- Termo + Termo
- Fator + Termo
- identifier + Termo
- identifier + Termo * Fator
- identifier + Fator * Fator
- identifier + identifier * identifier
- a + b * c
```

> A multiplicação ocorre primeiro dentro de `Termo`, garantindo que `b * c` seja calculado antes da adição com `a`.

# Análise de ambiguidades potenciais e estratégias de resolução

#### Dangling else (associação do `else`)

* **Problema**: construções `if ... then ... else ... end` podem gerar ambiguidade quando aninhadas - não fica claro a que `if` cada `else` pertence.

* **Solução**: separar sentenças "casadas" (matched) de "não casadas" (unmatched). Exemplo esquemático:

```
ComandoCondicional → IfMatched | IfUnmatched
IfMatched   → if Expressão then IfMatched else IfMatched end | comando_base
IfUnmatched → if Expressão then Comando | if Expressão then IfMatched else IfUnmatched
```

* **Outra abordagem**: exigir delimitadores explícitos (`end`) ou chaves `{ }` para blocos. Nossa gramática já usa `end`, mas a regra “o `else` se associa ao `if` não pareado mais próximo” deve ser documentada.
#### Precedência e associatividade de operadores

* **Problema**: expressões aritméticas podem ser ambíguas, por exemplo `a - b - c` pode ser interpretado como `(a - b) - c` ou `a - (b - c)`.

* **Solução**: organizar a gramática em níveis (Fator < Termo < ExpressãoAritmética). Por exemplo:

```
ExpressãoAritmética → ExpressãoAritmética + Termo 
                     | ExpressãoAritmética - Termo 
                     | Termo
```

Isso garante que **a multiplicação e divisão têm prioridade sobre soma e subtração**, e que as operações do mesmo nível são avaliadas **da esquerda para a direita**.
#### Expressões lógicas e comparações encadeadas

* Comparações como `a < b < c` são consideradas **erro sintático**.  
* O usuário deve escrever `a < b and b < c` quando necessário. A regra de precedência documenta esse comportamento.

# Decisões de projeto e trade-offs (expressividade × simplicidade)

- **Por que CFG (Tipo 2)?**: Expressa aninhamentos e recursão de forma natural. É simples de especificar e permite usar ferramentas/parsers existentes (Yacc/Bison, ANTLR, etc.).

- **Limites da CFG:** checagens de contexto (escopo, tipos, declaração prévia) requerem fases semânticas extras e tabelas de símbolos.

- **Paradigma:** a linguagem mistura elementos imperativos e funcionais (funções, declaração de variáveis e comandos de controle) - isso aumenta a gramática, mas não exige regras além da CFG. Decisões sobre mutabilidade (mutável vs imutável) foram colocadas como atributos nas declarações de variável para simplificar a semântica.

# Estratégia prática para implementação do parser (próximos passos)

* Implementar analisador léxico conforme a [[02 - Especificação de Alfabetos e Tokens.md|especificação de alfabetos e tokens]] (tokenização de identificadores, literais, palavras-chave e operadores).

* Implementar parser de teste em duas alternativas: (a) Parser LL(1) com gramática transformada (eliminação de recursão à esquerda / factoring); (b) Parser LR(1) / LALR(1) usando ferramenta (Bison/ANTLR) se preferirmos manter a gramática mais natural e direta.

* Escrever uma bateria de testes com os exemplos fornecidos (declaração de variáveis, condicionais aninhados, funções e chamada de funções com argumentos). Exemplos e derivações já documentados no material do projeto.
