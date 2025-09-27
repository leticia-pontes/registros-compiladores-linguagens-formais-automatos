
Este analisador léxico (lexer) é a entrega parcial do compilador Codon. Ele é responsável por ler um arquivo de código-fonte e produzir uma lista de tokens com seus respectivos tipos, valores e posições (linha e coluna).

## ⚙️ Como Executar

**Pré-requisitos:**

* Python 3.x instalado.

**Instruções:**

1.  **Estrutura:** O script principal do analisador (`lexer.py`) está no diretório `01 - Compilador` (diretório temporário; o compilador receberá seu próprio repositório).
2.  **Caminho do Código-Fonte:** O analisador deve ser executado a partir da linha de comando, recebendo o caminho para o arquivo de código-fonte Codon como argumento.

```bash
# Exemplo: Se o código de teste estiver no mesmo diretório do lexer, como é o caso
python lexer.py sample.cd
```

## 📋 Saída Esperada (Formato de Tabela)

A saída do programa deve ser uma tabela formatada com duas colunas principais (Token e Tipo) para cada token reconhecido.

| Token         | Tipo  |
| :------------ | :---- |
| `func`        | `KWD` |
| `calcular_cn` | `ID`  |
| ...           | ...   |
## 🚨 Tratamento de Erro Léxico

Se o analisador encontrar um caractere ou sequência que não corresponde a nenhuma regra de tokenização, ele deve interromper e emitir uma mensagem de erro detalhada, conforme o exemplo abaixo, para o token inválido `á` na linha 1, coluna 326:

```bash
ERRO LÉXICO: Caractere não reconhecido 'á' encontrado na Linha 1, Coluna 326.
```