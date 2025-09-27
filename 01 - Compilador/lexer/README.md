
Este analisador léxico (lexer) é a entrega parcial do compilador Codon. Ele é responsável por ler um arquivo de código-fonte e produzir uma lista de tokens com seus respectivos tipos, valores e posições (linha e coluna).

## ⚙️ Como Executar

**Pré-requisitos:**

* Python 3.x instalado.

**Instruções:**

1.  **Estrutura:** O script principal do analisador (`lexer.py`) está no diretório `lexer/` (está no repositório temporário; o compilador receberá seu próprio repositório).
2.  **Caminho do Código-Fonte:** O analisador deve ser executado a partir da linha de comando, recebendo o caminho para o arquivo de código-fonte Codon como argumento.
3. Os códigos na linguagem Codon (.cd) estão no mesmo diretório do analisador léxico.
4. Os arquivos são `sample.cd`, que contém uma saída válida (tabela com tokens reconhecidos e tipos) e `sample_error.cd`, com saída de erro de token não reconhecido.

Saída válida:
```bash
python lexer.py sample.cd
```

Saída inválida:
```bash
python lexer.py sample_error.cd
```

## 📋 Saída Esperada (Formato de Tabela)

A saída do programa deve ser uma tabela formatada com duas colunas principais (Token e Tipo) para cada token reconhecido, além das colunas contendo a linha e coluna onde o token foi encontrado.

| Token         | Tipo  | Lin | Col |
| :------------ | :---- | :-- | :-- |
| `func`        | `KWD` | 2   | 1   |
| `calcular_cn` | `ID`  | 2   | 6   |
| ...           | ...   | ... | ... |

## 🚨 Tratamento de Erro Léxico

Se o analisador encontrar um caractere ou sequência que não corresponde a nenhuma regra de tokenização, ele deve interromper e emitir uma mensagem de erro detalhada, conforme o exemplo abaixo, para o token inválido `á` na linha 16, coluna 1:

```bash
ERRO LÉXICO: Caractere não reconhecido 'á' encontrado na Linha 16, Coluna 1.
```