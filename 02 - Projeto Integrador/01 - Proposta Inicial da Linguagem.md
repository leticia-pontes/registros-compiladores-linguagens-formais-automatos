---
tags:
  - projeto
---
**Nome provisório da linguagem:**

> _Codon_

**Equipe:**

1. Laura Yumi Osawa – Líder de Projeto / Facilitador
    
2. Letícia Alves de Pontes – Responsável Técnico / Arquiteto de Linguagem
    
3. Cauã dos Santos Pereira – Pesquisador (Paradigmas e Inspirações)
    
4. José Victor Santos Tranquilino de Souza – Documentador / Gestor do Diário
    
5. Emerson Caique Alexandre Felizardo – Designer de Sintaxe / UX
    
6. Hugo Pacheco Medeiros – Tester / Avaliador
    

---

**1. Visão Geral da Linguagem**

> (Explique em 3 a 5 frases a proposta da linguagem: para que serve, que problema resolve, qual é o objetivo central.)
> A linguagem Codon integra programação e biologia genética, permitindo automatizar cálculos de probabilidade no contexto genético. Com ela, biólogos podem criar scripts de análise e simulação usando termos da área, sem precisar lidar com a sintaxe genérica de linguagens de programação tradicionais.

---

**2. Objetivos Principais**

- Permitir que biólogos escrevam scripts de análise ou simulação usando termos da área, sem precisar lidar com sintaxe genérica de programação.
    
- Objetivo 2
    
- Objetivo 3
    

---

**3. Público-Alvo**

>O público-alvo dessa linguagem será formado principalmente por profissionais e estudantes da área de biociências, com idades variando entre 20 e 50 anos, abrangendo desde graduandos curiosos até pesquisadores experientes em genética, biotecnologia e bioinformática. A maioria terá pouca ou nenhuma experiência prévia em programação tradicional, mas possuirá sólidos conhecimentos conceituais sobre biologia molecular, manipulação de sequências e análise de dados genômicos. Esses usuários precisam de ferramentas que traduzam termos e operações biológicas diretamente para código, evitando barreiras técnicas de linguagens genéricas como Python ou C++. Suas necessidades incluem processar grandes volumes de dados genéticos, realizar simulações de mutações, identificar padrões em sequências e integrar análises com bancos de dados científicos, tudo de forma rápida, intuitiva e reprodutível, sem se perder em detalhes de implementação de baixo nível.

---

**4. Principais Características Desejadas**

- Paradigma(s) adotado(s): Declarativo e imperativo.
    
- Nível de abstração: Alta
    
- Facilidade de uso ou poder técnico? Priorizar a facilidade de uso
    
- Suporte a integração com outras ferramentas? Sim, suportar importar/exportar dados estatísticos
    

---

**5. Motivação / Justificativa**

> O mundo precisa dessa linguagem porque a biologia, especialmente a genética, está cada vez mais dependente de análises computacionais, mas as ferramentas existentes ainda exigem conhecimentos técnicos que muitos biólogos e estudantes não possuem. Essa linguagem se diferencia por falar a língua do biólogo, usando comandos e estruturas diretamente inspirados na nomenclatura genética, reduzindo a curva de aprendizado e permitindo que qualquer pessoa com conhecimento da área possa realizar análises, simulações e visualizações de dados genéticos de forma rápida e intuitiva, sem precisar se tornar um programador profissional. Ao oferecer essa acessibilidade, ela abre novos caminhos para acelerar e ampliar o avanço das pesquisas na área da biologia.

---

**6. Cenários de Uso**

- Exemplo 1: Em salas de aulas de biologia genética pode-se utilizar a linguagem para que, os alunos escrevam comandos simples para visualizar como pequenas mudanças alteram proteínas, facilitando a compreensão de conceitos como mutação, transcrição e tradução.
    
- Exemplo 2: No ambiente de pesquisas ao receber algum dado de uma nova sequência genômica rapidamente é possível escrever um script simples para alinhar a sequência com um banco de dados local, identificar mutações e gerar um relatório com esses dados.
    
- Exemplo 3: Um desenvolvedor educacional cria um jogo no qual o jogador “conserta” sequências de DNA/RNA defeituosas para restaurar a função de genes. A lógica genética e as mutações são programadas diretamente na linguagem, permitindo fácil ajuste e expansão do conteúdo sem mexer na base do jogo.
    

---

**7. Inspirações**

> Liste linguagens ou ferramentas que influenciaram o projeto (ex.: Python, Scratch, R, etc.) e o que pretendem aproveitar ou evitar.
> - Python com a biblioteca Biopython → Manter a simplicidade e clareza da sintaxe da linguagem e funções voltadas a analise de dados biologicos da biblioteca. Porém evitar a verbosidade e a necessidade de importar múltiplos pacotes para tarefas simples.
> - R -> Manter a integração com calculos de estatística, mas evitar a inconsistência sintática e a dificuldade para iniciantes.