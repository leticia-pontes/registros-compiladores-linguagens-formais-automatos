### Últimos Acessos
```dataview
table file.name as "Arquivo", file.mtime as "Última Modificação"
from ""
where file.name != "Mapa da Disciplina"
sort file.mtime desc
limit 15
```

### 01 - Conhecimentos Teóricos
```dataview
table file.name as "Arquivo"
from "01 - Conhecimentos Teóricos"
sort file.name asc
```

### 02 - Projeto Integrador
```dataview
table file.name as "Arquivo"
from "02 - Projeto Integrador"
sort file.name asc
```

### 03 - Diário de Bordo
```dataview
table file.name as "Arquivo"
from "03 - Diário de Bordo"
sort file.name asc
```

### 04 - Materiais de Apoio
```dataview
table file.name as "Arquivo"
from "04 - Materiais de Apoio"
sort file.name asc
```
