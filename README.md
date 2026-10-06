# Azure FinOps Lab

Projeto educacional desenvolvido em Python para análise de custos de recursos em Cloud e identificação de oportunidades de otimização.

## Objetivo

Simular uma solução FinOps capaz de analisar custos, identificar possíveis desperdícios e estimar oportunidades de economia em um ambiente Cloud.

## Funcionalidades

- Cálculo do custo mensal total
- Análise de custos por serviço
- Análise de custos por ambiente
- Identificação de possíveis recursos ociosos
- Identificação de possíveis oportunidades de rightsizing
- Estimativa de economia mensal
- Estimativa de economia anual
- Geração de relatório em JSON
- Testes automatizados com Pytest

## Como funciona

```text
Dados de custos
      ↓
Arquivo CSV
      ↓
Python
      ↓
Regras FinOps
      ↓
Análise dos recursos
      ↓
Recomendações
      ↓
Relatório JSON
Tecnologias
Python
CSV
JSON
Pytest
Git
GitHub
Estrutura
azure-finops-lab/
│
├── data/
│   └── costs.csv
│
├── reports/
│   └── analysis.json
│
├── src/
│   ├── main.py
│   └── finops.py
│
├── tests/
│   └── test_finops.py
│
└── README.md
Exemplo de análise

Com os dados simulados atuais:

Custo mensal: R$ 8.900,00
Economia potencial mensal: R$ 1.400,00
Economia potencial anual: R$ 16.800,00
Recursos analisados: 6
Recomendações encontradas: 2
Importante

Este projeto utiliza dados simulados e não possui conexão com ambientes corporativos ou recursos reais do Azure.

As estimativas de economia são regras educacionais utilizadas para demonstrar conceitos de FinOps e não representam necessariamente preços ou recomendações oficiais da Azure.

Próximos passos
Melhorar as regras de análise FinOps
Adicionar classificação de risco e prioridade
Criar análise histórica de custos
Implementar detecção de anomalias
Criar dashboard
Automatizar a execução do projeto
Evoluir a arquitetura para permitir futura integração com fontes reais de dados Cloud, em ambientes autorizados
Resultado

O projeto demonstra conhecimentos de:

FinOps
Cloud Computing
Python
Análise de dados
Automação
Testes automatizados
Engenharia de software