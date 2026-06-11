Projeto MVP — Machine Learning & Analytics

Este repositório contém o MVP (Produto Mínimo Viável) da Sprint de Machine Learning & Analytics, focado na classificação de níveis de calorias a partir de dados de macronutrientes.

## 📋 Informações Gerais

*   **Nome:** Marcos Aurélio Guidolini
*   **Matrícula:** 4052025002325
*   **Data:** 28/05/2026
*   **Notebook Original:** [`MVP_ML_Analytics_Classificacao_Calorias.ipynb`](https://github.com/MGuidolini/PUC-MVP/blob/Sprint02---Machine-Learning-%26-Analytics/MVP_ML_Analytics_Final.ipynb)

## 🎯 Definição do Problema

O objetivo deste projeto é desenvolver e avaliar modelos de Machine Learning para classificar a ingestão de macronutrientes de alimentos em três níveis calóricos: **Baixo**, **Médio** e **Alto**. A aplicação visa auxiliar profissionais da área de nutrição a identificar rapidamente o perfil calórico de uma refeição.

*   **Tipo de Problema:** Classificação Multiclasse.
*   **Critério de Sucesso:** F1-score ponderado (weighted F1-score), superando o modelo baseline (Dummy Classifier) em pelo menos 10%.
*   **Restrições:** Tempo de treinamento e inferência inferior a 1 minuto.

## 📊 Dataset

*   **Nome:** Calorie Dataset
*   **Fonte:** [`calorie_dataset.csv`](https://raw.githubusercontent.com/MGuidolini/PUC-MVP/refs/heads/main/calorie_dataset.csv)
*   **Descrição:** Conjunto de dados sintético, mas realista, contendo 5.000 amostras com informações de macronutrientes (Carboidrato, Proteína, Gordura, Fibra e Açúcar em gramas), calorias totais e uma classe de calorias.
*   **Atributos Chave:**
    *   `Carboidrato/g`, `Proteina/g`, `Gordura/g`, `Fibra/g`, `Acucar/g`: Quantidades de macronutrientes.
    *   `Calorias_Totais/Kcal`: Coluna de calorias calculada corretamente (a coluna original foi identificada como incorreta e substituída).
    *   `Nivel_Calorias`: Target ('BAIXA': < 400 Kcal, 'MEDIA': 400-699 Kcal, 'ALTA': >= 700 Kcal).

## 🔍 Análise Exploratória dos Dados (EDA)

*   **Correção de Dados:** Identificada e corrigida uma inconsistência na coluna de calorias original, criando `Calorias_Totais/Kcal` e um novo target `Nivel_Calorias` com base na regra de cálculo.
*   **Valores Ausentes/Duplicados:** Nenhuma ocorrência.
*   **Desbalanceamento de Classes:** O target `Nivel_Calorias` apresentou um desbalanceamento significativo (MEDIA: ~78.8%, ALTA: ~11.7%, BAIXA: ~9.5%).
*   **Escala das Variáveis:** `Calorias_Totais/Kcal` mostrou uma escala muito maior que os macronutrientes, justificando a padronização.

## ⚙️ Preparação dos Dados e Pré-processamento

*   **Divisão:**
    *   **Holdout:** 70% treino / 30% teste (estratificada).
    *   **Validação Cruzada:** `StratifiedKFold` com 5 folds, aplicada para otimização de hiperparâmetros.
*   **Pipeline de Pré-processamento:**
    *   `SimpleImputer(strategy="median")`: Para valores ausentes em colunas numéricas.
    *   `StandardScaler()`: Para padronizar features numéricas, crucial para modelos sensíveis à escala.
    *   `OneHotEncoder(handle_unknown="ignore")`: Para features categóricas (embora não aplicável neste conjunto de features).
*   **Tratamento de Desbalanceamento:** `SMOTE` (Synthetic Minority Over-sampling Technique) foi aplicado **dentro de cada fold de treino** da validação cruzada para balancear as classes e evitar o viés em relação às classes minoritárias.

## 📈 Modelagem e Avaliação

Foram avaliados os seguintes modelos:

*   **Baseline:** `DummyClassifier(strategy="most_frequent")` - F1-weighted ~0.025.
*   **Candidatos:**
    *   `LogisticRegression`
    *   `RandomForestClassifier`
    *   `XGBoostClassifier`
    *   `KNeighborsClassifier` (K-NN)

### Otimização de Hiperparâmetros

*   **Modelo Otimizado:** XGBoost
*   **Método:** `RandomizedSearchCV` (10 iterações) com 5 folds de `StratifiedKFold`.
*   **Métrica de Otimização:** F1-weighted.
*   **Melhores Hiperparâmetros:** `{'model__colsample_bytree': 0.7, 'model__gamma': 0, 'model__learning_rate': 0.05, 'model__max_depth': 7, 'model__n_estimators': 485, 'model__subsample': 0.9}`

### Desempenho do Modelo Final (XGBoost Otimizado)

O modelo **XGBoost Otimizado** foi selecionado como a melhor solução, atingindo os seguintes resultados no conjunto de teste (Holdout) após a otimização via Validação Cruzada:

| Métrica           | Valor     |
| :---------------- | :-------- |
| **F1-weighted**   | **0.99843** |
| **Accuracy**      | **0.99667** |
| **ROC AUC**       | **0.99995** |
| **Tempo de Treino** | **0.182 s** |

*   **Comparação com Baseline:** O modelo final apresentou uma melhoria superior a 4000% no F1-weighted em relação ao baseline, superando significativamente o critério de sucesso.
*   **Observação:** O `RandomForest` apresentou métricas quase perfeitas, mas com forte suspeita de *overfitting extremo* (ROC AUC de 1.0000 em CV), o que o tornou menos robusto para generalização em comparação com o XGBoost otimizado.

## 📝 Conclusão e Próximos Passos

O MVP demonstrou a construção e avaliação de modelos de ML para classificar níveis de calorias. O **XGBoost Otimizado** mostrou-se a solução mais equilibrada e robusta, com alto desempenho e boa capacidade de generalização.

### Limitações

*   **Dataset Sintético:** O uso de dados sintéticos pode limitar a generalização para cenários do mundo real.
*   **Desempenho Elevado:** Resultados próximos da perfeição podem mascarar sensibilidade excessiva a padrões do conjunto de treino.

### Próximos Passos

1.  **Validação com Dados Reais:** Testar o modelo com um dataset real para verificar a generalização.
2.  **Ajuste Fino Avançado:** Explorar técnicas de otimização mais avançadas ou refinadas.
3.  **Interpretabilidade:** Utilizar ferramentas como SHAP ou LIME para insights mais profundos.
4.  **Desenvolvimento de Interface:** Criar uma interface amigável para uso por profissionais de nutrição.

## 📦 Artefatos Salvos

*   [`comparacao_modelos_finais.csv`](https://raw.githubusercontent.com/MGuidolini/PUC-MVP/refs/heads/Sprint02---Machine-Learning-%26-Analytics/comparacao_modelos_finais.csv): Tabela comparativa detalhada de todos os modelos e métricas de avaliação.

