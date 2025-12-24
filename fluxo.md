# 📌 Fluxo do Extrator de RQs

```mermaid
flowchart TD
    A[Início do Script] --> B[Ler RQ.xlsx]
    B --> C[Ler resultado_rq.csv]
    C --> D[Identificar RQs já processadas]
    D --> E[Filtrar RQs pendentes]
    E -->|Nenhuma pendente| F[Fim]
    E -->|Existem pendentes| G[Abrir Sistema (Selenium)]
    G --> H[Pesquisar RQ]
    H --> I[Extrair Dados]
    I --> J[Salvar no CSV (append)]
    J --> K[Voltar para lista]
    K --> E
