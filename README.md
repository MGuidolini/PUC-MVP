
## README do Projeto

Este README oferece uma visão geral do projeto, incluindo seus objetivos, a metodologia utilizada e os principais resultados obtidos. Ele serve como um guia rápido para entender e replicar a análise realizada neste notebook.

### 1. Visão Geral do Projeto

*   **Título:** MVP Análise de Dados e Boas Práticas - Classificação Calórica de Alimentos
*   **Autor:** Marcos Aurélio Guidolini
*   **Matrícula:** 4052025002325
*   **Data:** `calorie_dataset.csv `

Este projeto foca na análise e classificação calórica de alimentos com base em seus macronutrientes. O objetivo principal é identificar a ingestão calórica por refeição e classificá-la em níveis (**Baixa, Média, Alta**), além de explorar padrões de consumo. Ele aborda a importância do balanceamento de dados e do pré-processamento para a construção de modelos de Machine Learning robustos.

### 2. Fonte de Dados

*   **Dataset Original:** [Calorias](https://raw.githubusercontent.com/MGuidolini/PUC-MVP/refs/heads/main/calorie_dataset.csv)
*   **Descrição:** Um conjunto de dados sintético, mas realista, de nutrição alimentar contendo informações sobre macronutrientes (**Carboidrato, Proteína, Gordura, Fibra, Açúcar**), calorias totais e uma classe calórica rotulada (**low, medium, high**).
*   **Tamanho:** 5.000 instâncias, 7 atributos iniciais (**6 numéricos, 1 categórico**).

### 3. Problema e Objetivos

*   **Tipo de Problema:** Classificação Supervisionada.
*   **Problema:** Prever a classe calórica (**Baixa, Média, Alta**) de uma refeição com base nos macronutrientes e outras características.
*   **Objetivo Principal:** Identificar a ingestão calórica (**Kcal**) por refeição e classificá-la em **Alto, Médio ou Baixo**.

### 4. Hipóteses do Projeto

1.  **Quem ingere mais calorias:** Analisar qual dos três grupos de Gênero (**Masculino, Feminino, Outros**) ingere mais calorias.
2.  **Consumo calórico por Estado:** Identificar em quais Estados Brasileiros se consome mais calorias.
3.  **Macronutrientes mais consumidos:** Determinar quais macronutrientes (**Carboidrato, Proteína, Gordura, Fibra, Açúcar**) são mais consumidos pelos três Gêneros.
4.  **Classificação calórica por Gênero:** Verificar se é possível identificar em que nível de calorias os indivíduos estão divididos, considerando o Gênero e os alimentos ingeridos.
5.  **Faixa etária com maior consumo de Proteína:** Identificar qual faixa etária consome mais Proteína.

### 5. Metodologia

O projeto seguiu as seguintes etapas:

*   **Importação de Bibliotecas:** Carregamento das bibliotecas necessárias (**pandas, numpy, matplotlib, seaborn, scikit-learn, imblearn**).
*   **Carga de Dados:** Leitura do `calorie_dataset.csv `.
*   **Análise Exploratória de Dados (EDA):**
    *   Verificação do tipo e total de instâncias.
    *   Identificação e tratamento de valores nulos (**não encontrados neste dataset**).
    *   Análise da distribuição inicial das classes de calorias, revelando desbalanceamento.
    *   Balanceamento das classes usando *RandomOverSampler*.
    *   Estatísticas descritivas (**média, desvio padrão**) antes e depois do balanceamento.
    *   Visualização das distribuições (**histogramas e boxplots**) por classe de caloria.
    *   Cálculo e visualização de matrizes de correlação para identificar relações entre macronutrientes e calorias.
*   **Pré-Processamento de Dados:**
    *   **Correção de Dados:** Identificação e correção de um erro no cálculo da coluna '*Calorias/Kcal*' original, criando a coluna '*Calorias_Totais/Kcal*' com base nas regras de cálculo fornecidas (*Carboidrato:* **4 kcal/g**, *Proteína:* **4 kcal/g**, *Gordura:* **9 kcal/g**, *Fibra:* **2 kcal/g**, *Açúcar:* **4 kcal/g**).
    *   **Feature Engineering:** Criação de novos atributos sintéticos (**'UF', 'Idade', 'Sexo', 'Refeicao'**) e a reclassificação do '*Nivel_Calorias*' com base na nova '*Calorias_Totais/Kcal*'.
    *   **Balanceamento de Classes (Nível de Calorias):** Novo balanceamento do dataset com base na coluna '*Nivel_Calorias*' para garantir distribuição equitativa.
    *   **Divisão Treino/Teste:** Separação dos dados em conjuntos de treinamento e teste.
    *   **Normalização:** Escalonamento dos dados numéricos para um intervalo fixo (**MinMaxScaler**).
    *   **Padronização:** Transformação dos dados para ter média 0 e desvio padrão 1 (**StandardScaler**).
*   **Respostas às Hipóteses:** Análise detalhada de cada hipótese com visualizações (**Plotly e Matplotlib**) e interpretação dos resultados.

### 6. Resultados e Conclusões

As análises realizadas confirmaram as seguintes conclusões: 
>**OBS:** **Os resultados das hipóteses podem variar em novas execuções devido à geração de dados aleatórios**

*   **Hipótese 1:** O grupo **Feminino** foi identificado como o que mais ingere calorias totais.
*   **Hipótese 2:** O estado de **Alagoas (AL)** destacou-se com o maior consumo total de calorias.
*   **Hipótese 3:** A **Proteína** foi o macronutriente mais consumido pelos três gêneros.
*   **Hipótese 4:** Foi possível identificar a distribuição dos níveis de calorias (**Baixa, Média, Alta**) entre os gêneros, mostrando padrões distintos.
*   **Hipótese 5:** A faixa etária em torno dos **39 anos** apresentou o maior consumo de **Proteínas**.

O projeto demonstrou a importância de um pré-processamento cuidadoso e do balanceamento de classes para garantir a confiabilidade das análises. A correção de inconsistências nos dados e a criação de novas features enriqueceram o dataset, tornando-o uma base sólida para futuras modelagens preditivas na área de nutrição e saúde.
