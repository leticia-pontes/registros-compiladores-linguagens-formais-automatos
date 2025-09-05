# Especificação Léxica (com Expressões Regulares)

> Semana 4 — Refinar a especificação léxica usando regex e preparar a implementação do analisador léxico.

Este documento define **todos os tipos de tokens** da linguagem (projeto: linguagem especializada em biologia), com **expressões regulares precisas**, **regras de precedência/empate**, **estratégias de tratamento de erro léxico** e **rascunhos de mensagens de erro**.

---

## Convenções

- **Dialeto de regex**: PCRE/RE2 (sintaxe comum). Onde usamos classes Unicode, adotamos `\p{…}`. Em geradores como ANTLR/Flex, adapte as classes/construções equivalentes.
- **Flags**: quando relevantes, indicamos ao lado (ex.: `(?i)` e `(?-i)`). O analisador não deve depender de flags globais.
- **Maximal‑munch**: sempre preferir **o token mais longo**. Em empates de mesmo comprimento, aplicar **ordem de precedência** abaixo.
- **Normalização Unicode**: Não utilizaremos a principio.
- **Separadores com `_`** em literais numéricos são permitidos, mas **não podem**: aparecer no início/fim; aparecer duplicados; rodear o prefixo da base.

---

## 1. Espaços em branco e quebras de linha (ignorados)

| Nome      | Regex        | Observações              |
| --------- | ------------ | ------------------------ |
| `WS`      | `[\t\f\r ]+` | Ignorar.                 |
| `NEWLINE` | `\n`         | Incrementa linha/coluna. |

---

## 2. Comentários

| Token           | Regex       | Mantém?  | Observações                                       |
| --------------- | ----------- | -------- | ------------------------------------------------- |
| `LINE_COMMENT`  | `/"`        | Não      | Precedência **antes** de operador `/`.            |
| `BLOCK_COMMENT` | `""" """`   | Não      | **Não aninhado**; erro se não fechar.             |

---

## 3. Identificadores e Palavras‑chave

### 3.1 Classes Unicode
- `ID_START = [_\p{XID_Start}]`
- `ID_CONT = [_\p{XID_Continue}]`

### 3.2 Identificadores
- **Regex**: `ID = {ID_START}{ID_CONT}*`
- **Exemplos válidos**: `gene`, `_align`, `Dados_σ3`.
- **Proibido**: `\u0000`–`\u001F`, espaços, pontuação fora de `_`.

### 3.3 Palavras‑chave (ASCII, case‑sensitive)

```
{ and, or, not, if, else, for, while, return,
break, continue, func, var, const, import, from, as,
struct, enum, match, case, default, true, false, null,
pub, extern, use }
```

- **Regex**: `\b(?:and|or|not|if|else|for|while|return|break|continue|func|var|const|import|from|as|struct|enum|match|case|default|true|false|null|pub|extern|use)\b`
- **Resolução com `ID`**: se o lexeme casar com `KWD`, produzir `KWD`; caso contrário, `ID`.

---
## 5. Operadores e Delimitadores

> **Regra geral**: sempre casar **os mais longos primeiro**.

### 5.1 Delimitadores
```
LPAREN     => \(
RPAREN     => \)
LBRACE     => \{
RBRACE     => \}
LBRACK     => \[
RBRACK     => \]
COMMA      => ,
SEMI       => ;
COLON      => :
AT         => @
ARROW      => ->
FATARROW   => =>
DOT3       => \.{3}
DOT2       => \.{2}
DOT        => \.
```

### 5.2 Operadores
```
PLUS       => \+
MINUS      => -
STAR       => \*
SLASH      => /
PERCENT    => %
CARET      => \^
AMP        => &
BAR        => \|
BANG       => !
TILDE      => ~
ASSIGN     => =

// Compostos (ordem prioritária)
PLUS_EQ    => \+=
MINUS_EQ   => -=
STAR_EQ    => \*=
SLASH_EQ   => /=
PERC_EQ    => %=
AMP_EQ     => &=
BAR_EQ     => \|=
CARET_EQ   => \^=

// Comparação/lógicos
EQ         => ==
NE         => !=
LE         => <=
GE         => >=
LT         => <
GT         => >
AND_AND    => &&
OR_OR      => \|\|

// Shift
SHL        => <<
SHR        => >>
SHL_EQ     => <<=
SHR_EQ     => >>=
```

**Observações de desambiguação**:
- Tentar `DOT3` → `DOT2` → `DOT`.
- `LINE_COMMENT (/"…)` tem precedência sobre `SLASH` e `SLASH_EQ`.

---

## 6. Regras de precedência e ambiguidades

1. **Comentários** (linha → bloco) e **espaços** (descartados).
2. **Delimitadores e operadores compostos** (mais longos primeiro): `...`, `..`, `>>=`, `<<=` etc.
3. **Strings**: `"""…"""` → `b"…"` → `r"…"` → `"…"` → `'(char)'`.
4. **Literais biológicos**: `dna"…"`/`rna"…"`/`prot"…"`.
5. **Números**: `0x/0o/0b` → `float` → `decimal`.
6. **Palavras‑chave** vs **identificadores**: se casar `KWD`, é `KWD`; senão `ID`.

**Casos típicos**:
- `1..10` → `INT(1)` + `DOT2` + `INT(10)`.
- `1...10` → `INT(1)` + `DOT3` + `INT(10)`.
- `a---b` → `ID(a)` + `MINUS_MINUS`? **Não temos `--`**; então `MINUS` + `MINUS` + `ID(b)`.
- `/*` sem `*/` até EOF → erro léxico (§7.2).

---

## 7. Tratamento de erros léxicos

### 7.1 Estratégia geral
- **Pânico leve** por categoria:
  - **Caractere inválido**: emitir `LEX001` no ponto e **consumir 1 codepoint**, continuar.
  - **String/char não terminada**: emitir `LEX002/LEX003`, **consumir até fim de linha** (string) ou **até próximo `'`** (char) ou EOF.
  - **Comentário de bloco não terminado**: `LEX004`, consumir até EOF.
  - **Dígito inválido para base**: `LEX005`, consumir até separador não alfanumérico.
  - **Sequência biológica inválida**: `LEX006`, consumir até aspas finais ou separador; tentar continuar.
- **Recuperação**: heurísticas de sincronização em `\n`, `;`, `)`, `]`, `}`.

### 7.2 Casos específicos
- **Escape inválido em string/char**: `LEX007`, mantém token como string, mas marca valor como inválido para parser, ou **quebra o token** (decisão: **sugestão** — manter e sinalizar).
- **Underscore mal posicionado** em números: `LEX008`, remover underscores e continuar, mas reportar.
- **Unicode não normalizado** em identificador**:** `LEX009` (aviso), sugerir forma NFC.
- **Caractere de controle** em string (sem escape): `LEX010`, sugerir `\xHH`.

---

## 8. Mensagens de erro (rascunho)

> Mensagens devem incluir **código**, **resumo**, **posição** e **dica**. Use trechos com marcador `^`.

- **Ex: Caractere inválido**
  - _"Caractere não reconhecido '…' (U+XXXX)."_
  - Dica: _"Remova ou escape o caractere"_.
    ```
    a = 1 § 2
          ^ caractere inválido (U+00A7)
    ```

> **Formato sugerido**: `arquivo:linha:coluna: severidade código: mensagem`.

---

## 9. Tabela de tokens (para implementação)

> Ordem importa: já na sequência recomendada para o gerador léxico.

1. **Comentários/espaços**: `DOC_COMMENT`, `LINE_COMMENT`, `BLOCK_COMMENT`, `WS`, `NEWLINE` (ignorados conforme política).
2. **Delimitadores compostos**: `DOT3`, `DOT2`, `FATARROW`, `ARROW`.
3. **Operadores compostos**: `SHR_EQ`, `SHL_EQ`, `PLUS_EQ`, `MINUS_EQ`, `STAR_EQ`, `SLASH_EQ`, `PERC_EQ`, `AMP_EQ`, `BAR_EQ`, `CARET_EQ`, `EQ`, `NE`, `LE`, `GE`, `AND_AND`, `OR_OR`, `SHR`, `SHL`.
4. **Delimitadores simples**: parênteses, colchetes, chaves, `, ; : @ .`.
5. **Strings**: `TRIPLE_STRING`, `BYTE_STRING`, `RAW_STRING`, `STRING` e `CHAR`.
6. **Literais biológicos**: `DNA_LIT`, `RNA_LIT`, `PROT_LIT`.
7. **Números**: `HEX_INT`, `OCT_INT`, `BIN_INT`, `FLOAT_EXP`, `FLOAT`, `DEC_INT`, `INF_NAN`.
8. **Palavras‑chave**: `KWD` (lista).
9. **Identificadores**: `ID`.

---

## 12. Exemplos rápidos

```txt
// comentários
func gc_content(seq dna"ACGTNN") -> float {
  let g = count(seq, 'G')
  let c = count(seq, 'C')
  return (g + c) / len(seq)
}

x = 1_000..2_000
r = 3.14e-2
name = "β‑actin"
pattern = r"^ATG(?:...)*?(?:TAA|TAG|TGA)$"
```


