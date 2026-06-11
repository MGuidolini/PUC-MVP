# MVP Análise de Dados e Boas Práticas - Classificação Calórica de Alimentos

## Visão Geral do Projeto

Este projeto detalha a análise e o pré-processamento de um conjunto de dados de alimentos com o objetivo de classificar a ingestão calórica em três níveis: **'Baixa'**, **'Média'** e **'Alta'**. A análise segue uma metodologia robusta, abordando desde a exploração inicial dos dados até o balanceamento de classes e a engenharia de novas características, culminando na validação de hipóteses cruciais para o entendimento dos padrões de consumo nutricional.

## Descrição do Problema

O problema central é a classificação supervisionada da ingestão calórica baseada em informações de macronutrientes (Carboidrato, Proteína, Gordura, Fibra e Açúcar) e calorias totais (Kcal). O objetivo é prever a classe de calorias ('Baixa', 'Média' ou 'Alta') para indivíduos de diferentes gêneros (Masculino, Feminino, Outros).

### Definições de Classes Calóricas:
*   **Baixa:** Menor que 400 Kcal
*   **Média:** Entre 400 e 699 Kcal
*   **Alta:** Maior que 700 Kcal

## Hipóteses do Problema

As seguintes hipóteses foram formuladas para guiar a análise:

1.  **Gênero com maior ingestão calórica:** Qual dos três grupos de gênero (M- Masculino, F- Feminino ou O- Outros) ingere mais calorias - Kcal?
2.  **Estado Brasileiro com maior consumo calórico:** Em que Estados Brasileiros se consome mais Calorias - Kcal?
3.  **Macronutriente mais consumido por gênero:** Quais Macronutrientes (Carboidrato, Proteína, Gordura, Fibra, Açúcar) são mais consumidos pelos três Gêneros?
4.  **Identificação do nível calórico por gênero:** Dados o Gênero do indivíduo e os alimentos ingeridos, é possível identificar em que nível de Calorias eles estão divididos?
5.  **Faixa etária com maior consumo de Proteína:** Que faixa etárias se consome mais Proteína?

## Dados

O dataset original é sintético, mas realista, contendo 5.000 amostras com nove atributos, incluindo macronutrientes, calorias totais e a classe calórica. Durante o pré-processamento, foram adicionadas colunas sintéticas para 'UF', 'Idade', 'Sexo' e 'Refeição' para enriquecer a análise e testar as hipóteses.

### Atributos Originais:
*   `Carboidrato/g`: Quantidade em gramas.
*   `Proteina/g`: Quantidade em gramas.
*   `Gordura/g`: Quantidade em gramas.
*   `Fibra/g`: Quantidade em gramas.
*   `Acucar/g`: Quantidade em gramas.
*   `Calorias/Kcal`: Calorias totais (Kcal).
*   `Classe_de_Calorias`: Categoria calórica ('low', 'medium', 'high').

### Atributos Adicionais (Sintéticos):
*   `UF`: Unidade Federativa (ex: 'SP', 'RJ', 'MG').
*   `Idade`: Idade do indivíduo (18 a 81 anos).
*   `Sexo`: Gênero ('F' - Feminino, 'M' - Masculino, 'O' - Outros).
*   `Refeicao`: Tipo de refeição ('CAFÉ DA MANHÃ', 'ALMOÇO', 'JANTAR', 'LANCHE').
*   `Calorias_Totais/Kcal`: **Recalculado** com base nas regras fornecidas (4 kcal/g para Carboidrato/Proteína/Açúcar, 9 kcal/g para Gordura, 2 kcal/g para Fibra).
*   `Nivel_Calorias`: **Recategorizado** ('BAIXA', 'MEDIA', 'ALTA') com base em `Calorias_Totais/Kcal`.

## Metodologia

1.  **Importação de Bibliotecas e Carga de Dados:** Carregamento do dataset e importação de `pandas`, `numpy`, `matplotlib`, `seaborn`, `sklearn`, `imblearn` e `plotly`.
2.  **Análise Exploratória de Dados (EDA):**
    *   Verificação de valores nulos.
    *   Análise da distribuição inicial das classes calóricas, identificando um desbalanceamento.
    *   Cálculo e visualização de estatísticas descritivas (média, desvio padrão) para o dataset desbalanceado e balanceado.
    *   Geração de histogramas para visualizar a distribuição de calorias por classe (antes e depois do balanceamento).
    *   Criação de boxplots para analisar a dispersão dos macronutrientes e calorias por classe.
3.  **Correção de Inconsistência:** Identificação e correção da coluna `Calorias/Kcal` original, que não seguia as regras de cálculo. Criação da nova coluna `Calorias_Totais/Kcal` com os valores corretos.
4.  **Feature Engineering:** Inclusão de novos atributos sintéticos (`UF`, `Idade`, `Sexo`, `Refeicao`) para enriquecer o dataset e permitir a análise das hipóteses.
5.  **Balanceamento de Classes:** Aplicação de `RandomOverSampler` para equalizar a distribuição da coluna `Nivel_Calorias`, garantindo que todas as classes tivessem a mesma quantidade de instâncias.
6.  **Análise de Correlação:** Geração de matrizes de correlação (heatmap) para identificar as relações entre os atributos numéricos e as calorias totais, antes e depois do balanceamento.
7.  **Pré-processamento para Modelagem (Normalização e Padronização):** Aplicação de `MinMaxScaler` para normalização (escalar dados para um intervalo fixo, geralmente 0-1) e `StandardScaler` para padronização (transformar dados para ter média 0 e desvio padrão 1) nos atributos numéricos, preparando os dados para algoritmos de Machine Learning.
8.  **Validação das Hipóteses:** Utilização de visualizações (barras, dispersão, histogramas) com `plotly` (para interatividade em ambiente Colab) e `matplotlib` (para compatibilidade em ambientes como GitHub) para responder às cinco hipóteses levantadas.

## Conclusões das Hipóteses

Os resultados obtidos através da análise e visualizações confirmaram as seguintes hipóteses:

1.  **Gênero com maior ingestão calórica:** O grupo **'FEMININO'** foi identificado como o que mais ingere calorias totais.
2.  **Estado com maior consumo calórico:** **ALAGOAS (AL)** destacou-se com o maior consumo total de calorias.
3.  **Macronutriente mais consumido por gênero:** A **Proteína** foi o macronutriente mais consumido pelos três gêneros.
4.  **Identificação do nível calórico por gênero:** **Sim**, foi possível identificar a distribuição dos níveis de calorias ('BAIXA', 'MEDIA', 'ALTA') entre os gêneros, mostrando padrões distintos.
5.  **Faixa etária com maior consumo de Proteínas:** A faixa etária em torno dos **39 anos** apresentou o maior consumo de **Proteínas**.

## Ferramentas e Bibliotecas

*   **Python**
*   **Pandas:** Manipulação e análise de dados.
*   **NumPy:** Operações numéricas.
*   **Matplotlib:** Geração de gráficos estáticos.
*   **Seaborn:** Visualização estatística de dados.
*   **Plotly:** Geração de gráficos interativos.
*   **Scikit-learn (sklearn):** Pré-processamento (normalização, padronização, divisão de treino/teste).
*   **Imblearn (RandomOverSampler):** Balanceamento de classes.

## Como Executar o Projeto

1.  **Ambiente:** O projeto foi desenvolvido e testado no Google Colab. Recomenda-se a execução neste ambiente para garantir a compatibilidade das bibliotecas e visualizações interativas do Plotly.
2.  **Dependências:** As bibliotecas necessárias estão listadas na seção de importações do notebook. Caso esteja executando localmente, instale-as via pip:
    ```bash
    pip install pandas numpy matplotlib seaborn scikit-learn imblearn plotly
    ```
3.  **Execução:** Abra o arquivo `.ipynb` em um ambiente Jupyter (como Google Colab ou Jupyter Notebook/Lab) e execute as células sequencialmente.
