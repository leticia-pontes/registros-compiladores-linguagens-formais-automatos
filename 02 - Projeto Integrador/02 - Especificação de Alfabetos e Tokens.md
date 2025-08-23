---
tags:
  - projeto
---
# Alfabeto da Linguagem
- Letras: a-z, A-Z
- Dígitos: 0-9
- Símbolos de pontuação e operadores: `{ } ( ) [ ] ; : , . " + - * / % = == != < <= > >= && || | ^ *\`
- Espaços em branco: espaço, tabulação e quebra de linha
- Símbolos especiais:  `'`( Diferencia átomos de carbono do açúcar (desoxirribose) nos nucleotídeos do DNA), → (Transcrição) , ← (Tradução)
# Definição de Tokens
### Identificadores
- Forma: letra ou `_` iniciais, seguido de letras, dígitos ou `_` 
- Exemplos: \_Traducao_, base_nitrogenada, Nucleotideo
- Case-sensitive (nucleotideo $\not=$ Nucleotideo)
### Literais Numéricos
- Inteiros: 0, 10, 23, 4500
- Decimais: 3.12, 0.61
- Notação científica: 1.5\^3
### Literais de Texto (strings)
- Entre aspas duplas `"Hello World!"` 
- Suporta  sequencias de escape: `\n, \t, \
### Operadores
- Aritméticos: `+, -, *, /, %, ^, *\
- Relacionais: ` ==, !=, <, >, <=, >=
- Lógicos: `&&, ||
- Especiais: `', →, ←
### Palavra-chave
- Controle de fluxo: `if, elif, else, while, for, switch, case, return, break, continue
- Estruturas: `function, procedure, class
- Tipos:`Int, Decimal, String, List, Vector, Nbase
### Comentários
- Linhas únicas: `/"
- Bloco: `""" drgxdrc """
# Estrutura Léxica Geral
- Espaços em branco: (espaço, tab, quebra de linha) separam tokens, mas não são significativos (exceto dentro de strings).
- Identificadores: não podem colidir com palavras-chave.
- Comentários: ignorados pelo compilador e não produzem tokens.
- Literais: seguem formato fixo (Strings sempre entre aspas duplas e números seguem notação decimal ou científica)
- Operadores: têm precedência definida posteriormente na gramática, mas já são tokens distintos.
- Palavras-chave: reservadas e não podem ser redefinidas.

# Exemplos Concretos de Programa
```
function transcrever(DNA){
    base_nitrogenada = "AUGC"
    RNA ← ""
    for i = 0; i < length(DNA); i++ {
        if DNA[i] == 'A' → RNA += "U"
        elif DNA[i] == 'T' → RNA += "A"
        elif DNA[i] == 'C' → RNA += "G"
        elif DNA[i] == 'G' → RNA += "C"
    }
    return RNA
}

/" Exemplo de uso "/
sequence = "ATCGTACG"
print(transcrever(sequence))

```

```
class Nucleotideo {
    base: Nbase
    posicao: Int
}

procedure ligar(n1: Nucleotideo, n2: Nucleotideo){
    if (n1.base != n2.base){
        print("Ligação permitida")
    } else {
        print("Ligação proibida")
    }
}

```
# Diário de Decisões de Design
- Case-sensitive: escolhemos por diferenciar maiúsculas/minúsculas para maior expressividade (inspirado em C++, Java).
- Identificadores: seguem convenções modernas (letra ou `_` inicial). Números não podem começar identificadores para evitar ambiguidade.
- Números científicos: adotamos `^` em vez de `e` para manter a proximidade com notação matemática.
- Strings: só com aspas duplas, evitando duplicidade com aspas simples (usadas como símbolo especial `'`).
- Comentários: usamos `/" ...` e `""" ... """` para refletir simplicidade e diferenciar de outras linguagens comuns.
- Operadores biológicos especiais: `'` diferencia elementos biológicos (átomos, açúcar), `→` (transcrição) e `←` (tradução) tornam o código semanticamente próximo da biologia.
- Palavras-chave: mantivemos um conjunto clássico de controle de fluxo, mas adicionamos tipos específicos (`Nbase`) para refletir o domínio.