# Gramática Formal da *Codon*

Este documento define uma gramática compacta, legível e adequada para análise sintática da *Codon*. Contém a definição formal (4-tupla), uma especificação em EBNF (útil para implementação) e uma listagem equivalente em BNF para referência.

---

## 1. Gramática como 4-tupla

G = (V, Σ, P, S)

* **V** (não-terminais):

  ```text
  { Programa, DeclTopo, Decl, DeclConst, DeclVar, Tipo,
    DeclMetodo, ParamsFormOpt, ParamsForm, ParamsFormSeg,
    Bloco, SeqComando, Comando, Designador, SufixoDesignador,
    ParamsAtivosOpt, ParamsAtivos, ParamsAtivosSeg,
    Condicao, OpRel,
    Expressao, ExpressaoSeg, Termo, TermoSeg, Fator,
    OpSoma, OpMult,
    ConstLit, Numero, ConstChar, ConstBool,
    Ident }
  ```

* **Σ** (terminais): palavras-chave, pontuação, operadores e classes léxicas

  ```text
  { program, const, var, void, if, else, while, return, read, print,
    new, true, false,
    Ident, Numero, ConstChar,
    ; , , , ( , ) , { , } , [ , ] , = , == , != , > , >= , < , <= ,
    + , - , * , / , % , ++ , -- , . , -> , ... }
  ```

* **S** (símbolo inicial): `Programa`

* **P** (produções): ver seções abaixo.

---

## 2. Notas e objetivos de design

* A gramática foi projetada para ser **amigável a análise preditiva / recursiva-descendente** (sem recursão à esquerda e com ambiguidade mínima).
* **Regra do maior casamento léxico** (por exemplo, `...` antes de `..` antes de `.`) é tratada no léxico.
* As palavras-chave são tokens separados do identificador. O parser recebe tokens como `IDENT`, `NUMBER`, `STRING` etc.
* A gramática suporta: declarações globais (const/var), métodos (`void`), listas de parâmetros, variáveis locais, estruturas de controle e expressões (binárias e unárias), criação de arrays e chamadas de métodos.

---

## 3. Gramática em EBNF

```ebnf
Programa        = "program" Ident "{" DeclTopo "}" .

DeclTopo        = { Decl | DeclMetodo } .

Decl            = DeclConst | DeclVar .

DeclConst       = "const" Tipo Ident "=" ConstLit ";" .

DeclVar         = "var" Tipo Ident { "," Ident } ";" .

Tipo            = Ident .

DeclMetodo      = "void" Ident "(" ParamsFormOpt ")"
                  { DeclVar }
                  Bloco .

ParamsFormOpt   = ParamsForm | ε .

ParamsForm      = Tipo Ident { "," Tipo Ident } .

Bloco           = "{" SeqComando "}" .

SeqComando      = { Comando } .

Comando         = ComandoDesignador
                | ComandoIf
                | ComandoWhile
                | ComandoReturn
                | ComandoRead
                | ComandoPrint
                | Bloco
                | ";"  /* comando vazio */ .

ComandoDesignador = Designador ( OpAtrib Expressao 
                        | "(" ParamsAtivosOpt ")"   /* chamada */
                        | "++" | "--" ) ";" .

ComandoIf       = "if" "(" Condicao ")" Comando [ "else" Comando ] .

ComandoWhile    = "while" "(" Condicao ")" Comando .

ComandoReturn   = "return" [ Expressao ] ";" .

ComandoRead     = "read" "(" Designador ")" ";" .

ComandoPrint    = "print" "(" Expressao [ "," Numero ] ")" ";" .

Designador      = Ident { "." Ident | "[" Expressao "]" } .

ParamsAtivosOpt = ParamsAtivos | ε .

ParamsAtivos    = Expressao { "," Expressao } .

Condicao        = Expressao OpRel Expressao .

OpRel           = "==" | "!=" | ">" | ">=" | "<" | "<=" .

Expressao       = [ "-" ] Termo { OpSoma Termo } .

OpSoma          = "+" | "-" .

Termo           = Fator { OpMult Fator } .

OpMult          = "*" | "/" | "%" .

Fator           = Designador
                | Designador "(" ParamsAtivosOpt ")"  /* chamada de função */
                | Numero
                | ConstChar
                | ConstBool
                | "new" Tipo "[" Expressao "]"
                | "(" Expressao ")" .

OpAtrib         = "=" .

ConstLit        = Numero | ConstChar | ConstBool .

Ident           = /* token IDENT produzido pelo léxico */ .
Numero          = /* token NUMBER produzido pelo léxico */ .
ConstChar       = /* token CHAR_CONST produzido pelo léxico */ .
ConstBool       = "true" | "false" .
```

---

## 4. Gramática em BNF (equivalente, útil para provas formais)

```bnf
<Programa>        ::= "program" <Ident> "{" <DeclTopo> "}"

<DeclTopo>        ::= <Decl> <DeclTopo>
                   | <DeclMetodo> <DeclTopo>
                   | ε

<Decl>            ::= <DeclConst>
                   | <DeclVar>

<DeclConst>       ::= "const" <Tipo> <Ident> "=" <ConstLit> ";"

<DeclVar>         ::= "var" <Tipo> <Ident> <DeclVarSeg> ";"

<DeclVarSeg>      ::= "," <Ident> <DeclVarSeg>
                   | ε

<Tipo>            ::= <Ident>

<DeclMetodo>      ::= "void" <Ident> "(" <ParamsFormOpt> ")" <SeqDeclVar> <Bloco>

<ParamsFormOpt>   ::= <ParamsForm>
                   | ε

<ParamsForm>      ::= <Tipo> <Ident> <ParamsFormSeg>

<ParamsFormSeg>   ::= "," <Tipo> <Ident> <ParamsFormSeg>
                   | ε

<SeqDeclVar>      ::= <DeclVar> <SeqDeclVar>
                   | ε

<Bloco>           ::= "{" <SeqComando> "}"

<SeqComando>      ::= <Comando> <SeqComando>
                   | ε

<Comando>         ::= <ComandoDesignador>
                   | "if" "(" <Condicao> ")" <Comando> <ParteElse>
                   | "while" "(" <Condicao> ")" <Comando>
                   | "return" <ExpressaoOpt> ";"
                   | "read" "(" <Designador> ")" ";"
                   | "print" "(" <Expressao> <PrintOpt> ")" ";"
                   | <Bloco>
                   | ";"

<ParteElse>       ::= "else" <Comando>
                   | ε

<ExpressaoOpt>    ::= <Expressao>
                   | ε

<PrintOpt>        ::= "," <Numero>
                   | ε

<ComandoDesignador> ::= <Designador> "=" <Expressao> ";"
                   | <Designador> "(" <ParamsAtivosOpt> ")" ";"
                   | <Designador> "++" ";"
                   | <Designador> "--" ";"

<Designador>      ::= <Ident> <SufixoDesignador>

<SufixoDesignador>::= "." <Ident> <SufixoDesignador>
                   | "[" <Expressao> "]" <SufixoDesignador>
                   | ε

<ParamsAtivosOpt> ::= <ParamsAtivos>
                   | ε

<ParamsAtivos>    ::= <Expressao> <ParamsAtivosSeg>

<ParamsAtivosSeg> ::= "," <Expressao> <ParamsAtivosSeg>
                   | ε

<Condicao>        ::= <Expressao> <OpRel> <Expressao>

<OpRel>           ::= "==" | "!=" | ">" | ">=" | "<" | "<="

<Expressao>       ::= <Termo> <ExpressaoSeg>
                   | "-" <Termo> <ExpressaoSeg>

<ExpressaoSeg>    ::= <OpSoma> <Termo> <ExpressaoSeg>
                   | ε

<OpSoma>          ::= "+" | "-"

<Termo>           ::= <Fator> <TermoSeg>

<TermoSeg>        ::= <OpMult> <Fator> <TermoSeg>
                   | ε

<OpMult>          ::= "*" | "/" | "%"

<Fator>           ::= <Designador>
                   | <Designador> "(" <ParamsAtivosOpt> ")"
                   | <Numero>
                   | <ConstChar>
                   | <ConstBool>
                   | "new" <Tipo> "[" <Expressao> "]"
                   | "(" <Expressao> ")"

<ConstLit>        ::= <Numero> | <ConstChar> | <ConstBool>
```

---

## 5. Extensões e notas de implementação

* **Tipos de array**: atualmente `Tipo` é um identificador simples. Para suportar `int[]`, adicione: `Tipo = Ident [ "[" "]" ]`.
* **Suporte a classes/objetos**: pode-se adicionar produções com `class` e construtores, inspiradas na MicroJava.
* **Precedência de operadores**: já é garantida pela separação de `Expressao`, `Termo` e `Fator`.
* **Ambiguidade e lookahead**: a gramática é LL(1) em grande parte; chamadas de método e designadores são diferenciados pelo token seguinte (`(` ou outros operadores).