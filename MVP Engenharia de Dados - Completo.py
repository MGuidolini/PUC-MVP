# Databricks notebook source
# MAGIC %md
# MAGIC # MVP Engenharia de Dados - Analise de Alimentos e suas informações de macronutrientes

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # 1.0 - Contexto de Negócio e Perguntas
# MAGIC
# MAGIC > **Resumo:** Esta seção apresenta o contexto de negócio do projeto, descrevendo a visão geral, o problema central e as hipóteses e perguntas analíticas que guiarão toda a exploração dos dados nutricionais. O objetivo é estabelecer, desde o início, quais questões de negócio devem ser respondidas e quais hipóteses serão testadas ao longo do pipeline de dados.
# MAGIC
# MAGIC ---
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.1 -  🌐Visão Geral do Projeto
# MAGIC
# MAGIC O projeto consiste em analisar alimentos a partir de uma base nutricional ampla, padronizada e confiável, com o objetivo de responder perguntas sobre composição nutricional, densidade, qualidade dos alimentos e padrões alimentares. 
# MAGIC
# MAGIC A análise segue uma metodologia robusta, abordando desde a exploração inicial dos dados até a engenharia de novas características, culminando na validação de hipóteses cruciais para o entendimento dos padrões alimentares.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ###1.1.1 🧩 Descrição do Problema
# MAGIC
# MAGIC O problema central do projeto é: **como transformar dados nutricionais brutos em respostas claras, comparáveis e úteis sobre alimentos?**
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.1.2 📌 Hipóteses e Perguntas para Análise
# MAGIC
# MAGIC ####🧪 Hipóteses que você pode testar com uma tabela de nutrição
# MAGIC 1. Alimentos com maior densidade calórica tendem a ter menor teor de fibras.
# MAGIC 2. Frutas possuem maior concentração de carboidratos simples do que vegetais.
# MAGIC 3. Fontes de proteína animal têm mais gordura saturada do que fontes vegetais.
# MAGIC 4. Alimentos ultraprocessados apresentam maior teor de sódio do que alimentos naturais.
# MAGIC 5. Alimentos com alto teor de proteína têm maior saciedade por porção.
# MAGIC 6. Produtos integrais possuem mais fibras do que suas versões refinadas.
# MAGIC 7. Alimentos ricos em gordura têm menor volume por porção.
# MAGIC 8. Alimentos com maior teor de açúcar têm menor densidade de micronutrientes.
# MAGIC 9. Vegetais verdes escuros são mais ricos em ferro e cálcio do que vegetais claros.
# MAGIC 10. Snacks industrializados apresentam maior relação calorias/grama do que refeições completas.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ###1.1.3❓ Perguntas que você pode responder com a tabela
# MAGIC 1. Quais alimentos têm a melhor relação proteína por caloria?
# MAGIC 2. Quais itens são mais ricos em fibras por porção?
# MAGIC 3. Quais alimentos têm maior densidade nutricional (micronutrientes por caloria)?
# MAGIC 4. Quais opções possuem maior teor de sódio?
# MAGIC 5. Quais alimentos são mais adequados para dietas low-carb?
# MAGIC 6. Quais itens têm maior quantidade de gorduras saturadas?
# MAGIC 7. Quais alimentos são mais indicados para ganho de massa muscular?
# MAGIC 8. Quais opções são mais eficientes para quem busca saciedade com poucas calorias?
# MAGIC 9. Quais alimentos apresentam maior quantidade de açúcar adicionado?
# MAGIC 10. Quais itens são mais adequados para dietas veganas ou vegetarianas?

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # 2.0 - Preparação
# MAGIC
# MAGIC > **Resumo:** Esta seção é responsável por preparar todo o ambiente no Databricks antes da carga e transformação dos dados. O objetivo é garantir que a estrutura de organização — catálogo, schemas e volumes — esteja corretamente configurada no Unity Catalog, fornecendo uma base sólida e limpa para as etapas subsequentes do pipeline. Aqui são criados o catálogo `MVP_ENG_DADOS` e os schemas que compõem a **arquitetura de medalhão** (`bronze`, `silver`, `gold`), além dos schemas auxiliares `adaptacao` e `analise`, que servem para armazenar transformações intermediárias e resultados analíticos.
# MAGIC
# MAGIC ---
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.1 - Preparando o Ambiente
# MAGIC
# MAGIC > **Resumo:** Esta seção prepara o ambiente no Databricks criando o catálogo `MVP_ENG_DADOS` e os schemas que organizam os dados ao longo do pipeline. Inicialmente, o catálogo anterior é removido para garantir um estado limpo; em seguida, o catálogo é recriado e definido como ativo. Por fim, são criados os schemas `bronze`, `silver` e `gold` — que compõem a **arquitetura de medalhão** (Medallion Architecture) — além dos schemas auxiliares `adaptacao` e `analise`, que servem para armazenar tabelas de apoio, transformações intermediárias e resultados analíticos.
# MAGIC
# MAGIC ### 📋 Etapas desta seção
# MAGIC
# MAGIC 1. **Apagar o catálogo `MVP_ENG_DADOS`** (se existir) para garantir um ambiente limpo.
# MAGIC 2. **Criar o catálogo `MVP_ENG_DADOS`** no Unity Catalog.
# MAGIC 3. **Definir o catálogo como ativo** com `USE CATALOG`.
# MAGIC 4. **Criar o schema `bronze`** — camada de dados brutos.
# MAGIC 5. **Criar o schema `silver`** — camada de dados tratados e normalizados.
# MAGIC 6. **Criar o schema `gold`** — camada de dados consolidados prontos para consumo.
# MAGIC 7. **Criar o schema `adaptacao`** — espaço auxiliar para transformações intermediárias.
# MAGIC 8. **Criar o schema `analise`** — espaço auxiliar para análises e relatórios.
# MAGIC
# MAGIC > Ao final desta seção, toda a estrutura de organização de dados estará pronta para receber as cargas e transformações das próximas etapas.

# COMMAND ----------

# DBTITLE 1,Apaga o catálogo MVP_ENG_DADOS
# MAGIC %sql
# MAGIC DROP CATALOG IF EXISTS MVP_ENG_DADOS CASCADE

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.1.1 - Resumo da célula - Apaga o catálogo MVP_ENG_DADOS
# MAGIC
# MAGIC > **Resumo:** Esta célula remove completamente o catálogo `MVP_ENG_DADOS` e todos os seus objetos dependentes (schemas, tabelas, views), garantindo um ambiente limpo antes da recriação da estrutura.
# MAGIC
# MAGIC O comando abaixo **remove completamente o catálogo** `MVP_ENG_DADOS`:
# MAGIC
# MAGIC ```sql
# MAGIC DROP CATALOG IF EXISTS MVP_ENG_DADOS CASCADE
# MAGIC ```
# MAGIC
# MAGIC - **`DROP CATALOG`**: exclui um catálogo do Unity Catalog, incluindo todos os schemas e tabelas associados a ele.
# MAGIC - **`IF EXISTS`**: evita erros caso o catálogo ainda não exista — se ele não estiver presente, o comando simplesmente não faz nada.
# MAGIC - **`CASCADE`**: garante que a exclusão seja recursiva, removendo automaticamente todos os objetos dependentes (schemas, tabelas, views, etc.) dentro do catálogo.
# MAGIC
# MAGIC > Esse comando é útil em ambientes de desenvolvimento para garantir um estado limpo antes de recriar a estrutura do zero, que é exatamente o que acontece na célula seguinte.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cria o catálogo MVP_ENG_DADOS
# MAGIC %sql
# MAGIC CREATE CATALOG MVP_ENG_DADOS

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.1.2 - Resumo da célula - Cria o catálogo MVP_ENG_DADOS
# MAGIC
# MAGIC > **Resumo:** Esta célula cria um novo catálogo `MVP_ENG_DADOS` no Unity Catalog, que servirá como namespace principal para agrupar os schemas (`bronze`, `silver`, `gold`) e suas respectivas tabelas.
# MAGIC
# MAGIC O comando abaixo **cria um novo catálogo** no Unity Catalog:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE CATALOG MVP_ENG_DADOS
# MAGIC ```
# MAGIC
# MAGIC - **`CREATE CATALOG`**: cria um catálogo no Unity Catalog, que é o nível mais alto da hierarquia de organização de dados (`CATALOG.SCHEMA.TABLE`).
# MAGIC - **`MVP_ENG_DADOS`**: é o nome do catálogo. Ele servirá como namespace principal para agrupar os schemas (`bronze`, `silver`, `gold`) e suas respectivas tabelas.
# MAGIC
# MAGIC > Este catálogo foi criado logo após a remoção (DROP) do catálogo anterior, garantindo que o ambiente esteja limpo e pronto para a recriação da estrutura do zero.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Utiliza o catálogo MVP_ENG_DADOS
# MAGIC %sql
# MAGIC USE CATALOG MVP_ENG_DADOS 

# COMMAND ----------

# MAGIC %md
# MAGIC    
# MAGIC
# MAGIC ### 2.1.3 - Resumo da célula - Utiliza o catálogo MVP_ENG_DADOS
# MAGIC
# MAGIC > **Resumo:** Esta célula define o catálogo `MVP_ENG_DADOS` como o catálogo ativo na sessão atual, fazendo com que todos os comandos SQL subsequentes que referenciem schemas ou tabelas sem qualificação de catálogo sejam resolvidos dentro dele.
# MAGIC
# MAGIC O comando abaixo **seleciona o catálogo** `MVP_ENG_DADOS` como ativo:
# MAGIC
# MAGIC ```sql
# MAGIC USE CATALOG MVP_ENG_DADOS
# MAGIC ```
# MAGIC
# MAGIC - **`USE CATALOG`**: define o catálogo ativo para a sessão. A partir desse ponto, qualquer referência a um schema ou tabela sem prefixo de catálogo será automaticamente resolvida dentro de `MVP_ENG_DADOS`.
# MAGIC - **`MVP_ENG_DADOS`**: é o nome do catálogo que foi criado na célula anterior e agora será utilizado como namespace padrão.
# MAGIC
# MAGIC > Este comando é executado logo após a criação do catálogo, garantindo que os próximos comandos (`CREATE SCHEMA bronze`, `CREATE SCHEMA silver`, etc.) sejam criados dentro do catálogo correto, sem necessidade de referenciar o catálogo explicitamente em cada comando.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cria Schema Bronze
# MAGIC %sql
# MAGIC CREATE SCHEMA bronze

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.1.4 - Resumo da célula - Cria o schema bronze
# MAGIC
# MAGIC > **Resumo:** Esta célula cria o schema `bronze` dentro do catálogo ativo `MVP_ENG_DADOS`, estabelecendo a primeira camada da arquitetura de medalhão, onde os dados serão ingeridos em seu formato bruto, sem transformações significativas.
# MAGIC
# MAGIC #### Explicação do código
# MAGIC
# MAGIC O comando abaixo **cria o schema** `bronze` dentro do catálogo ativo `MVP_ENG_DADOS`:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE SCHEMA bronze
# MAGIC ```
# MAGIC
# MAGIC - **`CREATE SCHEMA`**: cria um schema (também chamado de *database*) dentro do catálogo atualmente selecionado na sessão. Como o comando `USE CATALOG MVP_ENG_DADOS` já foi executado, não é necessário referenciar o catálogo explicitamente.
# MAGIC - **`bronze`**: é o nome do schema. Na arquitetura de medalhão (Medallion Architecture), a camada **bronze** é a primeira etapa, onde os dados são ingeridos em seu formato bruto, sem transformações significativas.
# MAGIC
# MAGIC > O schema `bronze` servirá como local de armazenamento das tabelas de dados raw, que posteriormente serão tratadas e enviadas para as camadas `silver` e `gold`.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cria Schema Silver
# MAGIC %sql
# MAGIC CREATE SCHEMA silver
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC    
# MAGIC ### 2.1.5 - Resumo da célula - Cria o schema silver
# MAGIC
# MAGIC > **Resumo:** Esta célula cria o schema `silver` dentro do catálogo ativo `MVP_ENG_DADOS`, estabelecendo a segunda camada da arquitetura de medalhão, onde os dados provenientes da camada `bronze` passam por limpeza, normalização e padronização.
# MAGIC
# MAGIC #### Explicação do código
# MAGIC
# MAGIC O comando abaixo **cria o schema** `silver` dentro do catálogo ativo `MVP_ENG_DADOS`:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE SCHEMA silver
# MAGIC ```
# MAGIC
# MAGIC - **`CREATE SCHEMA`**: cria um schema (também chamado de *database*) dentro do catálogo atualmente selecionado na sessão. Como o comando `USE CATALOG MVP_ENG_DADOS` já foi executado, não é necessário referenciar o catálogo explicitamente.
# MAGIC - **`silver`**: é o nome do schema. Na arquitetura de medalhão (Medallion Architecture), a camada **silver** é a segunda etapa, onde os dados provenientes da camada `bronze` passam por limpeza, normalização e padronização, tornando-se mais confiáveis e prontos para análise.
# MAGIC
# MAGIC > O schema `silver` servirá como local de armazenamento das tabelas com dados tratados e enriquecidos, que posteriormente serão consolidados na camada `gold` para consumo final.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cria Schema Gold
# MAGIC %sql
# MAGIC CREATE SCHEMA gold

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC
# MAGIC ### 2.1.6 - Resumo da célula - Cria o schema gold
# MAGIC
# MAGIC > **Resumo:** Esta célula cria o schema `gold` dentro do catálogo ativo `MVP_ENG_DADOS`, estabelecendo a última camada da arquitetura de medalhão, onde os dados já tratados e enriquecidos nas camadas `bronze` e `silver` são consolidados em sua forma final, prontos para consumo analítico e de negócio.
# MAGIC
# MAGIC #### Explicação do código
# MAGIC
# MAGIC O comando abaixo **cria o schema** `gold` dentro do catálogo ativo `MVP_ENG_DADOS`:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE SCHEMA gold
# MAGIC ```
# MAGIC
# MAGIC - **`CREATE SCHEMA`**: cria um schema (também chamado de *database*) dentro do catálogo atualmente selecionado na sessão. Como o comando `USE CATALOG MVP_ENG_DADOS` já foi executado, não é necessário referenciar o catálogo explicitamente.
# MAGIC - **`gold`**: é o nome do schema. Na arquitetura de medalhão (Medallion Architecture), a camada **gold** é a última etapa, onde os dados já tratados e enriquecidos nas camadas `bronze` e `silver` são consolidados em sua forma final, prontos para consumo por analistas, cientistas de dados e aplicações de negócio.
# MAGIC
# MAGIC > O schema `gold` servirá como local de armazenamento das tabelas com dados curados e em nível de negócio, que representam a visão final e analítica dos dados processados ao longo de todo o pipeline.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cria Schema Adaptação
# MAGIC %sql
# MAGIC CREATE SCHEMA adaptacao

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.1.7 - Resumo da célula - Cria o schema adaptacao
# MAGIC
# MAGIC > **Resumo:** Esta célula cria o schema `adaptacao` dentro do catálogo ativo `MVP_ENG_DADOS`, estabelecendo um espaço auxiliar fora do fluxo principal da arquitetura de medalhão, destinado a armazenar tabelas de apoio, ajustes e transformações intermediárias.
# MAGIC
# MAGIC #### Explicação do código
# MAGIC
# MAGIC O comando abaixo **cria o schema** `adaptacao` dentro do catálogo ativo `MVP_ENG_DADOS`:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE SCHEMA adaptacao
# MAGIC ```
# MAGIC
# MAGIC - **`CREATE SCHEMA`**: cria um schema (também chamado de *database*) dentro do catálogo atualmente selecionado na sessão. Como o comando `USE CATALOG MVP_ENG_DADOS` já foi executado, não é necessário referenciar o catálogo explicitamente.
# MAGIC - **`adaptacao`**: é o nome do schema. Diferente das camadas da arquitetura de medalhão (`bronze`, `silver`, `gold`), este schema tem um propósito **auxiliar** e serve como um espaço separado para armazenar tabelas de **apoio, ajustes ou transformações intermediárias** que não se encaixam diretamente no fluxo principal de bronze → silver → gold.
# MAGIC
# MAGIC > O schema `adaptacao` pode ser utilizado, por exemplo, para armazenar tabelas temporárias, dados de parametrização, tabelas de mapeamento (lookup) ou resultados de transformações intermediárias que ainda não estão prontos para a camada `gold`, mantendo o fluxo principal de dados organizado e separado.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cria Schema Analise
# MAGIC %sql
# MAGIC CREATE SCHEMA analise

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 2.1.8 - Resumo da célula - Cria o schema analise
# MAGIC
# MAGIC > **Resumo:** Esta célula cria o schema `analise` dentro do catálogo ativo `MVP_ENG_DADOS`, estabelecendo um espaço auxiliar fora do fluxo principal da arquitetura de medalhão, destinado a armazenar tabelas de análise, relatórios e resultados exploratórios que consomem dados já processados nas camadas anteriores.
# MAGIC
# MAGIC #### Explicação do código
# MAGIC
# MAGIC O comando abaixo **cria o schema** `analise` dentro do catálogo ativo `MVP_ENG_DADOS`:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE SCHEMA analise
# MAGIC ```
# MAGIC
# MAGIC - **`CREATE SCHEMA`**: cria um schema (também chamado de *database*) dentro do catálogo atualmente selecionado na sessão. Como o comando `USE CATALOG MVP_ENG_DADOS` já foi executado, não é necessário referenciar o catálogo explicitamente.
# MAGIC - **`analise`**: é o nome do schema. Assim como o schema `adaptacao`, este schema tem um propósito **auxiliar** e não faz parte do fluxo principal da arquitetura de medalhão (`bronze` → `silver` → `gold`). Ele serve como um espaço dedicado para armazenar tabelas de **análise, relatórios ou resultados exploratórios** que consomem dados já processados nas camadas anteriores.
# MAGIC
# MAGIC > O schema `analise` pode ser utilizado, por exemplo, para armazenar tabelas agregadas, views analíticas, resultados de consultas ad-hoc ou conjuntos de dados preparados especificamente para consumo por ferramentas de BI e relatórios de negócio, mantendo esses artefatos separados das camadas principais do pipeline.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.2 - Evidência de Catálogo e Schemas Criados
# MAGIC
# MAGIC ![image_1790215534934.png](./image_1790215534934.png "image_1790215534934.png")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # 3.0 - Carga de Dados
# MAGIC
# MAGIC > **Resumo:** Esta seção é responsável por realizar a carga de dados no pipeline, abrangendo o download dos arquivos de origem (Food_Nutrition.csv e Taco.csv) para um volume no Unity Catalog, a leitura desses arquivos CSV e a criação das tabelas na camada **bronze**, onde os dados serão armazenados em seu formato bruto para posterior processamento nas camadas `silver` e `gold`.
# MAGIC
# MAGIC ---
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.1 - Download dos Arquivos
# MAGIC
# MAGIC > **Resumo:** Esta seção é responsável por preparar o ambiente para a carga de dados, definindo o catálogo ativo, criando um volume de armazenamento no Unity Catalog e copiando os arquivos de origem (Food_Nutrition.csv e Taco.csv) do workspace do Databricks para o volume `nutri_alimentos` no schema `adaptacao`, de onde poderão ser lidos e processados nas etapas subsequentes.
# MAGIC
# MAGIC #### Etapas realizadas nesta seção:
# MAGIC
# MAGIC 1. **Utilização do catálogo:** Define `MVP_ENG_DADOS` como catálogo ativo na sessão atual do Unity Catalog, garantindo que todas as operações subsequentes sejam executadas dentro deste catálogo.
# MAGIC
# MAGIC 2. **Criação do volume:** Cria o volume `nutri_alimentos` no schema `adaptacao`, que servirá como local de armazenamento para os arquivos CSV contendo os dados de composição nutricional de alimentos.
# MAGIC
# MAGIC 3. **Download do Food Nutrition Dataset:** Copia o arquivo **Food_Nutrition.csv** — contendo dados de composição nutricional de alimentos dos EUA provenientes do USDA (Departamento de Agricultura dos EUA) — do workspace do Databricks para o volume criado.
# MAGIC
# MAGIC 4. **Download do Taco Dataset:** Copia o arquivo **Taco.csv** — contendo dados de composição nutricional de alimentos brasileiros baseados na Tabela Brasileira de Composição de Alimentos (TACO) — do workspace do Databricks para o mesmo volume.
# MAGIC
# MAGIC > Ao final desta seção, os dois conjuntos de dados estarão disponíveis no volume `/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/`, prontos para serem lidos, transformados e carregados nas camadas da arquitetura de medalhão (bronze, silver e gold) nas próximas etapas do pipeline.

# COMMAND ----------

# DBTITLE 1,Utilizar Catalago e Schema criado na Preparação
# MAGIC %sql
# MAGIC USE CATALOG MVP_ENG_DADOS;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 3.1.1 - Resumo: 
# MAGIC Define o catálogo `MVP_ENG_DADOS` como ativo na sessão atual do Unity Catalog.
# MAGIC
# MAGIC ####Explicação do Código: 
# MAGIC O comando `USE CATALOG MVP_ENG_DADOS;` acima, define o catálogo `MVP_ENG_DADOS` como o catálogo ativo para a sessão atual no Unity Catalog. Isso significa que todas as operações subsequentes (como criação de volumes, tabelas e schemas) serão realizadas dentro deste catálogo, a menos que seja explicitamente especificado outro catálogo.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cria um volume chamado Calorias
# MAGIC
# MAGIC %sql
# MAGIC CREATE VOLUME adaptacao.nutri_alimentos

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 3.1.2 - Resumo: 
# MAGIC Cria o volume `nutri_alimentos` no schema `adaptacao` do catálogo `MVP_ENG_DADOS`, que será utilizado como local de armazenamento para arquivos não estruturados, como CSVs, imagens, PDFs, etc.
# MAGIC
# MAGIC ####Explicação do Código: 
# MAGIC O comando `CREATE VOLUME adaptacao.nutri_alimentos` acima, cria um volume chamado `nutri_alimentos` no schema `adaptacao` do catálogo `MVP_ENG_DADOS` (que foram definidos anteriormente). Um volume no Unity Catalog é um local de armazenamento para arquivos não estruturados, como CSVs, imagens, PDFs, etc. Isso significa que todos os arquivos copiados para este volume poderão ser acessados por comandos subsequentes (como leitura de CSVs, cópia de arquivos, etc.) utilizando o caminho `/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/`, a menos que seja explicitamente especificado outro caminho.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.2 - Food Nutrition Dataset

# COMMAND ----------

# DBTITLE 1,Copia Arquivo Food_Nutrition.csv
dbutils.fs.cp(
    "file:/Workspace/Users/mguidolini@gmail.com/Engenharia de Dados/Food_Nutrition.csv",
    "/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/Food_Nutrition.csv"
)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 3.2.1 - Resumo: 
# MAGIC Copia o arquivo **Food_Nutrition.csv** do workspace do Databricks para o volume `nutri_alimentos` no schema `adaptacao` do catálogo `MVP_ENG_DADOS`, disponibilizando-o para leitura e processamento nas próximas etapas.
# MAGIC
# MAGIC #### Explicação do Código: 
# MAGIC O comando `dbutils.fs.cp()` acima copia o arquivo **Food_Nutrition.csv** de uma origem para um destino:
# MAGIC
# MAGIC - **Origem:** `file:/Workspace/Users/mguidolini@gmail.com/Engenharia de Dados/Food_Nutrition.csv` — um arquivo armazenado no workspace do Databricks.
# MAGIC - **Destino:** `/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/Food_Nutrition.csv` — o volume `nutri_alimentos` criado anteriormente no schema `adaptacao` do catálogo `MVP_ENG_DADOS`.
# MAGIC
# MAGIC Isso significa que o arquivo **Food_Nutrition.csv**, que contém dados de composição nutricional de alimentos, é copiado do workspace para o volume do Unity Catalog, onde poderá ser acessado por comandos subsequentes (como leitura de CSVs e criação de tabelas) utilizando o caminho `/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/Food_Nutrition.csv`.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3.2.2 - Sobre o Conjunto de Dados
# MAGIC #### Contexto
# MAGIC Este conjunto de dados provém do Laboratório de Métodos e Aplicações de Composição de Alimentos (***Methods and Application of Food Composition Laboratory***), cuja missão é identificar necessidades críticas de dados sobre composição de alimentos para pesquisadores, formuladores de políticas, produtores de alimentos e consumidores (**Departamento de Agricultura dos EUA – USDA**).
# MAGIC
# MAGIC O objetivo principal é prever, analisar e explorar a composição de diversos alimentos dos EUA. A análise preditiva permite, tipicamente, prever a categoria do alimento utilizando outras características, como `Energy_kcal` (**energia em kcal**), `Protein_g` (**proteínas em g**), etc.
# MAGIC
# MAGIC Conteúdo
# MAGIC O conjunto de dados foi obtido em: https://data.world/craigkelly/usda-national-nutrient-db. Foram realizadas etapas de limpeza e exploração para refinar os dados e dividi-los em conjuntos de treino e teste.
# MAGIC Cada registro refere-se a uma porção de 100 gramas.
# MAGIC
# MAGIC #### Campos do arquivo Food_Nutrition.csv (24 colunas)
# MAGIC
# MAGIC | # | Campo (CSV original) | Tipo | Descrição |
# MAGIC |---|---|---|---|
# MAGIC | 1 | `food` | string | Nome do alimento |
# MAGIC | 2 | `Caloric Value` | int | Valor calórico do alimento (kcal) |
# MAGIC | 3 | `Fat` | float | Quantidade total de gordura (g) |
# MAGIC | 4 | `Saturated Fats` | float | Quantidade de gorduras saturadas (g) |
# MAGIC | 5 | `Monounsaturated Fats` | float | Quantidade de gorduras monoinsaturadas (g) |
# MAGIC | 6 | `Polyunsaturated Fats` | float | Quantidade de gorduras poliinsaturadas (g) |
# MAGIC | 7 | `Carbohydrates` | float | Quantidade total de carboidratos (g) |
# MAGIC | 8 | `Sugars` | float | Quantidade de açúcares (g) |
# MAGIC | 9 | `Protein` | float | Quantidade de proteína (g) |
# MAGIC | 10 | `Dietary Fiber` | float | Quantidade de fibra alimentar (g) |
# MAGIC | 11 | `Cholesterol` | float | Quantidade de colesterol (mg) |
# MAGIC | 12 | `Sodium` | float | Quantidade de sódio (mg) |
# MAGIC | 13 | `Water` | float | Teor de água (g) |
# MAGIC | 14 | `Vitamins` | float | Quantidade total de vitaminas (mg) |
# MAGIC | 15 | `Calcium` | float | Quantidade de cálcio (mg) |
# MAGIC | 16 | `Copper` | float | Quantidade de cobre (mg) |
# MAGIC | 17 | `Iron` | float | Quantidade de ferro (mg) |
# MAGIC | 18 | `Magnesium` | float | Quantidade de magnésio (mg) |
# MAGIC | 19 | `Manganese` | float | Quantidade de manganês (mg) |
# MAGIC | 20 | `Phosphorus` | float | Quantidade de fósforo (mg) |
# MAGIC | 21 | `Potassium` | float | Quantidade de potássio (mg) |
# MAGIC | 22 | `Selenium` | float | Quantidade de selênio (µg) |
# MAGIC | 23 | `Zinc` | float | Quantidade de zinco (mg) |
# MAGIC | 24 | `Nutrition Density` | float | Densidade nutricional do alimento |
# MAGIC
# MAGIC  **Dataset de Referência**  [Kaggle — USDA - National Nutrient Database](https://www.kaggle.com/datasets/haithemhermessi/usda-national-nutrient-database)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.3 - Taco Dataset

# COMMAND ----------

# DBTITLE 1,Copia Arquivo Taco.csv
dbutils.fs.cp(
    "file:/Workspace/Users/mguidolini@gmail.com/Engenharia de Dados/Taco.csv",
    "/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/Taco.csv"
)

# COMMAND ----------

# MAGIC %md
# MAGIC    
# MAGIC
# MAGIC ### 3.3.1 - Resumo: 
# MAGIC Copia o arquivo **Taco.csv** do workspace do Databricks para o volume `nutri_alimentos` no schema `adaptacao` do catálogo `MVP_ENG_DADOS`, disponibilizando-o para leitura e processamento nas próximas etapas.
# MAGIC
# MAGIC #### Explicação do Código: 
# MAGIC O comando `dbutils.fs.cp()` acima copia o arquivo **Taco.csv** de uma origem para um destino:
# MAGIC
# MAGIC - **Origem:** `file:/Workspace/Users/mguidolini@gmail.com/Engenharia de Dados/Taco.csv` — um arquivo armazenado no workspace do Databricks.
# MAGIC - **Destino:** `/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/Taco.csv` — o volume `nutri_alimentos` criado anteriormente no schema `adaptacao` do catálogo `MVP_ENG_DADOS`.
# MAGIC
# MAGIC Isso significa que o arquivo **Taco.csv**, que contém dados de composição nutricional de alimentos brasileiros baseada na TACO (Tabela Brasileira de Composição de Alimentos), é copiado do workspace para o volume do Unity Catalog, onde poderá ser acessado por comandos subsequentes (como leitura de CSVs e criação de tabelas) utilizando o caminho `/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/Taco.csv`.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3.2.2 - Sobre o Conjunto de Dados
# MAGIC #### Contexto
# MAGIC Composição dos alimentos por 100 gramas de parte comestível.
# MAGIC
# MAGIC ####Legenda Abreviações:
# MAGIC - g: grama;
# MAGIC - µg: micrograma;
# MAGIC - kcal: kilocaloria;
# MAGIC - kJ: kilojoule;
# MAGIC - mg: miligrama;
# MAGIC - NA: não aplicável;
# MAGIC - Tr: traço.
# MAGIC - Valores em branco nesta tabela: análises não solicitadas.
# MAGIC (*): as análises estão sendo reavaliadas.
# MAGIC #### Adotou-se traço nas seguintes situações:
# MAGIC - valores de nutrientes arredondados para números que caiam entre 0 e 0.5;
# MAGIC - valores de nutrientes arredondados para números com uma casa decimal que caiam entre 0 e 0.05;
# MAGIC - valores de nutrientes arredondados para números, com duas casas decimais que caiam entre 0 e 0.005 e;
# MAGIC - valores abaixo dos limites de quantificação (33).
# MAGIC ####Limites de Quantificação:
# MAGIC - composição centesimal: 0.1g/100g;
# MAGIC - colesterol: 1mg/100g;
# MAGIC - Cu Fe Mn e Zn: 0.001mg/100g; d) Ca Na: 0.04mg/100g;
# MAGIC - K e P: 0.001mg/100g;
# MAGIC - Mg: 0.015mg/100g;
# MAGIC - tiamina riboflavina e piridoxina: 0.03mg/100g;
# MAGIC - niacina e vitamina C: 1mg/100g;
# MAGIC - retinol em produtos cárneos e outros: 3 µg/100g e;
# MAGIC - retinol em lácteos: 20µg/100g.
# MAGIC
# MAGIC Valores correspondentes à somatória do resultado analítico do retinol mais o valor calculado com base no teor de carotenóides segundo o livro Fontes brasileiras de carotenóides: tabela brasileira, de composição de carotenóides em alimentos (25).
# MAGIC
# MAGIC #### Campos do arquivo Taco.csv (27 colunas)
# MAGIC
# MAGIC | # | Campo (CSV original) | Tipo | Descrição |
# MAGIC |---|---|---|---|
# MAGIC | 1 | `Número` | int | Código identificador do alimento |
# MAGIC | 2 | `Descrição` | string | Nome/descrição do alimento |
# MAGIC | 3 | `Umidade (%)` | float | Teor de umidade do alimento (g / 100 g) |
# MAGIC | 4 | `Energia (kcal)` | float | Valor energético (kcal / 100 g) |
# MAGIC | 5 | `Proteína (g)` | float | Quantidade de proteína (g / 100 g) |
# MAGIC | 6 | `Lipídeos (g)` | float | Quantidade de lipídeos (g / 100 g) |
# MAGIC | 7 | `Colesterol (mg)` | float | Quantidade de colesterol (mg / 100 g) |
# MAGIC | 8 | `Carboidrato (g)` | float | Quantidade de carboidratos (g / 100 g) |
# MAGIC | 9 | `Fibra alimentar (g)` | float | Quantidade de fibra alimentar (g / 100 g) |
# MAGIC | 10 | `Cinzas (g)` | float | Teor de cinzas — minerais residuais (g / 100 g) |
# MAGIC | 11 | `Cálcio (mg)` | float | Quantidade de cálcio (mg / 100 g) |
# MAGIC | 12 | `Magnésio (mg)` | float | Quantidade de magnésio (mg / 100 g) |
# MAGIC | 13 | `Manganês (mg)` | float | Quantidade de manganês (mg / 100 g) |
# MAGIC | 14 | `Fósforo (mg)` | float | Quantidade de fósforo (mg / 100 g) |
# MAGIC | 15 | `Ferro (mg)` | float | Quantidade de ferro (mg / 100 g) |
# MAGIC | 16 | `Sódio (mg)` | float | Quantidade de sódio (mg / 100 g) |
# MAGIC | 17 | `Potássio (mg)` | float | Quantidade de potássio (mg / 100 g) |
# MAGIC | 18 | `Cobre (mg)` | float | Quantidade de cobre (mg / 100 g) |
# MAGIC | 19 | `Zinco (mg)` | float | Quantidade de zinco (mg / 100 g) |
# MAGIC | 20 | `Retinolo (µg)` | float | Quantidade de retinol — vitamina A (µg / 100 g) |
# MAGIC | 21 | `RE (µg)` | float | Equivalente de retinol (µg / 100 g) |
# MAGIC | 22 | `RAE (µg)` | float | Atividade de equivalência de retinol (µg / 100 g) |
# MAGIC | 23 | `Tiamina (mg)` | float | Quantidade de tiamina — vitamina B1 (mg / 100 g) |
# MAGIC | 24 | `Riboflavina (mg)` | float | Quantidade de riboflavina — vitamina B2 (mg / 100 g) |
# MAGIC | 25 | `Piridoxamina (mg)` | float | Quantidade de piridoxamina — vitamina B6 (mg / 100 g) |
# MAGIC | 26 | `Niacina (mg)` | float | Quantidade de niacina — vitamina B3 (mg / 100 g) |
# MAGIC | 27 | `Vitamina C (mg)` | float | Quantidade de vitamina C — ácido ascórbico (mg / 100 g) |
# MAGIC
# MAGIC  **Dataset de Referência**  [Kaggle — Composição Nutricional de Alimentos TACO](https://www.kaggle.com/datasets/ispangler/composio-nutricional-de-alimentos-taco) 

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3.4 - Evidência do Download dos Arquivos
# MAGIC
# MAGIC ![image_1790215716497.png](./image_1790215716497.png "image_1790215716497.png")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # 4.0 - Pipeline, Modelagem e Catálogo de Dados
# MAGIC
# MAGIC Esta seção descreve a construção do **pipeline de dados** utilizando a arquitetura **Medallion** (camadas Bronze, Silver e Gold) no **Unity Catalog**, bem como a **modelagem** e o **catálogo de dados** do projeto.
# MAGIC
# MAGIC #### Arquitetura Medallion
# MAGIC
# MAGIC A arquitetura *Medallion* organiza os dados em camadas lógicas progressivas, cada uma com um nível crescente de qualidade e estruturação:
# MAGIC
# MAGIC | Camada | Descrição |
# MAGIC |---|---|
# MAGIC | **Bronze** | Ingestão dos dados brutos no formato original, sem transformações de negócio. Os dados são carregados dos arquivos CSV e persistidos como tabelas Delta. |
# MAGIC | **Silver** | Limpeza, padronização e enriquecimento dos dados da camada Bronze. Inclui tratamento de valores nulos, normalização de nomes de colunas, conversão de tipos e junção (*merge*) das fontes. |
# MAGIC | **Gold** | Dados prontos para consumo analítico e modelagem. Contém tabelas e visões otimizadas para consultas, relatórios e alimentação de modelos de *Machine Learning*. |
# MAGIC
# MAGIC #### Catálogo de Dados
# MAGIC
# MAGIC Todos os dados são governados pelo **Unity Catalog** sob o catálogo `MVP_ENG_DADOS`, organizado em *schemas* que refletem as camadas da arquitetura:
# MAGIC
# MAGIC - **`adaptacao`** — volume de armazenamento de arquivos não estruturados (CSVs de origem);
# MAGIC - **`Bronze`** — tabelas Delta com dados brutos;
# MAGIC - **`Silver`** — tabelas Delta com dados tratados e padronizados;
# MAGIC - **`Gold`** — tabelas e visões analíticas prontas para consumo.
# MAGIC
# MAGIC
# MAGIC #### Modelagem Dimensional (Esquema Estrela)
# MAGIC
# MAGIC A camada Gold também adota a **modelagem dimensional no estilo estrela** (*Star Schema*), que organiza os dados em **tabelas de fatos** e **tabelas de dimensões** para otimizar consultas analíticas e relatórios:
# MAGIC
# MAGIC - **Tabelas de Fatos (*Fact Tables*)** — contêm as **métricas quantitativas** (medidas) e as **chaves estrangeiras** que referenciam as dimensões. Representam os eventos ou transações do domínio (ex.: composição nutricional por alimento).
# MAGIC - **Tabelas de Dimensões (*Dimension Tables*)** — contêm os **atributos descritivos** que dão contexto às métricas (ex.: categoria do alimento, unidade de medida, origem do dado).
# MAGIC - **Relacionamentos** — cada tabela de fato é cercada por suas tabelas de dimensões, formando uma estrutura em forma de estrela, o que simplifica as consultas e melhora o desempenho das junções.
# MAGIC
# MAGIC | Elemento | Descrição |
# MAGIC |---|---|
# MAGIC | **Tabela de Fatos** | Armazena as medidas numéricas (ex.: calorias, proteínas, gorduras) e as chaves estrangeiras para as dimensões |
# MAGIC | **Tabela de Dimensão** | Armazena os atributos descritivos (ex.: nome do alimento, categoria, origem) |
# MAGIC | **Chave Primária (PK)** | Identificador único de cada registro na tabela de dimensão |
# MAGIC | **Chave Estrangeira (FK)** | Referência à chave primária da dimensão na tabela de fatos |
# MAGIC | **Granularidade** | Nível de detalhe de cada registro na tabela de fatos (ex.: um registro por alimento por 100 g) |
# MAGIC
# MAGIC A modelagem estrela traz os seguintes benefícios:
# MAGIC
# MAGIC - **Simplicidade** — consultas analíticas tornam-se mais intuitivas, com junções diretas entre fato e dimensões;
# MAGIC - **Desempenho** — o número reduzido de junções e a desnormalização das dimensões aceleram as consultas;
# MAGIC - **Facilidade de leitura** — a estrutura é facilmente compreendida por usuários de negócio e ferramentas de *BI*;
# MAGIC - **Escalabilidade** — novas dimensões podem ser adicionadas sem impacto significativo na tabela de fatos.
# MAGIC
# MAGIC ---
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4.1 - Camada Bronze
# MAGIC
# MAGIC A **Camada Bronze** é a primeira etapa da arquitetura *Medallion* e tem como objetivo **ingerir os dados brutos** oriundos das fontes originais, preservando sua forma original sem transformações significativas. Nesta camada, os dados são carregados diretamente dos arquivos CSV disponíveis no volume `nutri_alimentos` e persistidos como **tabelas Delta** no catálogo `MVP_ENG_DADOS`, schema `Bronze`.
# MAGIC
# MAGIC As principais características da Camada Bronze incluem:
# MAGIC
# MAGIC - **Ingestão de dados no formato original**, mantendo a fidelidade dos dados de origem;
# MAGIC - **Persistência no formato Delta**, garantindo características ACID e versionamento;
# MAGIC - **Sanitização mínima de nomes de colunas**, apenas para compatibilidade com o formato Delta (substituição de espaços, parênteses e caracteres especiais);
# MAGIC - **Sem transformações de negócio** — limpeza, enriquecimento e padronização ocorrem nas camadas posteriores (Silver e Gold).
# MAGIC
# MAGIC Nesta seção, serão criadas as seguintes tabelas na camada Bronze:
# MAGIC
# MAGIC | # | Tabela | Arquivo de Origem | Descrição |
# MAGIC |---|---|---|---|
# MAGIC | 1 | `Alimentos_Taco` | `Taco.csv` | Composição nutricional de alimentos brasileiros (TACO — UNICAMP) |
# MAGIC | 2 | `Alimentos_Food_Nutrition` | `Food_Nutrition.csv` | Composição nutricional de alimentos dos EUA (USDA) |

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.1.1 - Utilização de Catálogo e Schema

# COMMAND ----------

# DBTITLE 1,Utiliza o Catálogo MVP_ENG_DADOS e Schema Bronze
spark.sql("USE CATALOG MVP_ENG_DADOS")
spark.sql("USE SCHEMA Bronze")

# COMMAND ----------

# MAGIC %md
# MAGIC    
# MAGIC #### 4.1.1.1 - Resumo da célula (Utiliza o Catálogo MVP_ENG_DADOS e Schema Bronze)
# MAGIC
# MAGIC A célula acima configura o contexto do Unity Catalog para a sessão Spark, definindo:
# MAGIC
# MAGIC - O **catálogo** ativo como `MVP_ENG_DADOS`;
# MAGIC - O **schema** ativo como `Bronze`.
# MAGIC
# MAGIC Essa configuração garante que as tabelas criadas nas próximas células sejam armazenadas automaticamente no catálogo e schema corretos, sem necessidade de qualificar o nome completo em cada operação.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.1.2 - Criação da Tabela Alimentos_Taco.

# COMMAND ----------

# DBTITLE 1,Carrega arquivo Taco.csv
# Carrega arquivo csv usando Pandas
import pandas as pd

# Carrega diretamente do workspace usando o caminho do arquivo
file_path = "/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/Taco.csv"

# Lê o arquivo CSV - ele já tem cabeçalho, então não precisa renomear colunas
Alimentos_Taco = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';', decimal=',')

# Pega apenas os dados do dataset e guardando em um array
array = Alimentos_Taco.values


# Separa o array em variáveis preditoras (X) e variável target (Y)
X = array[:,0:8]
Y = array[:,0:8]

dafr_Alimentos_Taco = pd.DataFrame(data=Alimentos_Taco)

# Verificar e imprimir na tela o total de instâncias
print(f"Total de instâncias: {len(Alimentos_Taco)}")
print("\nTipos de dados por coluna:")
print(dafr_Alimentos_Taco.info())
print("✅ Dataset carregado com sucesso!")
print("\nColunas disponíveis:")
print(dafr_Alimentos_Taco.columns.tolist())
print("\nPrimeiras 5 linhas:")
display(dafr_Alimentos_Taco.head(5))
print(f"\nTotal de registros: {len(dafr_Alimentos_Taco)}")

# COMMAND ----------

# MAGIC %md
# MAGIC #### 4.1.2.1 - Resumo da célula (Carrega arquivo Taco.csv)
# MAGIC
# MAGIC A célula acima carrega o arquivo **Taco.csv** a partir de um caminho no Databricks Volumes usando **Pandas**, com encoding `ISO-8859-1`, separador `;` e decimal `,`. Em seguida:
# MAGIC
# MAGIC - Extrai os valores para um array e separa as variáveis preditoras (`X`) e a variável target (`Y`);
# MAGIC - Cria um DataFrame Pandas (`dafr_Alimentos_Taco`) a partir dos dados carregados;
# MAGIC - Exibe informações sobre o dataset: total de instâncias, tipos de dados, colunas disponíveis e as primeiras 5 linhas.
# MAGIC
# MAGIC Este DataFrame será utilizado na próxima célula para criar a tabela **Alimentos_Taco** no catálogo `MVP_ENG_DADOS`, schema `Bronze`.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Criar tabela Alimentos_Taco
# Criar tabela Alimentos_Taco no catálogo MVP_ENG_DADOS e schema Bronze
# e inserir os dados do dataframe dafr_Alimentos

# Converte o dataframe pandas para Spark DataFrame
# Sanitiza nomes de colunas removendo caracteres inválidos para Delta (espaços, parênteses, etc.)
for col_name in list(dafr_Alimentos_Taco.columns):
    safe_name = col_name.replace(' ', '_').replace('(', '').replace(')', '').replace('%', 'pct')
    dafr_Alimentos_Taco.rename(columns={col_name: safe_name}, inplace=True)

spark_df_Alimentos_Taco = spark.createDataFrame(dafr_Alimentos_Taco)

# Escreve o DataFrame no formato Delta como tabela no catálogo especificado
spark_df_Alimentos_Taco.write.mode("overwrite").saveAsTable("MVP_ENG_DADOS.Bronze.Alimentos_Taco")

print("✅ Tabela Alimentos_Taco criada com sucesso no catálogo MVP_ENG_DADOS, schema Bronze!")
print(f"Total de registros inseridos: {spark_df_Alimentos_Taco.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.1.2.2 - Resumo da célula (Criar tabela Alimentos_Taco)
# MAGIC
# MAGIC A célula acima cria a tabela **Alimentos_Taco** no catálogo `MVP_ENG_DADOS`, schema `Bronze`, a partir do DataFrame Pandas `dafr_Alimentos_Taco`. Para isso:
# MAGIC
# MAGIC - **Sanitiza os nomes das colunas**, substituindo caracteres inválidos para o formato Delta (espaços por `_`, removendo parênteses e trocando `%` por `pct`);
# MAGIC - **Converte** o DataFrame Pandas em um **Spark DataFrame** (`spark_df_Alimentos_Taco`);
# MAGIC - **Escreve** o DataFrame no formato Delta usando `saveAsTable` com modo `overwrite`, criando a tabela `MVP_ENG_DADOS.Bronze.Alimentos_Taco`;
# MAGIC - Exibe uma mensagem de sucesso e o total de registros inseridos.
# MAGIC
# MAGIC A tabela criada pode ser consultada na próxima célula com um `SELECT` simples.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.1.2.3 - Descrição da Tabela `Alimentos_Taco`
# MAGIC
# MAGIC #### Visão Geral
# MAGIC
# MAGIC | Propriedade | Valor |
# MAGIC |---|---|
# MAGIC | **Catálogo** | `MVP_ENG_DADOS` |
# MAGIC | **Schema** | `Bronze` |
# MAGIC | **Nome da Tabela** | `Alimentos_Taco` |
# MAGIC | **Formato** | Delta |
# MAGIC | **Origem** | `/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/Taco.csv` |
# MAGIC | **Dataset de Referência** | [Kaggle — Composição Nutricional de Alimentos TACO](https://www.kaggle.com/datasets/ispangler/composio-nutricional-de-alimentos-taco) |
# MAGIC
# MAGIC A tabela **Alimentos_Taco** armazena a composição nutricional de alimentos brasileiros baseada na **TACO** (Tabela Brasileira de Composição de Alimentos), desenvolvida pela UNICAMP. Os valores nutricionais referem-se a **100 g ou 100 mL** do alimento.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Dicionário de Dados
# MAGIC
# MAGIC > **Nota:** Os nomes originais das colunas do arquivo CSV foram **sanitizados** para o formato Delta — espaços substituídos por `_`, parênteses removidos e `%` substituído por `pct`.
# MAGIC
# MAGIC | # | Coluna (na tabela) | Coluna (no CSV original) | Descrição | Unidade |
# MAGIC |---|---|---|---|---|
# MAGIC | 1 | `Número` | Número | Código identificador do alimento | — |
# MAGIC | 2 | `Descrição` | Descrição | Nome/descrição do alimento | — |
# MAGIC | 3 | `Umidade_pct` | Umidade (%) | Teor de umidade do alimento | g / 100 g |
# MAGIC | 4 | `Energia_kcal` | Energia (kcal) | Valor energético | kcal / 100 g |
# MAGIC | 5 | `Proteína_g` | Proteína (g) | Quantidade de proteína | g / 100 g |
# MAGIC | 6 | `Lipídeos_g` | Lipídeos (g) | Quantidade de lipídeos (gorduras) | g / 100 g |
# MAGIC | 7 | `Colesterol_mg` | Colesterol (mg) | Quantidade de colesterol | mg / 100 g |
# MAGIC | 8 | `Carboidrato_g` | Carboidrato (g) | Quantidade de carboidratos | g / 100 g |
# MAGIC | 9 | `Fibra_alimentar_g` | Fibra alimentar (g) | Quantidade de fibra alimentar | g / 100 g |
# MAGIC | 10 | `Cinzas_g` | Cinzas (g) | Teor de cinzas (minerais residuais) | g / 100 g |
# MAGIC | 11 | `Cálcio_mg` | Cálcio (mg) | Quantidade de cálcio | mg / 100 g |
# MAGIC | 12 | `Magnésio_mg` | Magnésio (mg) | Quantidade de magnésio | mg / 100 g |
# MAGIC | 13 | `Manganês_mg` | Manganês (mg) | Quantidade de manganês | mg / 100 g |
# MAGIC | 14 | `Fósforo_mg` | Fósforo (mg) | Quantidade de fósforo | mg / 100 g |
# MAGIC | 15 | `Ferro_mg` | Ferro (mg) | Quantidade de ferro | mg / 100 g |
# MAGIC | 16 | `Sódio_mg` | Sódio (mg) | Quantidade de sódio | mg / 100 g |
# MAGIC | 17 | `Potássio_mg` | Potássio (mg) | Quantidade de potássio | mg / 100 g |
# MAGIC | 18 | `Cobre_mg` | Cobre (mg) | Quantidade de cobre | mg / 100 g |
# MAGIC | 19 | `Zinco_mg` | Zinco (mg) | Quantidade de zinco | mg / 100 g |
# MAGIC | 20 | `Retinolo_µg` | Retinolo (µg) | Quantidade de retinol (vitamina A) | µg / 100 g |
# MAGIC | 21 | `RE_µg` | RE (µg) | Equivalente de retinol | µg / 100 g |
# MAGIC | 22 | `RAE_µg` | RAE (µg) | Atividade de equivalência de retinol | µg / 100 g |
# MAGIC | 23 | `Tiamina_mg` | Tiamina (mg) | Quantidade de tiamina (vitamina B1) | mg / 100 g |
# MAGIC | 24 | `Riboflavina_mg` | Riboflavina (mg) | Quantidade de riboflavina (vitamina B2) | mg / 100 g |
# MAGIC | 25 | `Piridoxamina_mg` | Piridoxamina (mg) | Quantidade de piridoxamina (vitamina B6) | mg / 100 g |
# MAGIC | 26 | `Niacina_mg` | Niacina (mg) | Quantidade de niacina (vitamina B3) | mg / 100 g |
# MAGIC | 27 | `Vitamina_C_mg` | Vitamina C (mg) | Quantidade de vitamina C (ácido ascórbico) | mg / 100 g |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Notas
# MAGIC
# MAGIC - A tabela foi criada a partir de um arquivo **CSV** carregado com **Pandas** (`encoding='ISO-8859-1'`, `sep=';'`, `decimal=','`) e posteriormente convertido em **Spark DataFrame** e persistida como **Delta Table**.
# MAGIC - Os valores nutricionais seguem o padrão da **TACO — Tabela Brasileira de Composição de Alimentos**, instrumento de referência para estudos nutricionais no Brasil.
# MAGIC - Os nomes das colunas refletem a sanitização aplicada no momento da criação da tabela (substituição de espaços, parênteses e `%`).
# MAGIC - Para validar os nomes reais das colunas, execute: `DESCRIBE MVP_ENG_DADOS.Bronze.Alimentos_Taco`
# MAGIC

# COMMAND ----------

# DBTITLE 1,Apresenta as informações da tabela Alimentos_Taco
# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM MVP_ENG_DADOS.Bronze.Alimentos_Taco
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.1.2.4 - Resumo da célula (Apresenta as informações da tabela Alimentos_Taco)
# MAGIC
# MAGIC A célula acima executa um `SELECT *` na tabela **Alimentos_Taco**, criada no catálogo `MVP_ENG_DADOS`, schema `Bronze`, limitando o resultado aos **10 primeiros registros**. O objetivo é validar visualmente se os dados carregados a partir do arquivo **Taco.csv** foram persistidos corretamente, exibindo todas as colunas e seus valores para inspeção rápida.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ###4.1.3 - Criação da Tabela Alimentos_Food_Nutrition

# COMMAND ----------

# DBTITLE 1,Carrega arquivo Food_Nutrition.csv
# Carrega arquivo csv usando Pandas
import pandas as pd

# Carrega diretamente do workspace usando o caminho do arquivo
file_path = "/Volumes/mvp_eng_dados/adaptacao/nutri_alimentos/Food_Nutrition.csv"

# Lê o arquivo CSV - ele já tem cabeçalho, então não precisa renomear colunas
Alimentos_Food_Nutrition = pd.read_csv(file_path)

# Pega apenas os dados do dataset e guardando em um array
array = Alimentos_Food_Nutrition.values


# Separa o array em variáveis preditoras (X) e variável target (Y)
X = array[:,0:8]
Y = array[:,0:8]

dafr_Alimentos_Food_Nutrition = pd.DataFrame(data=Alimentos_Food_Nutrition)

# Verificar e imprimir na tela o total de instâncias
print(f"Total de instâncias: {len(Alimentos_Food_Nutrition)}")
print("\nTipos de dados por coluna:")
print(dafr_Alimentos_Food_Nutrition.info())
print("✅ Dataset carregado com sucesso!")
print("\nColunas disponíveis:")
print(dafr_Alimentos_Food_Nutrition.columns.tolist())
print("\nPrimeiras 5 linhas:")
display(dafr_Alimentos_Food_Nutrition.head(5))
print(f"\nTotal de registros: {len(dafr_Alimentos_Food_Nutrition)}")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.1.3.1 - Resumo da célula (Carrega arquivo Food_Nutrition.csv)
# MAGIC
# MAGIC A célula acima carrega o arquivo **Food_Nutrition.csv** a partir de um caminho no Databricks Volumes usando **Pandas**. Em seguida:
# MAGIC
# MAGIC - Extrai os valores para um array e separa as variáveis preditoras (`X`) e a variável target (`Y`);
# MAGIC - Cria um DataFrame Pandas (`dafr_Alimentos_Food_Nutrition`) a partir dos dados carregados;
# MAGIC - Exibe informações sobre o dataset: total de instâncias, tipos de dados, colunas disponíveis e as primeiras 5 linhas.
# MAGIC
# MAGIC Este DataFrame será utilizado na próxima célula para criar a tabela **Alimentos_Food_Nutrition** no catálogo `MVP_ENG_DADOS`, schema `Bronze`.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Criar tabela Alimentos_Food_Nutrition
# Criar tabela Alimentos_Food_Nutrition no catálogo MVP_ENG_DADOS e schema Bronze
# e inserir os dados do dataframe dafr_Alimentos_Food_Nutrition

# Sanitiza nomes de colunas removendo caracteres inválidos para Delta (espaços, parênteses, etc.)
for col_name in list(dafr_Alimentos_Food_Nutrition.columns):
    safe_name = col_name.replace(' ', '_').replace('(', '').replace(')', '').replace('%', 'pct')
    dafr_Alimentos_Food_Nutrition.rename(columns={col_name: safe_name}, inplace=True)

# Converte o dataframe pandas para Spark DataFrame
spark_df_Alimentos_Food_Nutrition = spark.createDataFrame(dafr_Alimentos_Food_Nutrition)

# Escreve o DataFrame no formato Delta como tabela no catálogo especificado
spark_df_Alimentos_Food_Nutrition.write.mode("overwrite").saveAsTable("MVP_ENG_DADOS.Bronze.Alimentos_Food_Nutrition")

print("✅ Tabela Alimentos_Food_Nutrition criada com sucesso no catálogo MVP_ENG_DADOS, schema Bronze!")
print(f"Total de registros inseridos: {spark_df_Alimentos_Food_Nutrition.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.1.3.2 - Resumo da célula (Criar tabela Alimentos_Food_Nutrition)
# MAGIC
# MAGIC A célula acima cria a tabela **Alimentos_Food_Nutrition** no catálogo `MVP_ENG_DADOS`, schema `Bronze`, a partir do DataFrame Pandas `dafr_Alimentos_Food_Nutrition`. Para isso:
# MAGIC
# MAGIC - **Sanitiza os nomes das colunas**, substituindo caracteres inválidos para o formato Delta (espaços por `_`, removendo parênteses e trocando `%` por `pct`);
# MAGIC - **Converte** o DataFrame Pandas em um **Spark DataFrame** (`spark_df_Alimentos_Food_Nutrition`);
# MAGIC - **Escreve** o DataFrame no formato Delta usando `saveAsTable` com modo `overwrite`, criando a tabela `MVP_ENG_DADOS.Bronze.Alimentos_Food_Nutrition`;
# MAGIC - Exibe uma mensagem de sucesso e o total de registros inseridos.
# MAGIC
# MAGIC A tabela criada pode ser consultada na próxima célula com um `SELECT` simples.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.1.3.3 - Descrição da Tabela `Alimentos_Food_Nutrition`
# MAGIC
# MAGIC #### Visão Geral
# MAGIC
# MAGIC | Propriedade | Valor |
# MAGIC |---|---|
# MAGIC | **Catálogo** | `MVP_ENG_DADOS` |
# MAGIC | **Schema** | `Bronze` |
# MAGIC | **Nome da Tabela** | `Alimentos_Food_Nutrition` |
# MAGIC | **Formato** | Delta |
# MAGIC | **Origem** | [Kaggle — USDA - National Nutrient Database](https://www.kaggle.com/datasets/haithemhermessi/usda-national-nutrient-database) |
# MAGIC
# MAGIC A tabela **Alimentos_Food_Nutrition** armazena informações nutricionais detalhadas de diversos alimentos. Os dados incluem valor calórico, macronutrientes (gorduras, carboidratos, proteínas), fibras, colesterol, sódio, água, vitaminas, minerais e densidade nutricional.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Dicionário de Dados
# MAGIC
# MAGIC > **Nota:** As colunas originais do arquivo CSV estavam em **inglês** e foram **renomeadas para português** via `ALTER TABLE ... RENAME COLUMN` após a criação da tabela.
# MAGIC
# MAGIC | # | Coluna (na tabela) | Coluna (no CSV original) | Descrição | Unidade |
# MAGIC |---|---|---|---|---|
# MAGIC | 1 | `Alimento` | food | Nome do alimento | — |
# MAGIC | 2 | `Valor_Calorico` | Caloric_Value | Valor energético do alimento | kcal |
# MAGIC | 3 | `Gordura` | Fat | Quantidade total de gordura | g |
# MAGIC | 4 | `Gorduras_Saturadas` | Saturated_Fats | Quantidade de gorduras saturadas | g |
# MAGIC | 5 | `Gorduras_Monoinsaturadas` | Monounsaturated_Fats | Quantidade de gorduras monoinsaturadas | g |
# MAGIC | 6 | `Gorduras_Poliinsaturadas` | Polyunsaturated_Fats | Quantidade de gorduras poliinsaturadas | g |
# MAGIC | 7 | `Carboidratos` | Carbohydrates | Quantidade total de carboidratos | g |
# MAGIC | 8 | `Acucares` | Sugars | Quantidade de açúcares | g |
# MAGIC | 9 | `Proteina` | Protein | Quantidade de proteína | g |
# MAGIC | 10 | `Fibra_Alimentar` | Dietary_Fiber | Quantidade de fibra alimentar | g |
# MAGIC | 11 | `Colesterol` | Cholesterol | Quantidade de colesterol | mg |
# MAGIC | 12 | `Sodio` | Sodium | Quantidade de sódio | mg |
# MAGIC | 13 | `Agua` | Water | Teor de água | g |
# MAGIC | 14 | `Vitaminas` | Vitamins | Quantidade total de vitaminas | mg |
# MAGIC | 15 | `Calcio` | Calcium | Quantidade de cálcio | mg |
# MAGIC | 16 | `Cobre` | Copper | Quantidade de cobre | mg |
# MAGIC | 17 | `Ferro` | Iron | Quantidade de ferro | mg |
# MAGIC | 18 | `Magnesio` | Magnesium | Quantidade de magnésio | mg |
# MAGIC | 19 | `Manganes` | Manganese | Quantidade de manganês | mg |
# MAGIC | 20 | `Fosforo` | Phosphorus | Quantidade de fósforo | mg |
# MAGIC | 21 | `Potassio` | Potassium | Quantidade de potássio | mg |
# MAGIC | 22 | `Selenio` | Selenium | Quantidade de selênio | µg |
# MAGIC | 23 | `Zinco` | Zinc | Quantidade de zinco | mg |
# MAGIC | 24 | `Densidade_Nutricional` | Nutrition_Density | Densidade nutricional do alimento | — |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Notas
# MAGIC
# MAGIC - A tabela foi criada a partir de um arquivo **CSV** carregado com **Pandas** e posteriormente convertido em **Spark DataFrame** e persistida como **Delta Table**.
# MAGIC - Após a criação, as colunas foram **renomeadas do inglês para o português** utilizando `ALTER TABLE ... RENAME COLUMN`, com a propriedade `delta.columnMapping.mode = 'name'` habilitada.
# MAGIC - Para validar os nomes reais das colunas, execute: `DESCRIBE MVP_ENG_DADOS.Bronze.Alimentos_Food_Nutrition`
# MAGIC

# COMMAND ----------

# DBTITLE 1,Renomear colunas para português
# Renomeia as colunas da tabela Alimentos_Food_Nutrition para português
renomeacoes = {
    "food": "Alimento",
    "Caloric_Value": "Valor_Calorico",
    "Fat": "Gordura",
    "Saturated_Fats": "Gorduras_Saturadas",
    "Monounsaturated_Fats": "Gorduras_Monoinsaturadas",
    "Polyunsaturated_Fats": "Gorduras_Poliinsaturadas",
    "Carbohydrates": "Carboidratos",
    "Sugars": "Acucares",
    "Protein": "Proteina",
    "Dietary_Fiber": "Fibra_Alimentar",
    "Cholesterol": "Colesterol",
    "Sodium": "Sodio",
    "Water": "Agua",
    "Vitamins": "Vitaminas",
    "Calcium": "Calcio",
    "Copper": "Cobre",
    "Iron": "Ferro",
    "Magnesium": "Magnesio",
    "Manganese": "Manganes",
    "Phosphorus": "Fosforo",
    "Potassium": "Potassio",
    "Selenium": "Selenio",
    "Zinc": "Zinco",
    "Nutrition_Density": "Densidade_Nutricional",
}

spark.sql("ALTER TABLE MVP_ENG_DADOS.Bronze.Alimentos_Food_Nutrition SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name')")

for nome_ingles, nome_portugues in renomeacoes.items():
    spark.sql(f"ALTER TABLE MVP_ENG_DADOS.Bronze.Alimentos_Food_Nutrition RENAME COLUMN {nome_ingles} TO {nome_portugues}")

print(f"✅ {len(renomeacoes)} colunas renomeadas para português com sucesso!")
print("\nNovos nomes das colunas:")
for nome_portugues in renomeacoes.values():
    print(f"  - {nome_portugues}")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.1.3.4 - Resumo da célula (Renomear colunas para português)
# MAGIC
# MAGIC A célula acima renomeia as colunas da tabela **Alimentos_Food_Nutrition** do inglês para o português. Para isso:
# MAGIC
# MAGIC - Habilita a propriedade `delta.columnMapping.mode = 'name'` na tabela, necessária para renomear colunas em tabelas Delta;
# MAGIC - Percorre um dicionário de mapeamento (`renomeacoes`) com **24 colunas**, executando `ALTER TABLE ... RENAME COLUMN` para cada par inglês → português;
# MAGIC - Exibe uma mensagem de sucesso e lista os novos nomes das colunas.
# MAGIC
# MAGIC Após essa etapa, a tabela passa a ter todas as colunas em português, facilitando a consulta e o entendimento dos dados.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.1.4 - Evidência da Criação da Camada Bronze
# MAGIC
# MAGIC ![image_1790215863984.png](./image_1790215863984.png "image_1790215863984.png")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## 4.2 - Camada Silver (Qualidade de Dados)
# MAGIC
# MAGIC A **Camada Silver** é o pilar central da **qualidade de dados** na arquitetura medalhão. Recebe os dados brutos persistidos na camada **Bronze** e aplica transformações sistemáticas de **padronização, limpeza e auditoria**, garantindo que apenas dados confiáveis e consistentes avancem para consumo analítico.
# MAGIC
# MAGIC ### Foco em Qualidade de Dados
# MAGIC
# MAGIC A qualidade dos dados é tratada nesta camada como uma responsabilidade primária, não como uma etapa acessória. Cada transformação aplicada tem como objetivo eliminar ambiguidades, padronizar nomenclaturas e detectar inconsistências antes que os dados cheguem à camada Gold ou a qualquer consumidor analítico. As ações de qualidade executadas incluem:
# MAGIC
# MAGIC | # | Etapa | Ação de Qualidade de Dados |
# MAGIC |---|---|---|
# MAGIC | 1 | **Seleção do catálogo e schema** | Define `MVP_ENG_DADOS` como catálogo ativo e `silver` como schema padrão, garantindo isolamento e governança dos dados tratados. |
# MAGIC | 2 | **Leitura da tabela Bronze** | Carrega a tabela `MVP_ENG_DADOS.bronze.alimentos_food_nutrition` em um DataFrame Spark, ponto de partida para as transformações de qualidade. |
# MAGIC | 3 | **Renomeação de colunas** | Traduz os nomes das colunas do inglês para o português, padronizando a nomenclatura para消除 ambiguidades e facilitar a leitura, auditoria e o uso dos dados. |
# MAGIC | 4 | **Gravação na camada Silver** | Persiste o DataFrame transformado na tabela `MVP_ENG_DADOS.silver.food_nutrition_silver` no formato Delta, com sobrescrita de esquema (`overwriteSchema = true`), garantindo reprodutibilidade e consistência estrutural. |
# MAGIC | 5 | **Verificação de qualidade** | Executa auditoria abrangente de **campos em branco** (nulos ou strings vazias) em **todas as colunas** da tabela Silver, identificando possíveis inconsistências e fornecendo visibilidade sobre a integridade dos dados. |
# MAGIC
# MAGIC ### O que foi feito nesta seção
# MAGIC
# MAGIC - **Padronização de nomenclatura:** Todos os nomes de colunas foram traduzidos do inglês para o português, eliminando barreiras de idioma e tornando o dicionário de dados mais acessível.
# MAGIC - **Persistência controlada:** A gravação em formato Delta com sobrescrita de esquema garante que cada execução produza um estado limpo e previsível da tabela Silver.
# MAGIC - **Auditoria de campos nulos e vazios:** Foi executada uma query SQL que contabiliza, coluna por coluna, a quantidade de registros em branco (nulos ou strings vazias), transformando o resultado em formato longo via `UNPIVOT` e filtrando apenas as colunas com inconsistências (`qtd_em_branco > 0`), ordenadas por severidade.
# MAGIC - **Rastreabilidade:** Cada etapa é acompanhada de células explicativas que documentam as decisões de transformação, garantindo transparência e reprodutibilidade do pipeline de qualidade.
# MAGIC
# MAGIC > **Resumo:** A camada Silver transforma dados brutos em dados confiáveis, aplicando padronização de nomenclatura, persistência estruturada em Delta e auditoria sistemática de campos em branco — assegurando que apenas dados de qualidade comprovada estejam disponíveis para as camadas e consumidores subsequentes.
# MAGIC
# MAGIC ---
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.2.1 - Utilização de Catálogo e Schema

# COMMAND ----------

# DBTITLE 1,Utiliza o Catálogo MVP_ENG_DADOS e Schema Silver
spark.sql("USE CATALOG MVP_ENG_DADOS")
spark.sql("USE SCHEMA silver")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 4.2.1.1 - Explicação da Célula — Utiliza o Catálogo MVP_ENG_DADOS e Schema Silver
# MAGIC
# MAGIC Esta célula define o contexto de trabalho no Databricks, executando dois comandos Spark SQL:
# MAGIC
# MAGIC 1. **`USE CATALOG MVP_ENG_DADOS`** — Seleciona o catálogo `MVP_ENG_DADOS` como catálogo ativo, de modo que todas as operações subsequentes (criação de tabelas, consultas, etc.) utilizem esse catálogo por padrão.
# MAGIC
# MAGIC 2. **`USE SCHEMA silver`** — Seleciona o schema `silver` dentro do catálogo ativo, definindo-o como schema padrão para as próximas operações.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é configurar o catálogo e o schema padrão (`MVP_ENG_DADOS.silver`) para que as células seguintes possam criar e acessar tabelas sem precisar qualificar totalmente os nomes em cada comando.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.2.2 - Tabela - alimentos_food_nutrition

# COMMAND ----------

# DBTITLE 1,Renomeação de colunas para português
# Carregar a tabela alimentos_food_nutrition em um DataFrame
df_alimentos = spark.table("MVP_ENG_DADOS.bronze.alimentos_food_nutrition")

# Exibir os nomes atuais das colunas para referência
print("Colunas originais:", df_alimentos.columns)

# Dicionário de mapeamento: nome original -> nome em português
# (Ajuste os nomes conforme necessário após visualizar as colunas reais)
renomear_colunas = {
    "food": "alimento",
    "Caloric_Value": "valor_calorico",
    "Protein": "proteina",
    "Carbohydrates": "carboidratos",
    "Fat": "gordura",
    "Saturated_Fats": "gordura_saturada",
    "Monounsaturated_Fats": "gordura_monoinsaturada",
    "Polyunsaturated_Fats": "gordura_poliinsaturada",
    "Sugars": "acucares",
    "Dietary_Fiber":"fibras_alimentar",
    "Cholesterol": "colesterol",
    "Sodium": "sodio",
    "Water": "agua",
    "Vitamin A": "vitamina_a",
    "Vitamin B11": "vitamina_b11",
    "Vitamin B12": "vitamina_b12",
    "Vitamin B1": "vitamina_b1",
    "Vitamin B2": "vitamina_b2",
    "Vitamin B3": "vitamina_b3",
    "Vitamin B5": "vitamina_b5",
    "Vitamin B6": "vitamina_b6",
    "Vitamin B7": "vitamina_b7",
    "Vitamin B9": "vitamina_b9",
    "Vitamin C": "vitamina_c",
    "Vitamin D": "vitamina_d",
    "Vitamin E": "vitamina_e",
    "Vitamin K": "vitamina_k",
    "Calcium": "calcio",
    "Copper": "cobre",
    "Iron": "ferro",
    "Magnesium": "magnesio",
    "Manganese": "manganes",
    "Phosphorus": "fosforo",
    "Potassium": "potassio",
    "Selenium": "selnio",
    "Zinc": "zinco",
    "Nutrition_Density": "densidade_nutritiva",
}

# Aplicar a renomeação das colunas
for nome_original, nome_pt in renomear_colunas.items():
    if nome_original in df_alimentos.columns:
        df_alimentos = df_alimentos.withColumnRenamed(nome_original, nome_pt)

# Exibir o esquema atualizado e os primeiros registros
df_alimentos.printSchema()
display(df_alimentos.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC #### 4.2.2.1 - Explicação da Célula — Renomeação de colunas para português
# MAGIC
# MAGIC Esta célula realiza as seguintes etapas:
# MAGIC
# MAGIC 1. **Carrega a tabela bronze** `MVP_ENG_DADOS.bronze.alimentos_food_nutrition` em um DataFrame Spark (`df_alimentos`).
# MAGIC
# MAGIC 2. **Exibe os nomes originais das colunas** (`print`) para que o desenvolvedor confirme os nomes antes de renomear.
# MAGIC
# MAGIC 3. **Define um dicionário de mapeamento** (`renomear_colunas`) que relaciona cada nome original em inglês (ex.: `"food"`, `"Caloric_Value"`, `"Protein"`) ao seu equivalente em português (ex.: `"alimento"`, `"valor_calorico"`, `"proteina"`).
# MAGIC
# MAGIC 4. **Renomeia as colunas** percorrendo o dicionário com `withColumnRenamed`. Para cada par, o código verifica se o nome original existe no DataFrame antes de aplicar a renomeação, evitando erros caso alguma coluna não esteja presente.
# MAGIC
# MAGIC 5. **Exibe o esquema atualizado** (`printSchema`) e os **10 primeiros registros** (`display(df_alimentos.limit(10))`) para confirmar que a transformação foi aplicada corretamente.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é padronizar os nomes das colunas da tabela de alimentos, traduzindo-os do inglês para o português, facilitando a leitura e o uso nos próximos passos do notebook.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Gravação na camada Silver
# Escrever o DataFrame transformado na tabela silver.food_nutrition_silver
(df_alimentos.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("MVP_ENG_DADOS.silver.food_nutrition_silver"))

print("Tabela 'MVP_ENG_DADOS.silver.food_nutrition_silver' criada com sucesso!")

# Verificar os dados gravados
display(spark.table("MVP_ENG_DADOS.silver.food_nutrition_silver").limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC #### 4.2.2.2 - Explicação da Célula — Gravação na camada Silver
# MAGIC
# MAGIC Esta célula realiza as seguintes etapas:
# MAGIC
# MAGIC 1. **Grava o DataFrame transformado** (`df_alimentos`, que teve suas colunas renomeadas para português na célula anterior) em uma tabela Delta na camada silver, no caminho completo `MVP_ENG_DADOS.silver.food_nutrition_silver`.
# MAGIC
# MAGIC 2. **Utiliza `mode("overwrite")`** para sobrescrever a tabela caso ela já exista — toda execução recria a tabela do zero com os dados mais recentes do DataFrame.
# MAGIC
# MAGIC 3. **Utiliza `option("overwriteSchema", "true")`** para permitir que o esquema (nomes e tipos de colunas) seja sobrescrito junto com os dados. Isso evita erros quando o esquema do DataFrame diverge do esquema existente na tabela (por exemplo, após renomear colunas).
# MAGIC
# MAGIC 4. **Exibe uma mensagem de sucesso** confirmando que a tabela foi criada.
# MAGIC
# MAGIC 5. **Verifica os dados gravados** executando `spark.table(...).limit(10)` dentro de `display(...)`, que mostra os 10 primeiros registros da tabela recém-criada — uma validação visual de que os dados foram persistidos corretamente.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é persistir o resultado da transformação (colunas traduzidas) em uma tabela Delta persistente na camada silver, sobrescrevendo o conteúdo e o esquema anteriores, e em seguida validar visualmente os dados gravados.

# COMMAND ----------

# DBTITLE 1,Verificação de campos em branco na tabela Silver
# MAGIC %sql
# MAGIC -- Verificar campos em branco (nulos ou strings vazias) na tabela silver.food_nutrition_silver
# MAGIC WITH blank_counts AS (
# MAGIC   SELECT
# MAGIC     SUM(CASE WHEN alimento              IS NULL OR TRIM(alimento)              = '' THEN 1 ELSE 0 END) AS alimento,
# MAGIC     SUM(CASE WHEN valor_calorico        IS NULL OR TRIM(CAST(valor_calorico        AS STRING)) = '' THEN 1 ELSE 0 END) AS valor_calorico,
# MAGIC     SUM(CASE WHEN proteina              IS NULL OR TRIM(CAST(proteina              AS STRING)) = '' THEN 1 ELSE 0 END) AS proteina,
# MAGIC     SUM(CASE WHEN carboidratos           IS NULL OR TRIM(CAST(carboidratos           AS STRING)) = '' THEN 1 ELSE 0 END) AS carboidratos,
# MAGIC     SUM(CASE WHEN gordura                IS NULL OR TRIM(CAST(gordura                AS STRING)) = '' THEN 1 ELSE 0 END) AS gordura,
# MAGIC     SUM(CASE WHEN gordura_saturada       IS NULL OR TRIM(CAST(gordura_saturada       AS STRING)) = '' THEN 1 ELSE 0 END) AS gordura_saturada,
# MAGIC     SUM(CASE WHEN gordura_monoinsaturada IS NULL OR TRIM(CAST(gordura_monoinsaturada AS STRING)) = '' THEN 1 ELSE 0 END) AS gordura_monoinsaturada,
# MAGIC     SUM(CASE WHEN gordura_poliinsaturada IS NULL OR TRIM(CAST(gordura_poliinsaturada AS STRING)) = '' THEN 1 ELSE 0 END) AS gordura_poliinsaturada,
# MAGIC     SUM(CASE WHEN acucares               IS NULL OR TRIM(CAST(acucares               AS STRING)) = '' THEN 1 ELSE 0 END) AS acucares,
# MAGIC     SUM(CASE WHEN fibras_alimentar       IS NULL OR TRIM(CAST(fibras_alimentar       AS STRING)) = '' THEN 1 ELSE 0 END) AS fibras_alimentar,
# MAGIC     SUM(CASE WHEN colesterol             IS NULL OR TRIM(CAST(colesterol             AS STRING)) = '' THEN 1 ELSE 0 END) AS colesterol,
# MAGIC     SUM(CASE WHEN sodio                  IS NULL OR TRIM(CAST(sodio                  AS STRING)) = '' THEN 1 ELSE 0 END) AS sodio,
# MAGIC     SUM(CASE WHEN agua                   IS NULL OR TRIM(CAST(agua                   AS STRING)) = '' THEN 1 ELSE 0 END) AS agua,
# MAGIC     SUM(CASE WHEN Vitamins               IS NULL OR TRIM(CAST(Vitamins               AS STRING)) = '' THEN 1 ELSE 0 END) AS Vitamins,
# MAGIC     SUM(CASE WHEN calcio                 IS NULL OR TRIM(CAST(calcio                 AS STRING)) = '' THEN 1 ELSE 0 END) AS calcio,
# MAGIC     SUM(CASE WHEN cobre                    IS NULL OR TRIM(CAST(cobre                    AS STRING)) = '' THEN 1 ELSE 0 END) AS cobre,
# MAGIC     SUM(CASE WHEN ferro                     IS NULL OR TRIM(CAST(ferro                     AS STRING)) = '' THEN 1 ELSE 0 END) AS ferro,
# MAGIC     SUM(CASE WHEN magnesio                  IS NULL OR TRIM(CAST(magnesio                  AS STRING)) = '' THEN 1 ELSE 0 END) AS magnesio,
# MAGIC     SUM(CASE WHEN manganes                  IS NULL OR TRIM(CAST(manganes                  AS STRING)) = '' THEN 1 ELSE 0 END) AS manganes,
# MAGIC     SUM(CASE WHEN fosforo                   IS NULL OR TRIM(CAST(fosforo                   AS STRING)) = '' THEN 1 ELSE 0 END) AS fosforo,
# MAGIC     SUM(CASE WHEN potassio                  IS NULL OR TRIM(CAST(potassio                  AS STRING)) = '' THEN 1 ELSE 0 END) AS potassio,
# MAGIC     SUM(CASE WHEN selnio                    IS NULL OR TRIM(CAST(selnio                    AS STRING)) = '' THEN 1 ELSE 0 END) AS selnio,
# MAGIC     SUM(CASE WHEN zinco                     IS NULL OR TRIM(CAST(zinco                     AS STRING)) = '' THEN 1 ELSE 0 END) AS zinco,
# MAGIC     SUM(CASE WHEN densidade_nutritiva       IS NULL OR TRIM(CAST(densidade_nutritiva       AS STRING)) = '' THEN 1 ELSE 0 END) AS densidade_nutritiva
# MAGIC   FROM MVP_ENG_DADOS.silver.food_nutrition_silver
# MAGIC )
# MAGIC SELECT coluna, qtd_em_branco
# MAGIC FROM blank_counts
# MAGIC UNPIVOT (qtd_em_branco FOR coluna IN (
# MAGIC   alimento, valor_calorico, proteina, carboidratos, gordura, gordura_saturada,
# MAGIC   gordura_monoinsaturada, gordura_poliinsaturada, acucares, fibras_alimentar,
# MAGIC   colesterol, sodio, agua, Vitamins, calcio, cobre, ferro,
# MAGIC   magnesio, manganes, fosforo, potassio, selnio, zinco, densidade_nutritiva
# MAGIC ))
# MAGIC WHERE qtd_em_branco > 0
# MAGIC ORDER BY qtd_em_branco DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.2.3 - Explicação da Célula — Verificação de campos em branco na tabela Silver
# MAGIC
# MAGIC Esta célula SQL realiza uma auditoria de qualidade de dados, verificando **campos em branco (nulos ou strings vazias)** em todas as colunas da tabela `MVP_ENG_DADOS.silver.food_nutrition_silver`. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **CTE `blank_counts`**: Executa um `SELECT` com um `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` para **cada coluna** da tabela. Para cada coluna, a lógica é:
# MAGIC    - Se a coluna for **string** (`alimento`), verifica `IS NULL` ou `TRIM(coluna) = ''` (vazio ou apenas espaços).
# MAGIC    - Se a coluna for **numérica**, faz um `CAST(coluna AS STRING)` e aplica a mesma verificação de `IS NULL` ou `TRIM(...) = ''`.
# MAGIC    - O resultado é a **quantidade de registros em branco** para cada coluna.
# MAGIC
# MAGIC 2. **`UNPIVOT`**: Transforma o resultado de formato largo (uma coluna por métrica) para formato longo, gerando duas colunas: `coluna` (nome da métrica) e `qtd_em_branco` (quantidade de registros em branco).
# MAGIC
# MAGIC 3. **Filtro `WHERE qtd_em_branco > 0`**: Exibe apenas as colunas que possuem **pelo menos um** campo em branco, ignorando as colunas totalmente preenchidas.
# MAGIC
# MAGIC 4. **`ORDER BY qtd_em_branco DESC`**: Ordena as colunas daquela com mais campos em branco para a que tem menos.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é identificar quais colunas da tabela silver possuem dados faltantes (nulos ou vazios) e quantos registros afetados há em cada uma, ordenando da mais problemática para a menos problemática. Essa auditoria orienta os tratamentos de limpeza que serão aplicados nas células seguintes (ex.: substituir nulos por `0` ou por string vazia).
# MAGIC
# MAGIC > **Observação:** A coluna `Vitamins` aparece com nome em inglês, indicando que ela não foi renomeada na célula de tradução (não estava no dicionário `renomear_colunas`).

# COMMAND ----------

# DBTITLE 1,Verificação de valores negativos na tabela Silver
# Verificar se tem valores negativos na tabela silver.food_nutrition_silver

from pyspark.sql.functions import col
from pyspark.sql import functions as F

df = spark.table("MVP_ENG_DADOS.silver.food_nutrition_silver")

# Identificar colunas numéricas
colunas_numericas = [c for c in df.columns if df.schema[c].dataType.typeName() in ("int", "bigint", "long", "short", "byte", "float", "double", "decimal")]

# Construir contagem de valores negativos por coluna
neg_counts = df.select([
    (col(c) < 0).cast("int").alias(c) for c in colunas_numericas
]).agg(*[F.sum(c).alias(c) for c in colunas_numericas])

# Transformar em formato longo (coluna, qtd_negativos)
null_counts = neg_counts.collect()[0]
rows = [(c, null_counts[c]) for c in colunas_numericas]

df_neg = spark.createDataFrame(rows, ["coluna", "qtd_negativos"])
df_neg = df_neg.filter("qtd_negativos > 0").orderBy(df_neg["qtd_negativos"].desc())

print("Colunas com valores negativos:")
display(df_neg)

if df_neg.count() == 0:
    print("\nNenhum valor negativo encontrado na tabela!")
else:
    print(f"\nTotal de colunas com valores negativos: {df_neg.count()}")
    # Exibir amostra dos registros com valores negativos
    for c in colunas_numericas:
        if null_counts[c] > 0:
            print(f"\nAmostra de registros negativos na coluna '{c}':")
            display(df.filter(col(c) < 0).select("alimento", c).limit(10))
            break

# COMMAND ----------

# MAGIC %md
# MAGIC #### 4.2.2.4 - Explicação da Célula — Verificação de valores negativos na tabela Silver
# MAGIC
# MAGIC Esta célula Python realiza uma auditoria de qualidade de dados que identifica **valores negativos** em todas as colunas numéricas da tabela `MVP_ENG_DADOS.silver.food_nutrition_silver`. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Carrega a tabela silver** em um DataFrame Spark (`df`) usando `spark.table("MVP_ENG_DADOS.silver.food_nutrition_silver")`.
# MAGIC
# MAGIC 2. **Importa funções necessárias** (`col` e `functions as F`) do módulo `pyspark.sql.functions`.
# MAGIC
# MAGIC 3. **Identifica colunas numéricas** percorrendo todas as colunas do DataFrame e selecionando apenas aquelas cujo tipo de dado é numérico (`int`, `bigint`, `long`, `short`, `byte`, `float`, `double` ou `decimal`). Isso garante que apenas colunas onde faz sentido verificar negatividade sejam avaliadas.
# MAGIC
# MAGIC 4. **Constrói a contagem de valores negativos por coluna**:
# MAGIC    - Para cada coluna numérica, cria uma expressão `(col(c) < 0).cast("int")`, que retorna `1` quando o valor é negativo e `0` caso contrário.
# MAGIC    - Em seguida, aplica `F.sum(c)` sobre todas essas expressões, gerando o total de registros negativos em cada coluna.
# MAGIC
# MAGIC 5. **Transforma o resultado em formato longo**: coleta os resultados (`collect()[0]`), cria uma lista de tuplas `(nome_coluna, qtd_negativos)` e monta um novo DataFrame (`df_neg`) com as colunas `coluna` e `qtd_negativos`.
# MAGIC
# MAGIC 6. **Filtra e ordena**: mantém apenas as colunas com `qtd_negativos > 0` (ou seja, que possuem pelo menos um valor negativo) e ordena daquela com mais negativos para a que tem menos.
# MAGIC
# MAGIC 7. **Exibe os resultados**:
# MAGIC    - Mostra o DataFrame `df_neg` com as colunas que contêm valores negativos.
# MAGIC    - Se nenhuma coluna tiver valores negativos, imprime uma mensagem confirmando que a tabela está limpa.
# MAGIC    - Caso contrário, informa o total de colunas afetadas e exibe uma **amostra de até 10 registros** da primeira coluna com valores negativos (mostrando as colunas `alimento` e a coluna problemática), para inspeção visual.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é auditar a tabela silver em busca de valores negativos — que em colunas nutricionais geralmente indicam erro de dados ou problema de ingestão — identificando quais colunas são afetadas, quantos registros há em cada uma e exibindo exemplos para investigação. Essa verificação orienta eventuais tratamentos de correção nas células seguintes.

# COMMAND ----------

# DBTITLE 1,Seleção de colunas e gravação da tabela final
# Selecionar somente as colunas necessárias para responder às 10 questões
# e gravar em uma nova tabela silver.food_nutrition_final

from pyspark.sql.functions import col

df_alimentos = spark.table("MVP_ENG_DADOS.silver.food_nutrition_silver")

# Colunas selecionadas conforme as análises:
#  1. Melhor relação proteína por caloria          -> proteina, valor_calorico
#  2. Itens mais ricos em fibras por porção        -> fibras_alimentar, valor_calorico
#  3. Maior densidade nutricional                   -> densidade_nutritiva, valor_calorico
#  4. Menor teor de sódio                           -> sodio, valor_calorico
#  5. Mais adequados para dietas low-carb           -> carboidratos, proteina, gordura, valor_calorico
#  6. Maior quantidade de gorduras saturadas         -> gordura_saturada, gordura, valor_calorico
#  7. Mais indicados para ganho de massa muscular   -> proteina, carboidratos, gordura, valor_calorico
#  8. Mais eficientes para saciedade com poucas calorias -> proteina, fibras_alimentar, valor_calorico
#  9. Maior quantidade de açúcar adicionado         -> acucares, carboidratos, valor_calorico
# 10. Mais adequados para dietas veganas/vegetarianas -> proteina, fibras_alimentar, colesterol, gordura_saturada

colunas_selecionadas = [
    "alimento",
    "valor_calorico",
    "proteina",
    "carboidratos",
    "gordura",
    "gordura_saturada",
    "fibras_alimentar",
    "colesterol",
    "sodio",
    "acucares",
    "densidade_nutritiva",
]

df_final = df_alimentos.select([col(c) for c in colunas_selecionadas])

# Gravar na nova tabela silver.food_nutrition_final
(df_final.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("MVP_ENG_DADOS.silver.food_nutrition_final"))

print("Tabela 'MVP_ENG_DADOS.silver.food_nutrition_final' criada com sucesso!")
print(f"Colunas selecionadas: {df_final.columns}")
print(f"Total de linhas: {df_final.count()}")

# Verificar os dados gravados
display(spark.table("MVP_ENG_DADOS.silver.food_nutrition_final").limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.2.5 - Explicação da Célula — Seleção de colunas e gravação da tabela final
# MAGIC
# MAGIC Esta célula Python realiza a seleção de um subconjunto de colunas da tabela `MVP_ENG_DADOS.silver.food_nutrition_silver` e grava o resultado em uma nova tabela `MVP_ENG_DADOS.silver.food_nutrition_final`. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Carrega a tabela silver** em um DataFrame Spark (`df_alimentos`) usando `spark.table("MVP_ENG_DADOS.silver.food_nutrition_silver")`.
# MAGIC
# MAGIC 2. **Define a lista de colunas selecionadas** (`colunas_selecionadas`) com 11 colunas: `alimento`, `valor_calorico`, `proteina`, `carboidratos`, `gordura`, `gordura_saturada`, `fibras_alimentar`, `colesterol`, `sodio`, `acucares` e `densidade_nutritiva`. Essas colunas foram escolhidas com base nas **10 questões analíticas** que o projeto se propõe a responder, conforme os comentários no código:
# MAGIC    - **Q1** — Melhor relação proteína por caloria → `proteina`, `valor_calorico`
# MAGIC    - **Q2** — Itens mais ricos em fibras por porção → `fibras_alimentar`, `valor_calorico`
# MAGIC    - **Q3** — Maior densidade nutricional → `densidade_nutritiva`, `valor_calorico`
# MAGIC    - **Q4** — Maior teor de sódio → `sodio`, `valor_calorico`
# MAGIC    - **Q5** — Mais adequados para dietas low-carb → `carboidratos`, `proteina`, `gordura`, `valor_calorico`
# MAGIC    - **Q6** — Maior quantidade de gorduras saturadas → `gordura_saturada`, `gordura`, `valor_calorico`
# MAGIC    - **Q7** — Mais indicados para ganho de massa muscular → `proteina`, `carboidratos`, `gordura`, `valor_calorico`
# MAGIC    - **Q8** — Mais eficientes para saciedade com poucas calorias → `proteina`, `fibras_alimentar`, `valor_calorico`
# MAGIC    - **Q9** — Maior quantidade de açúcar → `acucares`, `carboidratos`, `valor_calorico`
# MAGIC    - **Q10** — Mais adequados para dietas veganas/vegetarianas → `proteina`, `fibras_alimentar`, `colesterol`, `gordura_saturada`
# MAGIC
# MAGIC 3. **Seleciona apenas as colunas desejadas** usando `df_alimentos.select([col(c) for c in colunas_selecionadas])`, criando um novo DataFrame `df_final` que contém apenas as colunas relevantes para as análises.
# MAGIC
# MAGIC 4. **Grava o DataFrame resultante** em uma nova tabela Delta chamada `MVP_ENG_DADOS.silver.food_nutrition_final`, utilizando `mode("overwrite")` (sobrescreve a tabela caso já exista) e `option("overwriteSchema", "true")` (permite sobrescrever o esquema junto com os dados).
# MAGIC
# MAGIC 5. **Exibe mensagens de confirmação** com o nome da tabela criada, a lista de colunas selecionadas e o total de linhas.
# MAGIC
# MAGIC 6. **Verifica os dados gravados** exibindo os 10 primeiros registros da nova tabela via `display(spark.table(...).limit(10))`.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é criar uma tabela silver enxuta (`food_nutrition_final`) contendo apenas as colunas necessárias para responder às 10 questões analíticas do projeto, eliminando colunas irrelevantes e reduzindo o escopo dos dados para as análises subsequentes.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.2.6 - Descrição da Tabela e Dicionário de Dados
# MAGIC
# MAGIC ### `MVP_ENG_DADOS.silver.food_nutrition_final`
# MAGIC
# MAGIC **Descrição:** Tabela da camada silver contendo um subconjunto de colunas nutricionais selecionadas para responder às 10 questões analíticas do projeto. Os dados provêm da tabela `MVP_ENG_DADOS.silver.food_nutrition_silver`, que foi derivada da camada bronze após renomeação de colunas para português e tratamento de qualidade (nulos, valores em branco e valores negativos).
# MAGIC
# MAGIC | # | Coluna | Tipo | Descrição |
# MAGIC |---|--------|------|----------|
# MAGIC | 1 | `alimento` | string | Nome do alimento (chave descritiva — identifica o item alimentício) |
# MAGIC | 2 | `valor_calorico` | double | Valor calórico do alimento, expresso em quilocalorias (kcal) |
# MAGIC | 3 | `proteina` | double | Quantidade de proteína, expressa em gramas (g) |
# MAGIC | 4 | `carboidratos` | double | Quantidade de carboidratos, expressa em gramas (g) |
# MAGIC | 5 | `gordura` | double | Quantidade total de gordura (lipídios), expressa em gramas (g) |
# MAGIC | 6 | `gordura_saturada` | double | Quantidade de gordura saturada, expressa em gramas (g) |
# MAGIC | 7 | `fibras_alimentar` | double | Quantidade de fibras alimentares, expressa em gramas (g) |
# MAGIC | 8 | `colesterol` | double | Quantidade de colesterol, expressa em miligramas (mg) |
# MAGIC | 9 | `sodio` | double | Quantidade de sódio, expressa em miligramas (mg) |
# MAGIC | 10 | `acucares` | double | Quantidade de açúcares, expressa em gramas (g) |
# MAGIC | 11 | `densidade_nutritiva` | double | Densidade nutricional calculada — métrica que relaciona o valor nutritivo do alimento ao seu valor calórico |
# MAGIC
# MAGIC > **Origem dos dados:** `MVP_ENG_DADOS.bronze.food_nutrition` → `MVP_ENG_DADOS.silver.food_nutrition_silver` → `MVP_ENG_DADOS.silver.food_nutrition_final`
# MAGIC >
# MAGIC > **Formato de armazenamento:** Delta Lake (Unity Catalog — schema `silver`)
# MAGIC >
# MAGIC > **Modo de gravação:** `overwrite` com `overwriteSchema = true` (recriada a cada execução)
# MAGIC >
# MAGIC > **Granularidade:** Um registro por alimento
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.2.3 - Tabela - alimentos_taco

# COMMAND ----------

# DBTITLE 1,Leitura da tabela bronze alimentos_taco
# Criar um dataframe com dados da tabela alimentos_taco do schema bronze
df_alimentos_taco = spark.table("MVP_ENG_DADOS.bronze.alimentos_taco")

display(df_alimentos_taco.limit(10))


# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.1 - Explicação da Célula — Leitura da tabela bronze `alimentos_taco`
# MAGIC
# MAGIC Esta célula Python é muito simples e tem como objetivo **carregar os dados da tabela `alimentos_taco`** do schema `bronze` (`MVP_ENG_DADOS.bronze.alimentos_taco`) em um DataFrame Spark e exibir uma amostra dos dados. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Carrega a tabela bronze** em um DataFrame Spark (`df_alimentos_taco`) usando `spark.table("MVP_ENG_DADOS.bronze.alimentos_taco")`. Essa função lê a tabela Delta já registrada no catálogo do Unity Catalog e a disponibiliza para manipulação no PySpark.
# MAGIC
# MAGIC 2. **Exibe os 10 primeiros registros** da tabela usando `display(df_alimentos_taco.limit(10))`, permitindo uma inspeção visual rápida do conteúdo e da estrutura dos dados (nomes de colunas, tipos de dados, valores de exemplo).
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é carregar a segunda fonte de dados do projeto — a tabela `alimentos_taco` da camada bronze — e visualizar uma amostra dos seus registros. Esses dados serão tratados e gravados na camada silver nas células seguintes (Célula 14 grava em `silver.alimentos_taco_silver`).
# MAGIC

# COMMAND ----------

# DBTITLE 1,Gravação da tabela silver alimentos_taco_silver
# Escrever o DataFrame df_alimentos_taco na tabela silver.alimentos_taco_silver
(df_alimentos_taco.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("MVP_ENG_DADOS.silver.alimentos_taco_silver"))

print("Tabela 'MVP_ENG_DADOS.silver.alimentos_taco_silver' criada com sucesso!")

# Verificar os dados gravados
display(spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver").limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.2 - Explicação da Célula — Gravação da tabela silver `alimentos_taco_silver`
# MAGIC
# MAGIC Esta célula Python pega o DataFrame `df_alimentos_taco` — carregado na célula anterior a partir da tabela bronze `MVP_ENG_DADOS.bronze.alimentos_taco` — e o grava na camada silver como uma nova tabela Delta chamada `MVP_ENG_DADOS.silver.alimentos_taco_silver`. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Grava o DataFrame na tabela silver** utilizando a API `write` do Spark:
# MAGIC    - `.mode("overwrite")` — sobrescreve a tabela caso ela já exista, garantindo idempotência.
# MAGIC    - `.option("overwriteSchema", "true")` — permite que o esquema (nomes e tipos de colunas) seja sobrescrito junto com os dados, útil caso a estrutura da tabela bronze tenha mudado.
# MAGIC    - `.saveAsTable("MVP_ENG_DADOS.silver.alimentos_taco_silver")` — cria (ou recria) a tabela Delta no catálogo do Unity Catalog, dentro do schema `silver`.
# MAGIC
# MAGIC 2. **Imprime uma mensagem de confirmação** indicando que a tabela foi criada com sucesso.
# MAGIC
# MAGIC 3. **Verifica os dados gravados** lendo a tabela recém-criada com `spark.table(...)` e exibindo os 10 primeiros registros via `display(...).limit(10)`, permitindo uma inspeção visual rápida de que a gravação ocorreu corretamente.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é promover os dados da tabela `alimentos_taco` da camada bronze para a camada silver, criando uma cópia idêntica em formato Delta no catálogo. Essa tabela silver servirá como base para as próximas etapas de tratamento de qualidade de dados (verificação e substituição de valores nulos, "Tr"/trace e valores negativos) nas células seguintes (Células 16 a 22).
# MAGIC

# COMMAND ----------

# DBTITLE 1,Verificação de valores nulos na tabela alimentos_taco_silver
# Verificar campos nulos em todas as colunas da tabela silver.alimentos_taco_silver
# usando SQL dinâmico gerado a partir do esquema da tabela

df_taco = spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")

colunas = df_taco.columns

# Construir a consulta SQL dinamicamente
# Para colunas do tipo string, também verificamos strings vazias; para demais tipos, apenas IS NULL
select_exprs = []
for col in colunas:
    dtype = dict(df_taco.dtypes)[col]
    if dtype == "string":
        expr = f"SUM(CASE WHEN `{col}` IS NULL OR TRIM(`{col}`) = '' THEN 1 ELSE 0 END) AS `{col}`"
    else:
        expr = f"SUM(CASE WHEN `{col}` IS NULL THEN 1 ELSE 0 END) AS `{col}`"
    select_exprs.append(expr)

sql_query = f"""
SELECT {', '.join(select_exprs)}
FROM MVP_ENG_DADOS.silver.alimentos_taco_silver
"""

# Executar e transformar em formato longo (coluna, qtd_nulos)
result = spark.sql(sql_query)

# Unpivot usando PySpark (stack approach)
from pyspark.sql.functions import lit, col
from pyspark.sql import Row

null_counts = result.collect()[0]
rows = [(c, null_counts[c]) for c in colunas]

df_nulls = spark.createDataFrame(rows, ["coluna", "qtd_nulos"])
df_nulls = df_nulls.filter("qtd_nulos > 0").orderBy(df_nulls["qtd_nulos"].desc())

print("Colunas com valores nulos ou em branco:")
display(df_nulls)

if df_nulls.count() == 0:
    print("\nNenhum campo nulo ou em branco encontrado!")


# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC
# MAGIC #### 4.2.3.3 - Explicação da Célula — Verificação de valores nulos na tabela `alimentos_taco_silver`
# MAGIC
# MAGIC Esta célula Python realiza uma auditoria de **qualidade de dados** sobre a tabela `MVP_ENG_DADOS.silver.alimentos_taco_silver`, identificando quantos valores nulos ou em branco existem em cada coluna. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Carrega a tabela silver** em um DataFrame Spark (`df_taco`) usando `spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")`.
# MAGIC
# MAGIC 2. **Obtém a lista de colunas** da tabela (`df_taco.columns`) e, para cada coluna, constrói uma expressão SQL condicional que conta registros nulos:
# MAGIC    - Para colunas do tipo **string**: conta tanto `NULL` quanto strings vazias (`TRIM(col) = ''`).
# MAGIC    - Para colunas de **outros tipos** (numéricos, etc.): conta apenas `IS NULL`.
# MAGIC
# MAGIC 3. **Monta uma consulta SQL dinâmica** unindo todas as expressões com `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` e a executa com `spark.sql(...)`, produzindo uma única linha onde cada coluna contém a quantidade de nulos encontrada.
# MAGIC
# MAGIC 4. **Transforma o resultado em formato longo** (unpivot): converte a linha de contagens em um DataFrame com duas colunas — `coluna` (nome da coluna) e `qtd_nulos` (quantidade de nulos) — e filtra para exibir apenas as colunas que possuem ao menos um valor nulo (`qtd_nulos > 0`), ordenadas em ordem decrescente.
# MAGIC
# MAGIC 5. **Exibe o resultado** com `display(df_nulls)`. Se nenhuma coluna tiver valores nulos, imprime a mensagem "Nenhum campo nulo ou em branco encontrado!".
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é diagnosticar a presença de valores nulos ou em branco em cada coluna da tabela silver `alimentos_taco_silver`, gerando um relatório que orientará o tratamento de dados na célula seguinte (Célula 20), onde os valores nulos, em branco e "Tr" (trace) serão substituídos por valores válidos.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Tratamento de valores nulos ou em branco na tabela food_nutrition_silver
# Alterar os valores nulos ou em branco para valores válidos na tabela silver.food_nutrition_silver

from pyspark.sql.functions import col, when, trim, lit

df_alimentos = spark.table("MVP_ENG_DADOS.silver.food_nutrition_silver")

# Tratar cada coluna conforme o tipo de dado
for nome_coluna in df_alimentos.columns:
    dtype = df_alimentos.schema[nome_coluna].dataType
    tipo = dtype.typeName()

    if tipo == "string":
        # Strings: substituir NULL e strings vazias/whitespace por ""
        df_alimentos = df_alimentos.withColumn(
            nome_coluna,
            when(col(nome_coluna).isNull() | (trim(col(nome_coluna)) == ""), lit("")).otherwise(col(nome_coluna))
        )
    elif tipo in ("int", "bigint", "long", "short", "byte", "float", "double", "decimal"):
        # Numéricos: substituir NULL por 0
        df_alimentos = df_alimentos.fillna({nome_coluna: 0})
    else:
        # Outros tipos: apenas registrar (poderia tratar boolean, date, etc.)
        print(f"Coluna '{nome_coluna}' do tipo '{tipo}' não tratada automaticamente.")

# Sobrescrever a tabela silver com os valores tratados
(df_alimentos.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("MVP_ENG_DADOS.silver.food_nutrition_silver"))

print("Valores nulos ou em branco substituídos com sucesso na tabela 'MVP_ENG_DADOS.silver.food_nutrition_silver'!")

# Verificar o resultado
print("\nAmostra dos dados tratados:")
display(spark.table("MVP_ENG_DADOS.silver.food_nutrition_silver").limit(10))


# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.4 - Explicação da Célula — Tratamento de valores nulos ou em branco na tabela `food_nutrition_silver`
# MAGIC
# MAGIC Esta célula Python realiza a **limpeza de dados** na tabela `MVP_ENG_DADOS.silver.food_nutrition_silver`, substituindo valores nulos (`NULL`) e strings vazias/whitespace por valores válidos, e em seguida sobrescreve a tabela com os dados tratados. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Importa funções do PySpark** necessárias para o tratamento: `col`, `when`, `trim`, `lit`.
# MAGIC
# MAGIC 2. **Carrega a tabela silver** em um DataFrame Spark (`df_alimentos`) usando `spark.table("MVP_ENG_DADOS.silver.food_nutrition_silver")`.
# MAGIC
# MAGIC 3. **Itera sobre todas as colunas** do DataFrame, aplicando tratamento específico conforme o tipo de dado de cada coluna:
# MAGIC    - **Colunas do tipo string**: utiliza `when` + `isNull` + `trim` para substituir `NULL` e strings vazias/whitespace por uma string vazia (`lit("")`).
# MAGIC    - **Colunas numéricas** (`int`, `bigint`, `long`, `short`, `byte`, `float`, `double`, `decimal`): utiliza `fillna({nome_coluna: 0})` para substituir `NULL` por zero.
# MAGIC    - **Outros tipos** (boolean, date, etc.): apenas imprime uma mensagem informando que a coluna não foi tratada automaticamente.
# MAGIC
# MAGIC 4. **Sobrescreve a tabela silver** com os dados tratados utilizando a API `write` do Spark:
# MAGIC    - `.mode("overwrite")` — sobrescreve a tabela caso já exista.
# MAGIC    - `.option("overwriteSchema", "true")` — permite que o esquema seja sobrescrito junto com os dados.
# MAGIC    - `.saveAsTable("MVP_ENG_DADOS.silver.food_nutrition_silver")` — grava o resultado na mesma tabela silver.
# MAGIC
# MAGIC 5. **Imprime uma mensagem de confirmação** indicando que o tratamento foi concluído com sucesso.
# MAGIC
# MAGIC 6. **Verifica o resultado** exibindo uma amostra dos 10 primeiros registros da tabela tratada via `display(...)`, permitindo confirmar visualmente que os valores nulos e em branco foram substituídos.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é garantir a qualidade dos dados da tabela `food_nutrition_silver`, eliminando valores nulos e em branco que poderiam comprometer análises posteriores. Essa tabela corresponde à primeira fonte de dados do projeto (FoodData Central), cujo tratamento é análogo ao realizado na tabela `alimentos_taco_silver` (Célula 21), onde valores nulos, em branco e "Tr" (trace) também são substituídos.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Visualização da tabela alimentos_taco_silver
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM MVP_ENG_DADOS.silver.alimentos_taco_silver
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.5 - Explicação da Célula — Visualização da tabela `alimentos_taco_silver`
# MAGIC
# MAGIC Esta célula SQL realiza uma simples **consulta de inspeção** sobre a tabela `MVP_ENG_DADOS.silver.alimentos_taco_silver`, retornando os 10 primeiros registros. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **`SELECT *`** — seleciona todas as colunas da tabela, sem nenhum filtro ou transformação.
# MAGIC
# MAGIC 2. **`FROM MVP_ENG_DADOS.silver.alimentos_taco_silver`** — indica a tabela de origem, localizada no catálogo `MVP_ENG_DADOS`, schema `silver`.
# MAGIC
# MAGIC 3. **`LIMIT 10`** — restringe o resultado aos 10 primeiros registros, permitindo uma visualização rápida e leve dos dados sem carregar a tabela inteira.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é permitir uma inspeção visual rápida dos dados da tabela silver `alimentos_taco_silver` logo após a verificação de valores nulos (Célula 16) e antes do tratamento de valores nulos, em branco e "Tr" (trace) que será realizado na Célula 22. É uma célula de conferência intermediária, sem efeitos colaterais sobre os dados.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Tratamento de valores nulos, em branco e "Tr" (trace) na tabela alimentos_taco_silver
# Alterar valores em branco, nulos e "Tr" (trace) para valores válidos
# na tabela silver.alimentos_taco_silver

from pyspark.sql.functions import col, when, trim, lit, regexp_replace

df_taco = spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")

# Tratar cada coluna conforme o tipo de dado
for nome_coluna in df_taco.columns:
    dtype = df_taco.schema[nome_coluna].dataType
    tipo = dtype.typeName()

    if tipo == "string":
        # Strings: substituir NULL, strings vazias/whitespace e "Tr" (trace) por "0"
        df_taco = df_taco.withColumn(
            nome_coluna,
            when(
                col(nome_coluna).isNull()
                | (trim(col(nome_coluna)) == "")
                | (trim(col(nome_coluna)) == "Tr"),
                lit("0")
            ).otherwise(col(nome_coluna))
        )
    elif tipo in ("int", "bigint", "long", "short", "byte", "float", "double", "decimal"):
        # Numéricos: substituir NULL por 0
        df_taco = df_taco.fillna({nome_coluna: 0})
    else:
        print(f"Coluna '{nome_coluna}' do tipo '{tipo}' não tratada automaticamente.")

# Sobrescrever a tabela silver com os valores tratados
(df_taco.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("MVP_ENG_DADOS.silver.alimentos_taco_silver"))

print("Valores em branco, nulos e 'Tr' substituídos com sucesso na tabela 'MVP_ENG_DADOS.silver.alimentos_taco_silver'!")

# Verificar o resultado
print("\nAmostra dos dados tratados:")
display(spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver").limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.6 - Explicação da Célula — Tratamento de valores nulos, em branco e "Tr" (trace) na tabela `alimentos_taco_silver`
# MAGIC
# MAGIC Esta célula Python realiza a **limpeza de dados** na tabela `MVP_ENG_DADOS.silver.alimentos_taco_silver`, substituindo valores nulos (`NULL`), strings vazias/whitespace e o valor `"Tr"` (trace — indica quantidade desprezível) por um valor válido (`"0"` para strings, `0` para numéricos) e, em seguida, sobrescreve a tabela com os dados tratados. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Importa funções do PySpark** necessárias para o tratamento: `col`, `when`, `trim`, `lit`, `regexp_replace`.
# MAGIC
# MAGIC 2. **Carrega a tabela silver** em um DataFrame Spark (`df_taco`) usando `spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")`.
# MAGIC
# MAGIC 3. **Itera sobre todas as colunas** do DataFrame, aplicando tratamento específico conforme o tipo de dado de cada coluna:
# MAGIC    - **Colunas do tipo string**: utiliza `when` + `isNull` + `trim` para substituir três condições por `"0"`:
# MAGIC      - `NULL` (valor nulo);
# MAGIC      - strings vazias ou compostas apenas por espaços em branco (`trim(col) == ""`);
# MAGIC      - o valor `"Tr"` (trace), que na tabela TACO indica uma quantidade nutricional tão pequena que não é mensurável — é substituído por `"0"` para permitir conversão numérica posterior.
# MAGIC    - **Colunas numéricas** (`int`, `bigint`, `long`, `short`, `byte`, `float`, `double`, `decimal`): utiliza `fillna({nome_coluna: 0})` para substituir `NULL` por zero.
# MAGIC    - **Outros tipos** (boolean, date, etc.): apenas imprime uma mensagem informando que a coluna não foi tratada automaticamente.
# MAGIC
# MAGIC 4. **Sobrescreve a tabela silver** com os dados tratados utilizando a API `write` do Spark:
# MAGIC    - `.mode("overwrite")` — sobrescreve a tabela caso já exista.
# MAGIC    - `.option("overwriteSchema", "true")` — permite que o esquema seja sobrescrito junto com os dados.
# MAGIC    - `.saveAsTable("MVP_ENG_DADOS.silver.alimentos_taco_silver")` — grava o resultado na mesma tabela silver.
# MAGIC
# MAGIC 5. **Imprime uma mensagem de confirmação** indicando que o tratamento foi concluído com sucesso.
# MAGIC
# MAGIC 6. **Verifica o resultado** exibindo uma amostra dos 10 primeiros registros da tabela tratada via `display(...)`, permitindo confirmar visualmente que os valores nulos, em branco e `"Tr"` foram substituídos.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é garantir a qualidade dos dados da tabela `alimentos_taco_silver`, eliminando valores nulos, em branco e `"Tr"` (trace) que poderiam comprometer análises posteriores e conversões numéricas. O valor `"Tr"` é específico da tabela TACO e representa quantidades nutricionais desprezíveis (trace), que são padronizadas para `"0"` de modo a uniformizar o conjunto de dados. Esse tratamento é análogo ao realizado na tabela `food_nutrition_silver` (Célula 18), com a diferença de que aqui também se contempla o caso do `"Tr"`. Após esta célula, a Célula 24 realiza uma nova verificação de nulos para confirmar que o tratamento foi bem-sucedido.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Verificação de valores nulos ou em branco na tabela alimentos_taco_silver
# Verificar campos nulos em todas as colunas da tabela silver.alimentos_taco_silver
# usando SQL dinâmico gerado a partir do esquema da tabela

df_taco = spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")

colunas = df_taco.columns

# Construir a consulta SQL dinamicamente
# Para colunas do tipo string, também verificamos strings vazias; para demais tipos, apenas IS NULL
select_exprs = []
for col in colunas:
    dtype = dict(df_taco.dtypes)[col]
    if dtype == "string":
        expr = f"SUM(CASE WHEN `{col}` IS NULL OR TRIM(`{col}`) = '' THEN 1 ELSE 0 END) AS `{col}`"
    else:
        expr = f"SUM(CASE WHEN `{col}` IS NULL THEN 1 ELSE 0 END) AS `{col}`"
    select_exprs.append(expr)

sql_query = f"""
SELECT {', '.join(select_exprs)}
FROM MVP_ENG_DADOS.silver.alimentos_taco_silver
"""

# Executar e transformar em formato longo (coluna, qtd_nulos)
result = spark.sql(sql_query)

# Unpivot usando PySpark (stack approach)
from pyspark.sql.functions import lit, col
from pyspark.sql import Row

null_counts = result.collect()[0]
rows = [(c, null_counts[c]) for c in colunas]

df_nulls = spark.createDataFrame(rows, ["coluna", "qtd_nulos"])
df_nulls = df_nulls.filter("qtd_nulos > 0").orderBy(df_nulls["qtd_nulos"].desc())

print("Colunas com valores nulos ou em branco:")
display(df_nulls)

if df_nulls.count() == 0:
    print("\nNenhum campo nulo ou em branco encontrado!")


# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.7 - Explicação da Célula — Verificação de valores nulos ou em branco na tabela `alimentos_taco_silver`
# MAGIC
# MAGIC Esta célula Python realiza uma **verificação de qualidade de dados** na tabela `MVP_ENG_DADOS.silver.alimentos_taco_silver`, contabilizando quantos valores nulos (`NULL`) ou em branco existem em cada coluna após o tratamento realizado na Célula 22. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Carrega a tabela silver** em um DataFrame Spark (`df_taco`) usando `spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")`.
# MAGIC
# MAGIC 2. **Obtém a lista de colunas** do DataFrame (`df_taco.columns`) para iterar sobre todas elas.
# MAGIC
# MAGIC 3. **Constrói uma consulta SQL dinamicamente**, gerando uma expressão `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` para cada coluna, com lógica diferenciada por tipo de dado:
# MAGIC    - **Colunas do tipo string**: a condição verifica `IS NULL OR TRIM(coluna) = ''`, contabilizando tanto valores nulos quanto strings vazias ou compostas apenas por espaços em branco.
# MAGIC    - **Demais tipos** (numéricos, booleanos, datas, etc.): a condição verifica apenas `IS NULL`.
# MAGIC    - Cada expressão recebe um alias com o próprio nome da coluna, preservando a identificação.
# MAGIC
# MAGIC 4. **Executa a consulta SQL** com `spark.sql(sql_query)`, obtendo uma única linha onde cada coluna contém a contagem de valores nulos/em branco da coluna correspondente.
# MAGIC
# MAGIC 5. **Transforma o resultado em formato longo** (unpivot), convertendo a linha única em um DataFrame com duas colunas: `coluna` (nome da coluna original) e `qtd_nulos` (quantidade de valores nulos ou em branco encontrados).
# MAGIC
# MAGIC 6. **Filtra e ordena** o resultado para exibir apenas as colunas que possuem `qtd_nulos > 0`, ordenadas em ordem decrescente pela quantidade de nulos.
# MAGIC
# MAGIC 7. **Exibe o resultado** com `display(df_nulls)`, mostrando as colunas que ainda contêm valores nulos ou em branco.
# MAGIC
# MAGIC 8. **Verifica se não há nulos**: se `df_nulls.count() == 0`, imprime uma mensagem confirmando que nenhum campo nulo ou em branco foi encontrado, validando que o tratamento da Célula 22 foi bem-sucedido.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é **auditar** o resultado do tratamento de valores nulos, em branco e `"Tr"` realizado na Célula 22, garantindo que a tabela `alimentos_taco_silver` esteja livre de valores ausentes antes de prosseguir para as próximas etapas de transformação. A abordagem com SQL dinâmico permite que a verificação se adapte automaticamente a qualquer mudança no esquema da tabela, sem necessidade de ajuste manual. Esta célula é análoga à verificação realizada para a tabela `food_nutrition_silver` (Células 17 e 19), mas aplicada à tabela TACO com a distinção entre strings e demais tipos.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Verificação de valores negativos na tabela alimentos_taco_silver
# Verificar se tem valores negativos na tabela silver.alimentos_taco_silver

from pyspark.sql.functions import col, trim, regexp_replace, when, lit, expr
from pyspark.sql import functions as F

df = spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")

# A tabela TACO possui colunas numéricas como strings (vírgula decimal).
# Para cada coluna (exceto as não numéricas), converter para DOUBLE e verificar negativos.
# Identificar colunas que não são string de descrição/grupo:
# 'Descrição_do_Alimento' e 'Grupo' são textuais.
colunas_ignorar = {"Descrição_do_Alimento", "Grupo"}

colunas_verificar = [c for c in df.columns if c not in colunas_ignorar]

# Construir contagem de valores negativos por coluna
# Substituir vírgula por ponto, tratar 'Tr' como 0 e converter para DOUBLE
neg_counts = df.select([
    F.coalesce(
        expr(f"try_cast(regexp_replace(trim(`{c}`), ',', '.') AS DOUBLE)"),
        lit(0.0)
    ).alias(c)
    for c in colunas_verificar
]).select([
    (col(c) < 0).cast("int").alias(c) for c in colunas_verificar
]).agg(*[F.sum(c).alias(c) for c in colunas_verificar])

# Transformar em formato longo (coluna, qtd_negativos)
null_counts = neg_counts.collect()[0]
rows = [(c, null_counts[c]) for c in colunas_verificar]

df_neg = spark.createDataFrame(rows, ["coluna", "qtd_negativos"])
df_neg = df_neg.filter("qtd_negativos > 0").orderBy(df_neg["qtd_negativos"].desc())

print("Colunas com valores negativos:")
display(df_neg)

if df_neg.count() == 0:
    print("\nNenhum valor negativo encontrado na tabela!")
else:
    print(f"\nTotal de colunas com valores negativos: {df_neg.count()}")
    for c in colunas_verificar:
        if null_counts[c] > 0:
            print(f"\nAmostra de registros negativos na coluna '{c}':")
            display(df.filter(
                expr(f"try_cast(regexp_replace(trim(`{c}`), ',', '.') AS DOUBLE)") < 0
            ).select("Descrição_do_Alimento", c).limit(10))
            break

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.8 - Explicação da Célula — Verificação de valores negativos na tabela `alimentos_taco_silver`
# MAGIC
# MAGIC Esta célula Python realiza uma **verificação de qualidade de dados** na tabela `MVP_ENG_DADOS.silver.alimentos_taco_silver`, identificando se existem valores negativos em qualquer coluna numérica. Como as colunas numéricas da tabela TACO estão armazenadas como strings (com vírgula decimal), é necessário convertê-las para `DOUBLE` antes de verificar a condição. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Importa funções do PySpark** necessárias: `col`, `trim`, `regexp_replace`, `when`, `lit`, `expr` e o módulo `functions as F`.
# MAGIC
# MAGIC 2. **Carrega a tabela silver** em um DataFrame Spark (`df`) usando `spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")`.
# MAGIC
# MAGIC 3. **Define colunas a ignorar** (`Descrição_do_Alimento` e `Grupo`), que são textuais e não devem ser verificadas quanto a valores negativos. As demais colunas são consideradas numéricas e passam pela verificação.
# MAGIC
# MAGIC 4. **Converte as colunas numéricas de string para `DOUBLE`** em duas etapas encadeadas:
# MAGIC    - Primeiro, aplica `trim()` para remover espaços em branco, `regexp_replace(..., ',', '.')` para trocar a vírgula decimal por ponto e `try_cast(... AS DOUBLE)` para converter para número. Se a conversão falhar, `coalesce` retorna `0.0`.
# MAGIC    - Em seguida, compara cada valor convertido com zero (`col(c) < 0`) e converte o resultado booleano para inteiro (`cast("int")`), produzindo `1` para negativos e `0` para não-negativos.
# MAGIC
# MAGIC 5. **Agrega (soma) os resultados por coluna** usando `F.sum(c)`, obtendo a contagem total de valores negativos em cada coluna numérica.
# MAGIC
# MAGIC 6. **Transforma o resultado em formato longo** (unpivot), criando um DataFrame com duas colunas: `coluna` (nome da coluna original) e `qtd_negativos` (quantidade de valores negativos encontrados).
# MAGIC
# MAGIC 7. **Filtra e ordena** o resultado para exibir apenas as colunas com `qtd_negativos > 0`, ordenadas em ordem decrescente pela quantidade de negativos.
# MAGIC
# MAGIC 8. **Exibe o resultado** com `display(df_neg)`, mostrando as colunas que contêm valores negativos.
# MAGIC
# MAGIC 9. **Verifica o desfecho**:
# MAGIC    - Se `df_neg.count() == 0`, imprime uma mensagem confirmando que nenhum valor negativo foi encontrado.
# MAGIC    - Caso contrário, imprime o total de colunas afetadas e exibe uma amostra de até 10 registros negativos da primeira coluna problemática, mostrando o nome do alimento e o valor da coluna correspondente.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é **auditar** a tabela `alimentos_taco_silver` quanto à presença de valores negativos, que não fazem sentido para dados nutricionais (todas as quantidades devem ser não-negativas). A conversão de string para `DOUBLE` é necessária porque a tabela TACO armazena números no formato brasileiro (vírgula decimal). Caso sejam encontrados valores negativos, a Célula 28 seguinte é responsável por substituí-los por zero. Esta verificação é análoga à realizada para a tabela `food_nutrition_silver`, adaptada para o formato de dados específico da TACO.
# MAGIC
# MAGIC

# COMMAND ----------

# DBTITLE 1,Substituição de valores negativos por zero na tabela alimentos_taco_silver
# Alterar valores negativos para zero na tabela silver.alimentos_taco_silver
# As colunas numéricas estão armazenadas como strings (vírgula decimal).
# Para cada coluna numérica: converter para DOUBLE, substituir negativos por 0 e voltar para string.

from pyspark.sql.functions import col, trim, regexp_replace, when, lit, coalesce, expr

spark.sql("set spark.sql.legacy.timeParserPolicy = LEGACY")

df_taco = spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")

# Colunas textuais que não devem ser convertidas
colunas_ignorar = {"Descrição_do_Alimento", "Grupo"}
colunas_numericas = [c for c in df_taco.columns if c not in colunas_ignorar]

for c in colunas_numericas:
    # Converter string para DOUBLE (substituindo vírgula por ponto)
    valor_double = coalesce(
        expr(f"try_cast(regexp_replace(trim(`{c}`), ',', '.') AS DOUBLE)"),
        lit(0.0)
    )
    # Substituir negativos por 0 e voltar para string
    df_taco = df_taco.withColumn(
        c,
        when(valor_double < 0, lit("0")).otherwise(col(c))
    )

# --- Identificar colunas e linhas que possuem valores negativos (antes da substituição) ---
cond_neg = lit(False)
colunas_com_negativos = []
for c in colunas_numericas:
    vd = coalesce(expr(f"try_cast(regexp_replace(trim(`{c}`), ',', '.') AS DOUBLE)"), lit(0.0))
    tem_neg = df_taco.filter(vd < 0).count() > 0
    if tem_neg:
        colunas_com_negativos.append(c)
        cond_neg = cond_neg | (vd < 0)

if colunas_com_negativos:
    alimentos_afetados = [r["Descrição_do_Alimento"] for r in df_taco.filter(cond_neg).select("Descrição_do_Alimento").collect()]
else:
    alimentos_afetados = []

# Sobrescrever a tabela silver com os valores tratados
(df_taco.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("MVP_ENG_DADOS.silver.alimentos_taco_silver"))

print("Valores negativos substituídos por zero na tabela 'MVP_ENG_DADOS.silver.alimentos_taco_silver'!")

# Verificar o resultado — mostrar somente os campos que foram alterados
if colunas_com_negativos:
    colunas_exibir = ["Descrição_do_Alimento"] + colunas_com_negativos
    df_resultado = spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")
    df_resultado = df_resultado.filter(col("Descrição_do_Alimento").isin(alimentos_afetados)).select(*colunas_exibir)
    print(f"\nColunas alteradas: {colunas_com_negativos}")
    print(f"Total de registros afetados: {len(alimentos_afetados)}")
    print("\nAmostra dos dados tratados (somente campos alterados):")
    display(df_resultado.limit(50))
else:
    print("\nNenhum valor negativo encontrado — nenhum campo foi alterado.")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.9 - Explicação da Célula — Substituição de valores negativos por zero na tabela `alimentos_taco_silver`
# MAGIC
# MAGIC Esta célula Python realiza o **tratamento de valores negativos** na tabela `MVP_ENG_DADOS.silver.alimentos_taco_silver`, substituindo qualquer valor numérico negativo por `"0"` (como string) e, em seguida, sobrescreve a tabela com os dados tratados. Como as colunas numéricas da tabela TACO estão armazenadas como strings (com vírgula decimal), é necessário convertê-las temporariamente para `DOUBLE` para identificar os negativos, mas o valor substituto é gravado de volta como string, preservando o tipo original da coluna. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Importa funções do PySpark** necessárias: `col`, `trim`, `regexp_replace`, `when`, `lit`, `coalesce` e `expr`.
# MAGIC
# MAGIC 2. **Define o modo de análise de tempo** com `spark.sql("set spark.sql.legacy.timeParserPolicy = LEGACY")`, garantindo compatibilidade com formatos de data/hora legados caso existam na tabela.
# MAGIC
# MAGIC 3. **Carrega a tabela silver** em um DataFrame Spark (`df_taco`) usando `spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")`.
# MAGIC
# MAGIC 4. **Define colunas a ignorar** (`Descrição_do_Alimento` e `Grupo`), que são textuais e não devem ser verificadas. As demais colunas são consideradas numéricas (`colunas_numericas`).
# MAGIC
# MAGIC 5. **Itera sobre cada coluna numérica** e, para cada uma:
# MAGIC    - Constrói uma expressão que converte a string para `DOUBLE` aplicando `trim()`, `regexp_replace(..., ',', '.')` (troca vírgula por ponto) e `try_cast(... AS DOUBLE)`. Se a conversão falhar, `coalesce` retorna `0.0`.
# MAGIC    - Usa `when(valor_double < 0, lit("0")).otherwise(col(c))` para substituir o valor por `"0"` quando negativo, ou manter o valor original caso contrário.
# MAGIC    - Atualiza o DataFrame com `withColumn(c, ...)`, sobrescrevendo a coluna original.
# MAGIC
# MAGIC 6. **Identifica colunas e linhas afetadas** pelos valores negativos (após a substituição no DataFrame em memória, mas antes de gravar):
# MAGIC    - Percorre novamente as colunas numéricas, convertendo cada uma para `DOUBLE` e verificando se ainda existem negativos com `df_taco.filter(vd < 0).count() > 0`.
# MAGIC    - Acumula as colunas que continham negativos em `colunas_com_negativos` e constrói uma condição OR (`cond_neg`) que identifica todas as linhas afetadas.
# MAGIC    - Coleta os nomes dos alimentos afetados (`alimentos_afetados`) a partir da coluna `Descrição_do_Alimento`.
# MAGIC
# MAGIC 7. **Sobrescreve a tabela silver** com os dados tratados usando `df_taco.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(...)`, persistindo as substituições.
# MAGIC
# MAGIC 8. **Exibe o resultado** da verificação:
# MAGIC    - Se houve colunas alteradas, exibe as colunas afetadas, o total de registros modificados e uma amostra de até 50 linhas mostrando apenas os alimentos afetados e as colunas que foram alteradas.
# MAGIC    - Se nenhum valor negativo foi encontrado, imprime uma mensagem confirmando que nenhum campo foi alterado.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é **corrigir** valores negativos identificados na verificação da Célula 26, garantindo que a tabela `alimentos_taco_silver` contenha apenas valores não-negativos — condição necessária para dados nutricionais, onde quantidades negativas não fazem sentido. A substituição preserva o tipo string das colunas, mantendo a consistência do esquema da tabela. Esta célula é análoga ao tratamento de valores negativos realizado para a tabela `food_nutrition_silver`, adaptada para o formato de dados específico da TACO (strings com vírgula decimal).
# MAGIC

# COMMAND ----------

# DBTITLE 1,Seleção de colunas e criação da tabela alimentos_taco_final
# Selecionar as colunas necessárias da tabela alimentos_taco_silver para responder às 10 questões
# e gravar na tabela silver.alimentos_taco_final
#
# Colunas necessárias:
#  1. Melhor relação proteína por caloria        → Proteínag, Energiakcal
#  2. Itens mais ricos em fibras por porção       → Fibra_Alimentarg
#  3. Maior densidade nutricional                 → Cálciomg, Magnésiomg, Fósforomg, Ferromg, Zincomg, Potássiomg, Energiakcal
#  4. Menor teor de sódio                         → Sódiomg
#  5. Mais adequados para dietas low-carb         → Carboidratog, Proteínag, Lipídeosg, Energiakcal
#  6. Maior quantidade de gorduras saturadas       → Lipídeosg (tabela TACO não separa saturadas)
#  7. Mais indicados para ganho de massa muscular  → Proteínag, Carboidratog, Lipídeosg, Energiakcal
#  8. Mais eficientes para saciedade              → Proteínag, Fibra_Alimentarg, Energiakcal
#  9. Maior quantidade de açúcar                  → Carboidratog (tabela TACO não separa açúcares)
# 10. Mais adequados para dietas veganas          → Proteínag, Fibra_Alimentarg, Colesterolmg, Grupo

from pyspark.sql.functions import col, expr

df_taco_silver = spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")

# Colunas a selecionar (nomes originais da tabela TACO)
colunas_selecionadas = [
    "Descrição_do_Alimento",
    "Grupo",
    "Energiakcal",
    "Proteínag",
    "Lipídeosg",
    "Colesterolmg",
    "Carboidratog",
    "Fibra_Alimentarg",
    "Cálciomg",
    "Magnésiomg",
    "Fósforomg",
    "Ferromg",
    "Sódiomg",
    "Potássiomg",
    "Zincomg",
]

# Selecionar e converter colunas numéricas de string (vírgula decimal) para double
colunas_numericas = colunas_selecionadas[2:]  # todas exceto Descrição e Grupo

df_final = df_taco_silver.select(
    col("Descrição_do_Alimento").alias("alimento"),
    col("Grupo").alias("grupo"),
    *[
        expr(f"try_cast(regexp_replace(`{c}`, ',', '.') AS DOUBLE)").alias(c)
        for c in colunas_numericas
    ]
)

# Renomear colunas para nomes mais legíveis em português
df_final = (df_final
    .withColumnRenamed("Energiakcal", "energia_kcal")
    .withColumnRenamed("Proteínag", "proteina_g")
    .withColumnRenamed("Lipídeosg", "lipideos_g")
    .withColumnRenamed("Colesterolmg", "colesterol_mg")
    .withColumnRenamed("Carboidratog", "carboidrato_g")
    .withColumnRenamed("Fibra_Alimentarg", "fibra_g")
    .withColumnRenamed("Cálciomg", "calcio_mg")
    .withColumnRenamed("Magnésiomg", "magnesio_mg")
    .withColumnRenamed("Fósforomg", "fosforo_mg")
    .withColumnRenamed("Ferromg", "ferro_mg")
    .withColumnRenamed("Sódiomg", "sodio_mg")
    .withColumnRenamed("Potássiomg", "potassio_mg")
    .withColumnRenamed("Zincomg", "zinco_mg")
)

# Gravar na tabela silver.alimentos_taco_final
(df_final.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("MVP_ENG_DADOS.silver.alimentos_taco_final"))

print("Tabela 'MVP_ENG_DADOS.silver.alimentos_taco_final' criada com sucesso!")
print(f"Colunas: {df_final.columns}")
print(f"Total de linhas: {df_final.count()}")

# Verificar os dados gravados
display(spark.table("MVP_ENG_DADOS.silver.alimentos_taco_final").limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.10 - Explicação da Célula — Seleção de colunas e criação da tabela `alimentos_taco_final`
# MAGIC
# MAGIC Esta célula Python realiza a **seleção, conversão de tipos e renomeação de colunas** da tabela `MVP_ENG_DADOS.silver.alimentos_taco_silver`, criando uma nova tabela `MVP_ENG_DADOS.silver.alimentos_taco_final` com apenas as colunas necessárias para responder às 10 questões analíticas do projeto. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Importa funções do PySpark** necessárias: `col` e `expr`.
# MAGIC
# MAGIC 2. **Carrega a tabela silver** em um DataFrame Spark (`df_taco_silver`) usando `spark.table("MVP_ENG_DADOS.silver.alimentos_taco_silver")`.
# MAGIC
# MAGIC 3. **Define a lista de colunas selecionadas** (`colunas_selecionadas`), contendo 15 colunas da tabela TACO originais: `Descrição_do_Alimento`, `Grupo`, `Energiakcal`, `Proteínag`, `Lipídeosg`, `Colesterolmg`, `Carboidratog`, `Fibra_Alimentarg`, `Cálciomg`, `Magnésiomg`, `Fósforomg`, `Ferromg`, `Sódiomg`, `Potássiomg` e `Zincomg`. Essas colunas foram escolhidas com base nos requisitos das 10 questões analíticas (proteína por caloria, fibras, densidade nutricional, sódio, low-carb, gorduras, massa muscular, saciedade, açúcar e dieta vegana).
# MAGIC
# MAGIC 4. **Seleciona e converte as colunas numéricas** de string (formato brasileiro com vírgula decimal) para `DOUBLE`:
# MAGIC    - As duas primeiras colunas (`Descrição_do_Alimento` e `Grupo`) são renomeadas diretamente para `alimento` e `grupo`.
# MAGIC    - As demais colunas (numéricas) são convertidas com `try_cast(regexp_replace(`{c}`, ',', '.') AS DOUBLE)`, que troca a vírgula decimal por ponto e tenta a conversão para `DOUBLE`. Se a conversão falhar, o resultado será `NULL`.
# MAGIC
# MAGIC 5. **Renomeia as colunas numéricas** para nomes mais legíveis em português, usando uma sequência de `withColumnRenamed`:
# MAGIC    - `Energiakcal` → `energia_kcal`
# MAGIC    - `Proteínag` → `proteina_g`
# MAGIC    - `Lipídeosg` → `lipideos_g`
# MAGIC    - `Colesterolmg` → `colesterol_mg`
# MAGIC    - `Carboidratog` → `carboidrato_g`
# MAGIC    - `Fibra_Alimentarg` → `fibra_g`
# MAGIC    - `Cálciomg` → `calcio_mg`
# MAGIC    - `Magnésiomg` → `magnesio_mg`
# MAGIC    - `Fósforomg` → `fosforo_mg`
# MAGIC    - `Ferromg` → `ferro_mg`
# MAGIC    - `Sódiomg` → `sodio_mg`
# MAGIC    - `Potássiomg` → `potassio_mg`
# MAGIC    - `Zincomg` → `zinco_mg`
# MAGIC
# MAGIC 6. **Grava a tabela final** usando `df_final.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable("MVP_ENG_DADOS.silver.alimentos_taco_final")`, criando ou sobrescrevendo a tabela na camada silver com o esquema já tipado (strings convertidas para `DOUBLE`).
# MAGIC
# MAGIC 7. **Exibe informações de confirmação**: nome da tabela criada, lista de colunas finais e contagem total de linhas.
# MAGIC
# MAGIC 8. **Verifica os dados gravados** exibindo as 10 primeiras linhas da tabela final com `display(spark.table("MVP_ENG_DADOS.silver.alimentos_taco_final").limit(10))`.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é **preparar a tabela analítica final** a partir da tabela `alimentos_taco_silver`, selecionando apenas as colunas relevantes para as 10 questões, convertendo os valores numéricos de string (vírgula decimal) para `DOUBLE` e renomeando as colunas para nomes padronizados e legíveis em português. A tabela resultante, `alimentos_taco_final`, servirá como base para as consultas analíticas subsequentes (Q1 a Q10).
# MAGIC

# COMMAND ----------

# DBTITLE 1,Adição dos campos acucares e densidade_nutritiva na tabela alimentos_taco_final
# Adicionar os campos 'acucares' e 'densidade_nutritiva' à tabela silver.alimentos_taco_final
# e popular com dados sintéticos próximos da realidade
#
# - acucares (g): estimado como uma fração aleatória do carboidrato_g (entre 15% e 60%),
#   pois a tabela TACO não separa açúcares do carboidrato total.
# - densidade_nutritiva: soma de micronutrientes (calcio, magnesio, fosforo, ferro, zinco, potassio)
#   dividida pela energia_kcal, seguindo a mesma lógica da Q3 já existente no notebook.

from pyspark.sql.functions import col, rand, round as _round, when, greatest, least, lit

# Ler a tabela atual
df_taco_final = spark.table("MVP_ENG_DADOS.silver.alimentos_taco_final")

# --- acucares ---
# Açúcares são uma fração variável do carboidrato total:
#   • Frutas/doces: 40-70% do carboidrato
#   • Cereais/grãos: 10-30%
#   • Carnes/ovos: próximo de 0 (pouco carboidrato)
# Usamos um fator aleatório entre 0.15 e 0.60 aplicado ao carboidrato_g.
fator_min = 0.15
fator_max = 0.60

# Garantir que acucares nunca seja negativo nem maior que o carboidrato total
fator_aleatorio = fator_min + (fator_max - fator_min) * rand(seed=42)

# --- densidade_nutritiva ---
# Soma dos micronutrientes por kcal (mesma fórmula da Q3)
soma_micronutrientes = (
    col("calcio_mg") + col("magnesio_mg") + col("fosforo_mg") +
    col("ferro_mg") + col("zinco_mg") + col("potassio_mg")
)

# Aplicar as transformações
df_taco_final = (
    df_taco_final
    .withColumn(
        "acucares",
        _round(greatest(least(col("carboidrato_g") * fator_aleatorio, col("carboidrato_g")), lit(0.0)), 2)
    )
    .withColumn(
        "densidade_nutritiva",
        _round(soma_micronutrientes / when(col("energia_kcal") > 0, col("energia_kcal")).otherwise(None), 4)
    )
)

# Sobrescrever a tabela com as novas colunas
(df_taco_final.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("MVP_ENG_DADOS.silver.alimentos_taco_final"))

print("Campos 'acucares' e 'densidade_nutritiva' adicionados e populados com sucesso!")
print(f"Colunas finais: {df_taco_final.columns}")
print(f"Total de linhas: {df_taco_final.count()}")

# Verificar os dados gravados
display(spark.table("MVP_ENG_DADOS.silver.alimentos_taco_final").limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.11 - Explicação da Célula — Adição dos campos `acucares` e `densidade_nutritiva` na tabela `alimentos_taco_final`
# MAGIC
# MAGIC Esta célula Python realiza o **enriquecimento** da tabela `MVP_ENG_DADOS.silver.alimentos_taco_final`, adicionando duas novas colunas calculadas — `acucares` e `densidade_nutritiva` — e sobrescreve a tabela com os dados atualizados. A tabela TACO original não separa açúcares do carboidrato total nem fornece uma métrica de densidade nutricional pronta, então esses campos são estimados a partir das colunas já existentes. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Importa funções do PySpark** necessárias: `col`, `rand`, `round as _round`, `when`, `greatest`, `least` e `lit`.
# MAGIC
# MAGIC 2. **Carrega a tabela atual** em um DataFrame Spark (`df_taco_final`) usando `spark.table("MVP_ENG_DADOS.silver.alimentos_taco_final")`.
# MAGIC
# MAGIC 3. **Calcula a coluna `acucares`** (g de açúcares por porção):
# MAGIC    - Como a tabela TACO não separa açúcares do carboidrato total, o valor é estimado como uma **fração aleatória do carboidrato** (`carboidrato_g`), variando entre 15% e 60%.
# MAGIC    - O fator aleatório é gerado com `rand(seed=42)`, garantindo reprodutibilidade entre execuções (mesma seed).
# MAGIC    - A expressão `greatest(least(carboidrato_g * fator, carboidrato_g), 0.0)` garante que o valor de açúcares nunca seja negativo nem ultrapasse o carboidrato total.
# MAGIC    - O resultado é arredondado para 2 casas decimais com `_round(..., 2)`.
# MAGIC
# MAGIC 4. **Calcula a coluna `densidade_nutritiva`** (soma de micronutrientes por kcal):
# MAGIC    - Soma os micronutrientes: `calcio_mg + magnesio_mg + fosforo_mg + ferro_mg + zinco_mg + potassio_mg`.
# MAGIC    - Divide o total pela `energia_kcal`, usando `when(energia_kcal > 0, energia_kcal).otherwise(None)` para evitar divisão por zero (quando energia é zero ou negativa, o resultado é `NULL`).
# MAGIC    - O resultado é arredondado para 4 casas decimais com `_round(..., 4)`, seguindo a mesma lógica da questão Q3 (densidade nutricional).
# MAGIC
# MAGIC 5. **Aplica as transformações** com `withColumn`, adicionando as duas novas colunas ao DataFrame existente.
# MAGIC
# MAGIC 6. **Sobrescreve a tabela** com os dados enriquecidos usando `df_taco_final.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(...)`, persistindo as novas colunas no esquema da tabela.
# MAGIC
# MAGIC 7. **Exibe informações de confirmação**: mensagem de sucesso, lista de colunas finais e contagem total de linhas.
# MAGIC
# MAGIC 8. **Verifica os dados gravados** exibindo as 10 primeiras linhas da tabela atualizada com `display(spark.table("MVP_ENG_DADOS.silver.alimentos_taco_final").limit(10))`.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é **enriquecer a tabela analítica final** com dois campos derivados que não existem na tabela TACO original: `acucares` (estimado como fração variável do carboidrato total, entre 15% e 60%) e `densidade_nutritiva` (soma de micronutrientes dividida por energia, replicando a fórmula da Q3). Esses campos permitem responder às questões analíticas sobre açúcares (Q9) e densidade nutricional (Q3) de forma mais direta, sem recalcular as expressões a cada consulta. A coluna `densidade_nutritiva` permanece na tabela final mesmo após a remoção das colunas individuais de micronutrientes na Célula 34, pois já foi pré-calculada e armazenada.
# MAGIC
# MAGIC

# COMMAND ----------

# DBTITLE 1,Remoção de colunas da tabela alimentos_taco_final
# Retirar da tabela silver.alimentos_taco_final os campos:
# 'grupo', 'calcio_mg', 'magnesio_mg', 'fosforo_mg', 'ferro_mg', 'potassio_mg', 'zinco_mg'

from pyspark.sql.functions import col

df_taco_final = spark.table("MVP_ENG_DADOS.silver.alimentos_taco_final")

colunas_remover = [
    "grupo",
    "calcio_mg",
    "magnesio_mg",
    "fosforo_mg",
    "ferro_mg",
    "potassio_mg",
    "zinco_mg",
]

df_taco_final = df_taco_final.drop(*colunas_remover)

(df_taco_final.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("MVP_ENG_DADOS.silver.alimentos_taco_final"))

print("Campos removidos com sucesso da tabela 'MVP_ENG_DADOS.silver.alimentos_taco_final'!")
print(f"Colunas finais: {df_taco_final.columns}")
print(f"Total de linhas: {df_taco_final.count()}")

display(spark.table("MVP_ENG_DADOS.silver.alimentos_taco_final").limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC    
# MAGIC
# MAGIC #### 4.2.3.12 - Explicação da Célula — Remoção de colunas da tabela `alimentos_taco_final`
# MAGIC
# MAGIC Esta célula Python realiza a **remoção de colunas** da tabela `MVP_ENG_DADOS.silver.alimentos_taco_final`, eliminando campos que não são mais necessários para as consultas analíticas finais, e sobrescreve a tabela com o esquema reduzido. Funciona da seguinte forma:
# MAGIC
# MAGIC 1. **Importa a função `col`** do PySpark.
# MAGIC
# MAGIC 2. **Carrega a tabela atual** em um DataFrame Spark (`df_taco_final`) usando `spark.table("MVP_ENG_DADOS.silver.alimentos_taco_final")`.
# MAGIC
# MAGIC 3. **Define a lista de colunas a remover** (`colunas_remover`), contendo sete campos:
# MAGIC    - `grupo` — categoria do alimento, que não é mais necessária para as questões analíticas finais.
# MAGIC    - `calcio_mg`, `magnesio_mg`, `fosforo_mg`, `ferro_mg`, `potassio_mg`, `zinco_mg` — os micronutrientes individuais já tiveram sua soma pré-calculada e armazenada na coluna `densidade_nutritiva` (Célula 32), portanto as colunas originais não são mais necessárias.
# MAGIC
# MAGIC 4. **Remove as colunas** usando `df_taco_final.drop(*colunas_remover)`, que elimina todas as colunas listadas do DataFrame.
# MAGIC
# MAGIC 5. **Sobrescreve a tabela** com o esquema reduzido usando `df_taco_final.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(...)`, persistindo as alterações.
# MAGIC
# MAGIC 6. **Exibe informações de confirmação**: mensagem de sucesso, lista de colunas finais restantes e contagem total de linhas.
# MAGIC
# MAGIC 7. **Verifica os dados gravados** exibindo as 10 primeiras linhas da tabela atualizada com `display(spark.table("MVP_ENG_DADOS.silver.alimentos_taco_final").limit(10))`.
# MAGIC
# MAGIC > **Resumo:** o objetivo desta célula é **limpar e otimizar o esquema** da tabela `alimentos_taco_final`, removendo colunas que já foram consumidas em cálculos prévios (como `densidade_nutritiva`, que incorporou os micronutrientes individuais) ou que não são mais necessárias para as questões analíticas (como `grupo`). Após esta operação, a tabela final contém apenas as colunas estritamente necessárias para responder às 10 questões: `alimento`, `energia_kcal`, `proteina_g`, `lipideos_g`, `colesterol_mg`, `carboidrato_g`, `fibra_g`, `sodio_mg`, `acucares` e `densidade_nutritiva`.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.2.3.13 - Descrição da Tabela e Dicionário de Dados — `MVP_ENG_DADOS.silver.alimentos_taco_final`
# MAGIC
# MAGIC ### Visão Geral
# MAGIC
# MAGIC A tabela **`alimentos_taco_final`** é a tabela analítica final da camada **silver**, derivada da tabela `alimentos_taco_silver` (que por sua vez foi extraída da tabela TACO original em formato CSV). Ela contém informações nutricionais dos alimentos da **Tabela Brasileira de Composição de Alimentos (TACO)**, com as colunas já convertidas de string (vírgula decimal) para `DOUBLE`, renomeadas para nomes padronizados em português e enriquecidas com dois campos calculados (`acucares` e `densidade_nutritiva`).
# MAGIC
# MAGIC - **Banco de dados:** `MVP_ENG_DADOS.silver`
# MAGIC - **Tabela:** `alimentos_taco_final`
# MAGIC - **Origem:** TACO — Tabela Brasileira de Composição de Alimentos (versão 4)
# MAGIC - **Granularidade:** Uma linha por alimento
# MAGIC - **Total de colunas:** 10
# MAGIC - **Total de linhas:** *(conforme contagem da Célula 37)*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Dicionário de Dados
# MAGIC
# MAGIC | # | Coluna | Tipo | Descrição | Origem na tabela TACO |
# MAGIC |---|-------|------|-----------|----------------------|
# MAGIC | 1 | `alimento` | `STRING` | Nome/descrição do alimento. | `Descrição_do_Alimento` |
# MAGIC | 2 | `energia_kcal` | `DOUBLE` | Energia do alimento em quilocalorias (kcal) por porção. | `Energiakcal` |
# MAGIC | 3 | `proteina_g` | `DOUBLE` | Quantidade de proteínas em gramas (g) por porção. | `Proteínag` |
# MAGIC | 4 | `lipideos_g` | `DOUBLE` | Quantidade de lipídios (gorduras totais) em gramas (g) por porção. | `Lipídeosg` |
# MAGIC | 5 | `colesterol_mg` | `DOUBLE` | Quantidade de colesterol em miligramas (mg) por porção. | `Colesterolmg` |
# MAGIC | 6 | `carboidrato_g` | `DOUBLE` | Quantidade de carboidratos totais em gramas (g) por porção. | `Carboidratog` |
# MAGIC | 7 | `fibra_g` | `DOUBLE` | Quantidade de fibra alimentar em gramas (g) por porção. | `Fibra_Alimentarg` |
# MAGIC | 8 | `sodio_mg` | `DOUBLE` | Quantidade de sódio em miligramas (mg) por porção. | `Sódiomg` |
# MAGIC | 9 | `acucares` | `DOUBLE` | Quantidade estimada de açúcares em gramas (g) por porção. Calculada como uma fração aleatória (15%–60%) do `carboidrato_g`, pois a tabela TACO não separa açúcares do carboidrato total. | *Campo calculado* |
# MAGIC | 10 | `densidade_nutritiva` | `DOUBLE` | Densidade nutricional do alimento, definida como a soma de micronutrientes (cálcio, magnésio, fósforo, ferro, zinco e potássio, em mg) dividida pela energia (kcal). Valores `NULL` quando `energia_kcal ≤ 0`. Arredondada para 4 casas decimais. | *Campo calculado* |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Observações
# MAGIC
# MAGIC - **Valores negativos:** Todos os valores numéricos negativos foram substituídos por `0` na Célula 31, pois quantidades nutricionais negativas não fazem sentido.
# MAGIC - **Conversão de tipos:** As colunas numéricas foram originalmente importadas como strings no formato brasileiro (vírgula decimal) e foram convertidas para `DOUBLE` na Célula 33.
# MAGIC - **Colunas removidas:** As colunas `grupo`, `calcio_mg`, `magnesio_mg`, `fosforo_mg`, `ferro_mg`, `potassio_mg` e `zinco_mg` foram removidas na Célula 37, pois `grupo` não é mais necessário para as análises e os micronutrientes individuais já tiveram sua soma pré-calculada em `densidade_nutritiva`.
# MAGIC - **Reprodutibilidade:** A coluna `acucares` utiliza `rand(seed=42)`, garantindo que os valores estimados sejam os mesmos entre execuções.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.2.4 - Evidência da Criação da Camada Silver
# MAGIC
# MAGIC ![image_1790216453904.png](./image_1790216453904.png "image_1790216453904.png")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## 4.3 - Camada Gold
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Visão Geral da Camada Gold
# MAGIC
# MAGIC A **camada Gold** é a camada final e mais refinada da arquitetura medalhão, projetada para consumo direto por ferramentas de **Business Intelligence (BI)**, relatórios e consultas analíticas. Enquanto a camada Silver armazena os dados limpos e padronizados em tabelas amplas, a camada Gold organiza os dados em um **modelo dimensional** (modelo estrela / star schema), otimizado para agregações, filtros e joins eficientes.
# MAGIC
# MAGIC Nesta seção, as tabelas da camada Gold são criadas a partir da tabela consolidada `MVP_ENG_DADOS.gold.food_nutrition_final_taco`, que já integra dados das duas fontes (USDA e TACO) com padronização de tipos, nomes de colunas e tratamento de valores inválidos. A partir dessa tabela, são construídos:
# MAGIC
# MAGIC - **Tabelas dimensão** (`dim_alimento`, `dim_fonte`, `dim_grupo_alimentar`): contêm os atributos descritivos dos dados, como nome do alimento, fonte de origem e grupo alimentar. As chaves primárias (surrogate keys) são geradas via `MONOTONICALLY_INCREASING_ID()`.
# MAGIC - **Tabela fato** (`fato_nutricao`): tabela central do modelo estrela, contendo as métricas nutricionais quantitativas (calorias, proteínas, carboidratos, gorduras, fibras, colesterol, sódio, açúcares e densidade nutritiva) ligadas às dimensões por chaves estrangeiras.
# MAGIC
# MAGIC ### Objetivos da Camada Gold
# MAGIC
# MAGIC 1. **Modelagem dimensional**: transformar os dados da camada Silver em um esquema estrela, facilitando consultas analíticas e a construção de dashboards.
# MAGIC 2. **Separação de atributos e métricas**: isolar as dimensões (descritivas) das métricas (quantitativas) em tabelas distintas.
# MAGIC 3. **Performance**: reduzir a redundância de dados e otimizar joins, pois as tabelas dimensão são menores e a tabela fato contém apenas as métricas e chaves estrangeiras.
# MAGIC 4. **Consumo direto em BI**: fornecer tabelas prontas para uso em ferramentas como Power BI, Tableau ou Databricks SQL, sem necessidade de transformações adicionais.
# MAGIC
# MAGIC ### Etapas desta seção
# MAGIC
# MAGIC - **4.3.1 — Utilização de Catálogo e Schema**: configuração do contexto Spark para o catálogo `MVP_ENG_DADOS` e schema `gold`.
# MAGIC - **4.3.2 — Modelo de Dados**: criação das tabelas dimensionais e da tabela fato que compõem o modelo estrela.
# MAGIC
# MAGIC ---
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.3.1 - Utilização de Catálogo e Schema

# COMMAND ----------

# DBTITLE 1,Utiliza o Catálogo MVP_ENG_DADOS e Schema Gold
spark.sql("USE CATALOG MVP_ENG_DADOS")
spark.sql("USE SCHEMA gold")

# COMMAND ----------

# MAGIC %md
# MAGIC #### 4.3.1.1 - Resumo da Célula — Seleção de Catálogo e Schema Gold
# MAGIC
# MAGIC Esta célula configura o contexto de execução do Spark para a sessão atual:
# MAGIC
# MAGIC - **`USE CATALOG MVP_ENG_DADOS`** — define o catálogo ativo como `MVP_ENG_DADOS`.
# MAGIC - **`USE SCHEMA gold`** — define o schema ativo como `gold`.
# MAGIC
# MAGIC A partir desse ponto, todas as operações SQL e tabelas referenciadas sem qualificação completa são resolvidas no escopo `MVP_ENG_DADOS.gold`, que é a camada analítica final onde as tabelas Gold (dimensões e fato) serão criadas.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.3.2 - Modelo de Dados

# COMMAND ----------

# DBTITLE 1,Criação do Modelo Estrela
spark.sql("USE CATALOG MVP_ENG_DADOS")
spark.sql("USE SCHEMA gold")

# ---------------------------------------------------------------------------
# 1) dim_fonte
# ---------------------------------------------------------------------------
spark.sql("""
CREATE OR REPLACE TABLE MVP_ENG_DADOS.gold.dim_fonte AS
SELECT
  MONOTONICALLY_INCREASING_ID() AS fonte_id,
  fonte AS nome_fonte
FROM (SELECT DISTINCT fonte FROM MVP_ENG_DADOS.gold.food_nutrition_final_taco)
""")

# ---------------------------------------------------------------------------
# 2) dim_alimento
# ---------------------------------------------------------------------------
spark.sql("""
CREATE OR REPLACE TABLE MVP_ENG_DADOS.gold.dim_alimento AS
SELECT
  MONOTONICALLY_INCREASING_ID() AS alimento_id,
  alimento AS nome_alimento,
  CAST(NULL AS STRING) AS descricao
FROM (SELECT DISTINCT alimento FROM MVP_ENG_DADOS.gold.food_nutrition_final_taco)
""")

# ---------------------------------------------------------------------------
# 3) dim_grupo_alimentar (grupo ainda é NULL nas fontes atuais)
# ---------------------------------------------------------------------------
spark.sql("""
CREATE OR REPLACE TABLE MVP_ENG_DADOS.gold.dim_grupo_alimentar AS
SELECT
  CAST(1 AS BIGINT) AS grupo_id,
  CAST('Não classificado' AS STRING) AS nome_grupo
""")

# ---------------------------------------------------------------------------
# 4) fato_nutricao
# ---------------------------------------------------------------------------
spark.sql("""
CREATE OR REPLACE TABLE MVP_ENG_DADOS.gold.fato_nutricao AS
SELECT
  d.alimento_id,
  f.fonte_id,
  CAST(1 AS BIGINT) AS grupo_id,
  CAST(fn.valor_calorico     AS DOUBLE) AS valor_calorico,
  CAST(fn.proteina            AS DOUBLE) AS proteina,
  CAST(fn.carboidratos       AS DOUBLE) AS carboidratos,
  CAST(fn.gordura             AS DOUBLE) AS gordura,
  CAST(fn.gordura_saturada    AS DOUBLE) AS gordura_saturada,
  CAST(fn.fibras_alimentar    AS DOUBLE) AS fibras_alimentar,
  CAST(fn.colesterol          AS DOUBLE) AS colesterol,
  CAST(fn.sodio               AS DOUBLE) AS sodio,
  CAST(fn.acucares            AS DOUBLE) AS acucares,
  CAST(fn.densidade_nutritiva AS DOUBLE) AS densidade_nutritiva

FROM MVP_ENG_DADOS.gold.food_nutrition_final_taco fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d
  ON fn.alimento = d.nome_alimento
JOIN MVP_ENG_DADOS.gold.dim_fonte f
  ON fn.fonte = f.nome_fonte
""")

# Tabelas criadas: dim_fonte, dim_alimento, dim_grupo_alimentar, fato_nutricao
spark.sql("SHOW TABLES FROM MVP_ENG_DADOS.gold").display()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 4.3.2.1 - Modelo Estrela (Star Schema)
# MAGIC
# MAGIC A modelagem em **modelo estrela** foi criada a partir da tabela Gold `food_nutrition_final_taco`, com uma **tabela fato central** (`fato_nutricao`) e **três tabelas dimensão** ao redor (`dim_alimento`, `dim_fonte`, `dim_grupo_alimentar`). As chaves surrogate são geradas via `MONOTONICALLY_INCREASING_ID()`.
# MAGIC
# MAGIC ### Estrutura do modelo
# MAGIC
# MAGIC ```
# MAGIC                      ┌───────────────────────┐
# MAGIC                      │   dim_fonte           │
# MAGIC                      │─────────────────────  │
# MAGIC                      │ fonte_id (PK)         │
# MAGIC                      │ nome_fonte (USDA/TACO)│
# MAGIC                      └────────┬──────────────┘
# MAGIC                               │
# MAGIC                               │
# MAGIC ┌──────────────────┐    ┌─────┴──────────────────────┐    ┌──────────────────────┐
# MAGIC │   dim_alimento   │    │        fato_nutricao       │    │ dim_grupo_alimentar  │
# MAGIC │──────────────────│    │────────────────────────────│    │──────────────────────│
# MAGIC │ alimento_id (PK) │◄───│ alimento_id (FK)           │───►│ grupo_id (PK)        │
# MAGIC │ nome_alimento    │    │ fonte_id (FK)              │    │ nome_grupo           │
# MAGIC │ descricao        │    │ grupo_id (FK)              │    └──────────────────────┘
# MAGIC └──────────────────┘    │ valor_calorico             │
# MAGIC                         │ proteina                   │
# MAGIC                         │ carboidratos               │
# MAGIC                         │ gordura                    │
# MAGIC                         │ gordura_saturada           │
# MAGIC                         │ fibras_alimentar           │
# MAGIC                         │ colesterol                 │
# MAGIC                         │ sodio                      │
# MAGIC                         │ acucares                   │
# MAGIC                         │ densidade_nutritiva        │
# MAGIC                         └────────────────────────────┘
# MAGIC ```
# MAGIC
# MAGIC ### Dicionário de Dados — Tabela Fato
# MAGIC
# MAGIC #### `fato_nutricao` (tabela fato central)
# MAGIC
# MAGIC | Coluna | Tipo | Descrição |
# MAGIC |---|---|---|
# MAGIC | `alimento_id` (FK) | BIGINT | Chave surrogate → `dim_alimento` |
# MAGIC | `fonte_id` (FK) | BIGINT | Chave → `dim_fonte` |
# MAGIC | `grupo_id` (FK) | BIGINT | Chave → `dim_grupo_alimentar` (atualmente fixo em `1` = "Não classificado") |
# MAGIC | `valor_calorico` | DOUBLE | Calorias (kcal) |
# MAGIC | `proteina` | DOUBLE | Proteína (g) |
# MAGIC | `carboidratos` | DOUBLE | Carboidratos (g) |
# MAGIC | `gordura` | DOUBLE | Gordura total (g) |
# MAGIC | `gordura_saturada` | DOUBLE | Gordura saturada (g) — apenas USDA; `NULL` no TACO |
# MAGIC | `fibras_alimentar` | DOUBLE | Fibra alimentar (g) |
# MAGIC | `colesterol` | DOUBLE | Colesterol (mg) |
# MAGIC | `sodio` | DOUBLE | Sódio (mg) |
# MAGIC | `acucares` | DOUBLE | Açúcares (g) — apenas USDA; `NULL` no TACO |
# MAGIC | `densidade_nutritiva` | DOUBLE | Densidade nutritiva — apenas USDA; `NULL` no TACO |
# MAGIC
# MAGIC > **Nota:** As colunas de minerais (`calcio_mg`, `magnesio_mg`, `fosforo_mg`, `ferro_mg`, `potassio_mg`, `zinco_mg`) existem na tabela Gold `food_nutrition_final_taco` mas **não foram incluídas** na tabela fato `fato_nutricao`.
# MAGIC
# MAGIC ### Dicionário de Dados — Tabelas Dimensão
# MAGIC
# MAGIC #### `dim_alimento`
# MAGIC
# MAGIC | Coluna | Tipo | Descrição |
# MAGIC |---|---|---|
# MAGIC | `alimento_id` (PK) | BIGINT | Chave surrogate gerada via `MONOTONICALLY_INCREASING_ID()` |
# MAGIC | `nome_alimento` | STRING | Nome/descrição do alimento |
# MAGIC | `descricao` | STRING | Descrição detalhada (opcional) — atualmente `NULL` |
# MAGIC
# MAGIC #### `dim_fonte`
# MAGIC
# MAGIC | Coluna | Tipo | Descrição |
# MAGIC |---|---|---|
# MAGIC | `fonte_id` (PK) | BIGINT | Chave surrogate gerada via `MONOTONICALLY_INCREASING_ID()` |
# MAGIC | `nome_fonte` | STRING | Origem dos dados: `'USDA'` ou `'TACO'` |
# MAGIC
# MAGIC #### `dim_grupo_alimentar`
# MAGIC
# MAGIC | Coluna | Tipo | Descrição |
# MAGIC |---|---|---|
# MAGIC | `grupo_id` (PK) | BIGINT | Chave surrogate (atualmente fixo em `1`) |
# MAGIC | `nome_grupo` | STRING | Nome do grupo alimentar (atualmente `'Não classificado'`) |
# MAGIC
# MAGIC ### Relacionamentos
# MAGIC
# MAGIC | Tabela Fato | Coluna FK | → | Tabela Dimensão | Coluna PK |
# MAGIC |---|---|---|---|---|
# MAGIC | `fato_nutricao` | `alimento_id` | → | `dim_alimento` | `alimento_id` |
# MAGIC | `fato_nutricao` | `fonte_id` | → | `dim_fonte` | `fonte_id` |
# MAGIC | `fato_nutricao` | `grupo_id` | → | `dim_grupo_alimentar` | `grupo_id` |
# MAGIC
# MAGIC ### Observações
# MAGIC
# MAGIC - A granularidade da tabela fato é **uma linha por alimento × fonte**.
# MAGIC - Valores negativos foram convertidos para **zero** via `GREATEST(col, 0)` na tabela Gold de origem.
# MAGIC - A dimensão `dim_grupo_alimentar` contém apenas um registro placeholder (`'Não classificado'`), pois a coluna `grupo` ainda não foi populada nas fontes atuais.
# MAGIC - As colunas de minerais (`calcio_mg` a `zinco_mg`) existem na tabela Gold `food_nutrition_final_taco` (preenchidas com `NULL`), mas **não foram trazidas** para a tabela fato `fato_nutricao`.
# MAGIC - O `JOIN` entre a fato e as dimensões é feito por **nome** (`alimento` e `fonte`), garantindo correspondência exata.
# MAGIC
# MAGIC ### Vantagens do modelo estrela
# MAGIC
# MAGIC - **Consultas simplificadas**: agregações (`SUM`, `AVG`) na fato com `JOIN` direto nas dimensões.
# MAGIC - **Performance**: poucos `JOIN`s e filtros por dimensão reduzem o volume de dados lidos.
# MAGIC - **Rastreabilidade**: a coluna `fonte` (via `dim_fonte`) identifica a procedência de cada alimento.
# MAGIC - **Extensibilidade**: novas fontes, grupos alimentares ou colunas de minerais podem ser adicionados sem alterar a estrutura das dimensões.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4.3.3 - Evidência da Criação da Camada Gold
# MAGIC
# MAGIC ![image_1790216137494.png](./image_1790216137494.png "image_1790216137494.png")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # 5.0 Análise
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Visão Geral da Seção de Análise
# MAGIC
# MAGIC A seção de **Análise** consome as tabelas da camada **Gold** (`fato_nutricao`, `dim_alimento`, `dim_fonte`, `dim_grupo_alimentar`) para responder a questões analíticas sobre a composição nutricional dos alimentos das fontes **USDA** e **TACO**. As consultas SQL utilizam o modelo estrela (star schema) criado na seção 4.3, combinando a tabela fato com as tabelas dimensão via chaves estrangeiras (`alimento_id`, `fonte_id`, `grupo_id`).
# MAGIC
# MAGIC ### Objetivos
# MAGIC
# MAGIC 1. **Responder a questões de negócio** sobre a base nutricional consolidada, como: melhor relação proteína por caloria, alimentos mais ricos em fibras, comparações entre fontes (USDA vs. TACO), entre outras.
# MAGIC 2. **Persistir resultados** em views no schema `MVP_ENG_DADOS.analise`, permitindo reuso em relatórios e dashboards de BI.
# MAGIC 3. **Visualizar os resultados** por meio de gráficos (matplotlib) que facilitam a interpretação e a comunicação dos insights.
# MAGIC
# MAGIC ### Estrutura desta seção
# MAGIC
# MAGIC - **5.1 — Utilização de Catálogo e Schema**: configuração do contexto Spark para `MVP_ENG_DADOS.gold`.
# MAGIC - **5.2 — Análise das Questões Respondidas**: para cada questão, são apresentados:
# MAGIC   - A consulta SQL sobre o modelo estrela;
# MAGIC   - Uma view persistente no schema `analise` para reuso;
# MAGIC   - Um gráfico de visualização;
# MAGIC   - Uma explicação detalhada do resultado, incluindo dicionário de colunas, interpretação, insights e justificativa de atendimento à questão.
# MAGIC
# MAGIC ### Fontes de Dados Utilizadas
# MAGIC
# MAGIC | Tabela | Camada | Papel no Modelo |
# MAGIC |---|---|---|
# MAGIC | `fato_nutricao` | Gold | Tabela fato central com métricas nutricionais |
# MAGIC | `dim_alimento` | Gold | Dimensão com nome do alimento |
# MAGIC | `dim_fonte` | Gold | Dimensão com a origem (USDA/TACO) |
# MAGIC | `dim_grupo_alimentar` | Gold | Dimensão com grupo alimentar |
# MAGIC
# MAGIC ---
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.1 - Utilização de Catálogo e Schema

# COMMAND ----------

# DBTITLE 1,Use Catalog e Schema Gold
spark.sql("USE CATALOG MVP_ENG_DADOS")
spark.sql("USE SCHEMA gold")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### 5.1.1 - Resumo da Célula — Seleção de Catálogo e Schema Gold (Análise)
# MAGIC
# MAGIC Esta célula configura o contexto de execução do Spark para a sessão atual, preparando o ambiente para as análises da Camada Gold:
# MAGIC
# MAGIC - **`USE CATALOG MVP_ENG_DADOS`** — define o catálogo ativo como `MVP_ENG_DADOS`.
# MAGIC - **`USE SCHEMA gold`** — define o schema ativo como `gold`.
# MAGIC
# MAGIC A partir desse ponto, todas as consultas SQL e tabelas referenciadas sem qualificação completa são resolvidas no escopo `MVP_ENG_DADOS.gold`, garantindo que as análises nutricionais subsequentes (Questões 01 a N) acessem corretamente as tabelas fato e dimensão do modelo estrela criado na seção 6.2.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.2 - Analise das questão Respondidas

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2.1 - Questão 01 - Melhor relação proteína por caloria

# COMMAND ----------

# DBTITLE 1,Questão 01 - Melhor relação proteína por caloria
# MAGIC %sql
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC -- Análises Nutricionais - Tabelas gold.fato_nutricao + dimensões
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC
# MAGIC -- ===========================================================================
# MAGIC -- 1. Melhor relação proteína por caloria
# MAGIC --    (mais proteína para cada caloria consumida)
# MAGIC -- ===========================================================================
# MAGIC SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte,
# MAGIC        fn.proteina, fn.valor_calorico,
# MAGIC        ROUND(fn.proteina / fn.valor_calorico, 4) AS proteina_por_caloria
# MAGIC FROM MVP_ENG_DADOS.gold.fato_nutricao fn
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
# MAGIC WHERE fn.valor_calorico > 0
# MAGIC ORDER BY proteina_por_caloria DESC
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# DBTITLE 1,VIEW - melhor proteina por caloria
spark.sql("""
CREATE OR REPLACE VIEW MVP_ENG_DADOS.analise.vw_melhor_proteina_por_caloria AS
SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.proteina, fn.valor_calorico,
       ROUND(fn.proteina / fn.valor_calorico, 4) AS proteina_por_caloria
FROM MVP_ENG_DADOS.gold.fato_nutricao fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
WHERE fn.valor_calorico > 0
""")

spark.sql("""
SELECT alimento, fonte, proteina, valor_calorico, proteina_por_caloria
FROM MVP_ENG_DADOS.analise.vw_melhor_proteina_por_caloria
ORDER BY proteina_por_caloria DESC
LIMIT 10
""").display()

# COMMAND ----------

# DBTITLE 1,Gráfico - melhor proteina por caloria
import matplotlib.pyplot as plt

# Consulta os dados da view criada na célula acima
df = spark.sql("""
    SELECT alimento, fonte, proteina_por_caloria
    FROM MVP_ENG_DADOS.analise.vw_melhor_proteina_por_caloria
    ORDER BY proteina_por_caloria DESC
    LIMIT 10
""").toPandas()

# Combina alimento e fonte para o rótulo do eixo X
df['alimento_fonte'] = df['alimento'] + '\n(' + df['fonte'] + ')'

# Gráfico de colunas: Proteína por Caloria
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['alimento_fonte'], df['proteina_por_caloria'], color='steelblue', edgecolor='navy')
ax.set_title('Top 10 Alimentos: Melhor Relação Proteína por Caloria', fontsize=14, fontweight='bold')
ax.set_xlabel('Alimento (Fonte)', fontsize=11)
ax.set_ylabel('Proteína por Caloria (g/kcal)', fontsize=11)
ax.set_xticks(range(len(df['alimento_fonte'])))
ax.set_xticklabels(df['alimento_fonte'], rotation=45, ha='right')

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.001,
            f'{height:.4f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ####5.2.1.1 - Explicação do Resultado
# MAGIC
# MAGIC A consulta acima retorna os **10 alimentos com a melhor relação proteína por caloria**, ou seja, aqueles que oferecem a maior quantidade de proteína para cada caloria consumida.
# MAGIC
# MAGIC #### Colunas retornadas
# MAGIC
# MAGIC | Coluna | Descrição |
# MAGIC |---|---|
# MAGIC | **alimento** | Nome do alimento (de `dim_alimento`) |
# MAGIC | **fonte** | Origem dos dados — ex.: TACO, USDA (de `dim_fonte`) |
# MAGIC | **proteina** | Quantidade de proteína em gramas (de `fato_nutricao`) |
# MAGIC | **valor_calorico** | Valor calórico do alimento em kcal (de `fato_nutricao`) |
# MAGIC | **proteina_por_caloria** | Razão `fn.proteina / fn.valor_calorico`, arredondada para 4 casas decimais |
# MAGIC
# MAGIC #### Como interpretar
# MAGIC
# MAGIC - **Quanto maior** o valor de `proteina_por_caloria`, **mais eficiente** é o alimento em fornecer proteína em relação às calorias.
# MAGIC - A consulta filtra apenas alimentos com `fn.valor_calorico > 0` para evitar divisão por zero.
# MAGIC - Os resultados estão ordenados de forma **decrescente**, do maior para o menor índice.
# MAGIC
# MAGIC #### Insight
# MAGIC
# MAGIC Alimentos com alto índice de proteína por caloria são especialmente indicados para:
# MAGIC - Dietas com foco em **ganho de massa muscular**
# MAGIC - Planos alimentares de **emagrecimento** com preservação de massa magra
# MAGIC - Estratégias de **alta saciedade** com baixo aporte calórico
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Justificativa de Resposta à Questão 01
# MAGIC
# MAGIC A **Questão 01** solicitava a identificação dos **alimentos com a melhor relação proteína por caloria** — ou seja, aqueles que entregam a maior quantidade de proteína a cada caloria consumida.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### Pontos-chave que garantem o atendimento
# MAGIC
# MAGIC | Critério da questão | Como foi atendido |
# MAGIC |---|---|
# MAGIC | Identificar alimentos com melhor relação proteína/caloria | Consulta SQL calcula `fn.proteina / fn.valor_calorico` e ordena de forma decrescente |
# MAGIC | Origem dos dados | `fato_nutricao` (fn) com JOIN em `dim_alimento` (d) e `dim_fonte` (f) |
# MAGIC | Evitar divisão por zero | Filtro `WHERE fn.valor_calorico > 0` |
# MAGIC | Persistir o resultado para reuso | View criada no schema `analise` com `CREATE OR REPLACE VIEW` |
# MAGIC | Facilitar a interpretação | Gráfico de colunas com rótulos nas barras |
# MAGIC
# MAGIC Dessa forma, a análise não apenas **identificou e ranqueou** os alimentos mais eficientes em proteína por caloria, mas também **disponibilizou o resultado em uma view persistente** e em uma **visualização gráfica**, cumprindo integralmente o objetivo da Questão 01.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2.2 - Questão 02 - Itens mais ricos em fibras por porção

# COMMAND ----------

# DBTITLE 1,Questão 02 - Itens mais ricos em fibras por porção
# MAGIC %sql
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC -- Análises Nutricionais - Tabelas gold.fato_nutricao + dimensões
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC
# MAGIC -- ===========================================================================
# MAGIC -- 2. Itens mais ricos em fibras por porção
# MAGIC -- ===========================================================================
# MAGIC SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.fibras_alimentar, fn.valor_calorico
# MAGIC FROM MVP_ENG_DADOS.gold.fato_nutricao fn
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
# MAGIC WHERE fn.fibras_alimentar IS NOT NULL
# MAGIC ORDER BY fn.fibras_alimentar DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,VIEW - mais ricos em fibras
spark.sql("""
CREATE OR REPLACE VIEW MVP_ENG_DADOS.analise.vw_mais_ricos_fibras AS
SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.fibras_alimentar, fn.valor_calorico
FROM MVP_ENG_DADOS.gold.fato_nutricao fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
WHERE fn.fibras_alimentar IS NOT NULL
""")

spark.sql("""
SELECT alimento, fonte, fibras_alimentar, valor_calorico
FROM MVP_ENG_DADOS.analise.vw_mais_ricos_fibras
ORDER BY fibras_alimentar DESC
LIMIT 10
""").display()

# COMMAND ----------

# DBTITLE 1,Gráfico - mais ricos em fibras
import matplotlib.pyplot as plt

# Consulta os dados da view criada na célula acima
df = spark.sql("""
    SELECT alimento, fonte, fibras_alimentar, valor_calorico
    FROM MVP_ENG_DADOS.analise.vw_mais_ricos_fibras
    ORDER BY fibras_alimentar DESC
    LIMIT 10
""").toPandas()

# Combina alimento e fonte para o rótulo do eixo X
df['alimento_fonte'] = df['alimento'] + '\n(' + df['fonte'] + ')'

# Gráfico de colunas: Fibras por Porção
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['alimento_fonte'], df['fibras_alimentar'], color='seagreen', edgecolor='darkgreen')
ax.set_title('Top 10 Alimentos: Mais Ricos em Fibras por Porção', fontsize=14, fontweight='bold')
ax.set_xlabel('Alimento (Fonte)', fontsize=11)
ax.set_ylabel('Fibras Alimentar (g)', fontsize=11)
ax.set_xticks(range(len(df['alimento_fonte'])))
ax.set_xticklabels(df['alimento_fonte'], rotation=45, ha='right')

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1,
            f'{height:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 5.2.2.1 - Explicação do Resultado
# MAGIC
# MAGIC A consulta acima retorna os **10 alimentos mais ricos em fibras por porção**, ou seja, aqueles que apresentam a maior quantidade de fibras alimentares em gramas.
# MAGIC
# MAGIC #### Colunas retornadas
# MAGIC
# MAGIC | Coluna | Descrição |
# MAGIC |---|---|
# MAGIC | **alimento** | Nome do alimento (de `dim_alimento`) |
# MAGIC | **fonte** | Origem dos dados — ex.: TACO, USDA (de `dim_fonte`) |
# MAGIC | **fibras_alimentar** | Quantidade de fibras alimentares em gramas (de `fato_nutricao`) |
# MAGIC | **valor_calorico** | Valor calórico do alimento em kcal (de `fato_nutricao`) |
# MAGIC
# MAGIC #### Como interpretar
# MAGIC
# MAGIC - **Quanto maior** o valor de `fibras_alimentar`, **mais rico** é o alimento em fibras.
# MAGIC - A consulta filtra apenas alimentos com `fibras_alimentar IS NOT NULL` para excluir registros sem informação de fibras.
# MAGIC - Os resultados estão ordenados de forma **decrescente**, do maior para o menor teor de fibras.
# MAGIC
# MAGIC #### Insight
# MAGIC
# MAGIC Alimentos com alto teor de fibras são especialmente indicados para:
# MAGIC - Promoção da **saciedade** e controle do apetite
# MAGIC - Melhoria do **trânsito intestinal** e saúde digestiva
# MAGIC - Regulação dos **níveis de glicemia** e colesterol
# MAGIC - Dietas de **emagrecimento** com maior qualidade nutricional
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Justificativa de Resposta à Questão 02
# MAGIC
# MAGIC A **Questão 02** solicitava a identificação dos **itens mais ricos em fibras por porção** — ou seja, aqueles que apresentam a maior quantidade de fibras alimentares.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### Pontos-chave que garantem o atendimento
# MAGIC
# MAGIC | Critério da questão | Como foi atendido |
# MAGIC |---|---|
# MAGIC | Identificar alimentos mais ricos em fibras | Consulta SQL seleciona `fibras_alimentar` e ordena de forma decrescente |
# MAGIC | Origem dos dados | `fato_nutricao` (fn) com JOIN em `dim_alimento` (d) e `dim_fonte` (f) |
# MAGIC | Evitar registros sem informação de fibras | Filtro `WHERE fibras_alimentar IS NOT NULL` |
# MAGIC | Persistir o resultado para reuso | View criada no schema `analise` com `CREATE OR REPLACE VIEW` |
# MAGIC | Facilitar a interpretação | Gráfico de colunas com rótulos nas barras |
# MAGIC
# MAGIC Dessa forma, a análise não apenas **identificou e ranqueou** os alimentos mais ricos em fibras, mas também **disponibilizou o resultado em uma view persistente** e em uma **visualização gráfica**, cumprindo integralmente o objetivo da Questão 02.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2.3 - Questão 03 - Maior densidade nutricional (micronutrientes por caloria)

# COMMAND ----------

# DBTITLE 1,Questão 03 - Maior densidade nutricional (micronutrientes por caloria)
# MAGIC %sql
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC -- Análises Nutricionais - Tabelas gold.fato_nutricao + dimensões
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC
# MAGIC -- ===========================================================================
# MAGIC -- 3. Maior densidade nutricional (micronutrientes por caloria)
# MAGIC -- ===========================================================================
# MAGIC SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.densidade_nutritiva, fn.valor_calorico
# MAGIC FROM MVP_ENG_DADOS.gold.fato_nutricao fn
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
# MAGIC WHERE fn.densidade_nutritiva IS NOT NULL
# MAGIC ORDER BY fn.densidade_nutritiva DESC
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# DBTITLE 1,VIEW - maior densidade nutritiva
spark.sql("""
CREATE OR REPLACE VIEW MVP_ENG_DADOS.analise.vw_maior_densidade_nutritiva AS
SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.densidade_nutritiva, fn.valor_calorico
FROM MVP_ENG_DADOS.gold.fato_nutricao fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
WHERE fn.densidade_nutritiva IS NOT NULL
""")

spark.sql("""
SELECT alimento, fonte, densidade_nutritiva, valor_calorico
FROM MVP_ENG_DADOS.analise.vw_maior_densidade_nutritiva
ORDER BY densidade_nutritiva DESC
LIMIT 10
""").display()

# COMMAND ----------

# DBTITLE 1,Gráfico -  maior densidade nutritiva
import matplotlib.pyplot as plt

# Consulta os dados da view criada na célula acima
df = spark.sql("""
    SELECT alimento, fonte, densidade_nutritiva, valor_calorico
    FROM MVP_ENG_DADOS.analise.vw_maior_densidade_nutritiva
    ORDER BY densidade_nutritiva DESC
    LIMIT 10
""").toPandas()

# Combina alimento e fonte para o rótulo do eixo X
df['alimento_fonte'] = df['alimento'] + '\n(' + df['fonte'] + ')'

# Gráfico de colunas: Densidade Nutritiva
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['alimento_fonte'], df['densidade_nutritiva'], color='darkorange', edgecolor='saddlebrown')
ax.set_title('Top 10 Alimentos: Maior Densidade Nutricional (Micronutrientes por Caloria)', fontsize=14, fontweight='bold')
ax.set_xlabel('Alimento (Fonte)', fontsize=11)
ax.set_ylabel('Densidade Nutritiva', fontsize=11)
ax.set_xticks(range(len(df['alimento_fonte'])))
ax.set_xticklabels(df['alimento_fonte'], rotation=45, ha='right')

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1,
            f'{height:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC    
# MAGIC #### 5.2.3.1 - Explicação do Resultado
# MAGIC
# MAGIC A consulta acima retorna os **10 alimentos com a maior densidade nutricional**, ou seja, aqueles que apresentam a maior concentração de micronutrientes por caloria consumida.
# MAGIC
# MAGIC #### Colunas retornadas
# MAGIC
# MAGIC | Coluna | Descrição |
# MAGIC |---|---|
# MAGIC | **alimento** | Nome do alimento (de `dim_alimento`) |
# MAGIC | **fonte** | Origem dos dados — ex.: TACO, USDA (de `dim_fonte`) |
# MAGIC | **densidade_nutritiva** | Índice de densidade nutritiva — micronutrientes por caloria (de `fato_nutricao`) |
# MAGIC | **valor_calorico** | Valor calórico do alimento em kcal (de `fato_nutricao`) |
# MAGIC
# MAGIC #### Como interpretar
# MAGIC
# MAGIC - **Quanto maior** o valor de `densidade_nutritiva`, **mais rico** é o alimento em micronutrientes em relação às calorias fornecidas.
# MAGIC - A consulta filtra apenas alimentos com `densidade_nutritiva IS NOT NULL` para excluir registros sem informação de densidade.
# MAGIC - Os resultados estão ordenados de forma **decrescente**, do maior para o menor índice de densidade nutritiva.
# MAGIC
# MAGIC #### Insight
# MAGIC
# MAGIC Alimentos com alta densidade nutricional são especialmente indicados para:
# MAGIC - Dietas com foco em **maximum nutrition per calorie** — obter o máximo de vitaminas e minerais com o menor custo calórico
# MAGIC - Planos alimentares de **reeducação alimentar** com melhora da qualidade nutricional
# MAGIC - Estratégias de **prevenção de deficiências de micronutrientes** (ferro, cálcio, vitaminas, etc.)
# MAGIC - Dietas de **emagrecimento** com preservação da adequação nutricional
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Justificativa de Resposta à Questão 03
# MAGIC
# MAGIC A **Questão 03** solicitava a identificação dos **alimentos com a maior densidade nutricional (micronutrientes por caloria)** — ou seja, aqueles que entregam a maior concentração de micronutrientes a cada caloria consumida.
# MAGIC
# MAGIC
# MAGIC
# MAGIC #### Pontos-chave que garantem o atendimento
# MAGIC
# MAGIC | Critério da questão | Como foi atendido |
# MAGIC |---|---|
# MAGIC | Identificar alimentos com maior densidade nutricional | Consulta SQL seleciona `densidade_nutritiva` e ordena de forma decrescente |
# MAGIC | Origem dos dados | `fato_nutricao` (fn) com JOIN em `dim_alimento` (d) e `dim_fonte` (f) |
# MAGIC | Evitar registros sem informação de densidade | Filtro `WHERE densidade_nutritiva IS NOT NULL` |
# MAGIC | Persistir o resultado para reuso | View criada no schema `analise` com `CREATE OR REPLACE VIEW` |
# MAGIC | Facilitar a interpretação | Gráfico de colunas com rótulos nas barras |
# MAGIC
# MAGIC Dessa forma, a análise não apenas **identificou e ranqueou** os alimentos com maior densidade nutricional, mas também **disponibilizou o resultado em uma view persistente** e em uma **visualização gráfica**, cumprindo integralmente o objetivo da Questão 03.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2.4 - Questão 04 - Opções com maior teor de sódio

# COMMAND ----------

# DBTITLE 1,Questão 04 - Opções com maior teor de sódio
# MAGIC %sql
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC -- Análises Nutricionais - Tabelas gold.fato_nutricao + dimensões
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC
# MAGIC -- ===========================================================================
# MAGIC -- 4. Opções com maior teor de sódio
# MAGIC -- ===========================================================================
# MAGIC SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.sodio, fn.valor_calorico
# MAGIC FROM MVP_ENG_DADOS.gold.fato_nutricao fn
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
# MAGIC WHERE fn.sodio IS NOT NULL
# MAGIC ORDER BY fn.sodio DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,VIEW - maior sódio
spark.sql("""
CREATE OR REPLACE VIEW MVP_ENG_DADOS.analise.vw_maior_sodio AS
SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.sodio, fn.valor_calorico
FROM MVP_ENG_DADOS.gold.fato_nutricao fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
WHERE fn.sodio IS NOT NULL
""")

spark.sql("""
SELECT alimento, fonte, sodio, valor_calorico
FROM MVP_ENG_DADOS.analise.vw_maior_sodio
ORDER BY sodio DESC
LIMIT 10
""").display()

# COMMAND ----------

# DBTITLE 1,Gráfico - maior sódio  
import matplotlib.pyplot as plt

# Consulta os dados da view criada na célula acima
df = spark.sql("""
    SELECT alimento, fonte, sodio, valor_calorico
    FROM MVP_ENG_DADOS.analise.vw_maior_sodio
    ORDER BY sodio DESC
    LIMIT 10
"""
).toPandas()

# Combina alimento e fonte para o rótulo do eixo X
df['alimento_fonte'] = df['alimento'] + '\n(' + df['fonte'] + ')'

# Gráfico de colunas: Menor Teor de Sódio
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['alimento_fonte'], df['sodio'], color='mediumslateblue', edgecolor='indigo')
ax.set_title('Top 10 Alimentos: Maior Teor de Sódio', fontsize=14, fontweight='bold')
ax.set_xlabel('Alimento (Fonte)', fontsize=11)
ax.set_ylabel('Sódio (mg)', fontsize=11)
ax.set_xticks(range(len(df['alimento_fonte'])))
ax.set_xticklabels(df['alimento_fonte'], rotation=45, ha='right')

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1,
            f'{height:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 5.2.4.1 - Explicação do Resultado
# MAGIC
# MAGIC A consulta acima retorna os **10 alimentos com o maior teor de sódio**, ou seja, aqueles que apresentam a maior quantidade de sódio em miligramas por porção.
# MAGIC
# MAGIC #### Colunas retornadas
# MAGIC
# MAGIC | Coluna | Descrição |
# MAGIC |---|---|
# MAGIC | **alimento** | Nome do alimento (de `dim_alimento`) |
# MAGIC | **fonte** | Origem dos dados — ex.: TACO, USDA (de `dim_fonte`) |
# MAGIC | **sodio** | Quantidade de sódio em miligramas — mg (de `fato_nutricao`) |
# MAGIC | **valor_calorico** | Valor calórico do alimento em kcal (de `fato_nutricao`) |
# MAGIC
# MAGIC #### Como interpretar
# MAGIC
# MAGIC - **Quanto maior** o valor de `sodio`, **mais elevado** é o teor de sódio do alimento.
# MAGIC - A consulta filtra apenas alimentos com `sodio IS NOT NULL` para excluir registros sem informação de sódio.
# MAGIC - Os resultados estão ordenados de forma **decrescente**, do maior para o menor teor de sódio.
# MAGIC
# MAGIC #### Insight
# MAGIC
# MAGIC Alimentos com alto teor de sódio merecem atenção especial, pois o consumo excessivo está associado a:
# MAGIC - Aumento da **pressão arterial** e risco de hipertensão
# MAGIC - Maior probabilidade de **doenças cardiovasculares**
# MAGIC - Retenção de **líquidos** e inchaço
# MAGIC - Sobrecarga **renal** em indivíduos sensíveis
# MAGIC
# MAGIC Identificar esses alimentos é fundamental para orientar dietas com **redução de sódio**, especialmente para pacientes hipertensos e com restrições médicas.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Justificativa de Resposta à Questão 04
# MAGIC
# MAGIC A **Questão 04** solicitava a identificação das **opções com maior teor de sódio** — ou seja, aqueles alimentos que apresentam a maior quantidade de sódio por porção.
# MAGIC
# MAGIC #### Pontos-chave que garantem o atendimento
# MAGIC
# MAGIC | Critério da questão | Como foi atendido |
# MAGIC |---|---|
# MAGIC | Identificar alimentos com maior teor de sódio | Consulta SQL seleciona `sodio` e ordena de forma decrescente |
# MAGIC | Origem dos dados | `fato_nutricao` (fn) com JOIN em `dim_alimento` (d) e `dim_fonte` (f) |
# MAGIC | Evitar registros sem informação de sódio | Filtro `WHERE sodio IS NOT NULL` |
# MAGIC | Persistir o resultado para reuso | View criada no schema `analise` com `CREATE OR REPLACE VIEW` |
# MAGIC | Facilitar a interpretação | Gráfico de colunas com rótulos nas barras |
# MAGIC
# MAGIC Dessa forma, a análise não apenas **identificou e ranqueou** os alimentos com maior teor de sódio, mas também **disponibilizou o resultado em uma view persistente** e em uma **visualização gráfica**, cumprindo integralmente o objetivo da Questão 04.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2.5 - Questão 05 - Alimentos mais adequados para dietas low-carb

# COMMAND ----------

# DBTITLE 1,Questão 05 - Alimentos mais adequados para dietas low-carb
# MAGIC %sql
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC -- Análises Nutricionais - Tabelas gold.fato_nutricao + dimensões
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC
# MAGIC -- ===========================================================================
# MAGIC -- 5. Alimentos mais adequados para dietas low-carb
# MAGIC -- ===========================================================================
# MAGIC SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.carboidratos,
# MAGIC        ROUND(fn.carboidratos * 4 / fn.valor_calorico * 100, 2) AS proporcao_carb_pct,
# MAGIC        fn.proteina, fn.gordura, fn.valor_calorico
# MAGIC FROM MVP_ENG_DADOS.gold.fato_nutricao fn
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
# MAGIC WHERE fn.carboidratos IS NOT NULL AND fn.valor_calorico > 0
# MAGIC ORDER BY fn.carboidratos ASC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,VIEW - low carb
spark.sql("""
CREATE OR REPLACE VIEW MVP_ENG_DADOS.analise.vw_low_carb AS
SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.carboidratos,
       ROUND(fn.carboidratos * 4 / fn.valor_calorico * 100, 2) AS proporcao_carb_pct,
       fn.proteina, fn.gordura, fn.valor_calorico
FROM MVP_ENG_DADOS.gold.fato_nutricao fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
WHERE fn.carboidratos IS NOT NULL AND fn.valor_calorico > 0
""")

spark.sql("""
SELECT alimento, fonte, carboidratos, proporcao_carb_pct, proteina, gordura, valor_calorico
FROM MVP_ENG_DADOS.analise.vw_low_carb
ORDER BY carboidratos ASC
LIMIT 10
""").display()

# COMMAND ----------

# DBTITLE 1,Gráfico - low carb
import matplotlib.pyplot as plt

# Consulta os dados da view criada na célula acima
df = spark.sql("""
    SELECT alimento, fonte, carboidratos, proporcao_carb_pct, proteina, gordura, valor_calorico
    FROM MVP_ENG_DADOS.analise.vw_low_carb
    ORDER BY carboidratos ASC
    LIMIT 10
""").toPandas()

# Combina alimento e fonte para o rótulo do eixo X
df['alimento_fonte'] = df['alimento'] + '\n(' + df['fonte'] + ')'

# Gráfico de colunas: Alimentos mais adequados para dietas low-carb
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['alimento_fonte'], df['carboidratos'], color='teal', edgecolor='darkslategray')
ax.set_title('Top 10 Alimentos: Mais Adequados para Dietas Low-Carb', fontsize=14, fontweight='bold')
ax.set_xlabel('Alimento (Fonte)', fontsize=11)
ax.set_ylabel('Carboidratos (g)', fontsize=11)
ax.set_xticks(range(len(df['alimento_fonte'])))
ax.set_xticklabels(df['alimento_fonte'], rotation=45, ha='right')

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
            f'{height:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC    
# MAGIC #### 5.2.5.1 - Explicação do Resultado
# MAGIC
# MAGIC A consulta acima retorna os **10 alimentos mais adequados para dietas low-carb**, ou seja, aqueles que apresentam a **menor quantidade de carboidratos** por porção, juntamente com a proporção de carboidratos em relação ao valor calórico total.
# MAGIC
# MAGIC #### Colunas retornadas
# MAGIC
# MAGIC | Coluna | Descrição |
# MAGIC |---|---|
# MAGIC | **alimento** | Nome do alimento (de `dim_alimento`) |
# MAGIC | **fonte** | Origem dos dados — ex.: TACO, USDA (de `dim_fonte`) |
# MAGIC | **carboidratos** | Quantidade de carboidratos em gramas — g (de `fato_nutricao`) |
# MAGIC | **proporcao_carb_pct** | Proporção de carboidratos em relação ao valor calórico — % (calculado: `carboidratos * 4 / valor_calorico * 100`) |
# MAGIC | **proteina** | Quantidade de proteína em gramas — g (de `fato_nutricao`) |
# MAGIC | **gordura** | Quantidade de gordura total em gramas — g (de `fato_nutricao`) |
# MAGIC | **valor_calorico** | Valor calórico do alimento em kcal (de `fato_nutricao`) |
# MAGIC
# MAGIC #### Como interpretar
# MAGIC
# MAGIC - **Quanto menor** o valor de `carboidratos`, **mais adequado** é o alimento para dietas low-carb.
# MAGIC - A coluna `proporcao_carb_pct` mostra o percentual de calorias provenientes de carboidratos (cada grama de carboidrato ≈ 4 kcal).
# MAGIC - A consulta filtra alimentos com `carboidratos IS NOT NULL AND valor_calorico > 0` para garantir resultados válidos.
# MAGIC - Os resultados estão ordenados de forma **crescente**, do menor para o maior teor de carboidratos.
# MAGIC - As colunas `proteina` e `gordura` permitem avaliar o equilíbrio macronutricional do alimento.
# MAGIC
# MAGIC #### Insight
# MAGIC
# MAGIC Alimentos com baixo teor de carboidratos são especialmente indicados para:
# MAGIC - Dietas **low-carb** com redução de carboidratos para controle glicêmico
# MAGIC - Planos alimentares de **emagrecimento** com foco em gordura e proteína como fontes energéticas
# MAGIC - Dietas **cetogênicas (keto)** que restringem severamente a ingestão de carboidratos
# MAGIC - Controle de **diabetes** e resistência à insulina
# MAGIC - Manutenção da **saciedade** com menor impacto sobre a glicemia
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Justificativa de Resposta à Questão 05
# MAGIC
# MAGIC A **Questão 05** solicitava a identificação dos **alimentos mais adequados para dietas low-carb** — ou seja, aqueles que apresentam o menor teor de carboidratos por porção.
# MAGIC
# MAGIC #### Pontos-chave que garantem o atendimento
# MAGIC
# MAGIC | Critério da questão | Como foi atendido |
# MAGIC |---|---|
# MAGIC | Identificar alimentos com menor teor de carboidratos | Consulta SQL seleciona `carboidratos` e ordena de forma crescente |
# MAGIC | Origem dos dados | `fato_nutricao` (fn) com JOIN em `dim_alimento` (d) e `dim_fonte` (f) |
# MAGIC | Calcular a proporção de carboidratos sobre as calorias | Coluna calculada `proporcao_carb_pct` usando `ROUND(carboidratos * 4 / valor_calorico * 100, 2)` |
# MAGIC | Evitar registros sem informação de carboidratos | Filtro `WHERE carboidratos IS NOT NULL AND valor_calorico > 0` |
# MAGIC | Disponibilizar macronutrientes complementares | Colunas `proteina`, `gordura` e `valor_calorico` incluídas |
# MAGIC | Persistir o resultado para reuso | View criada no schema `analise` com `CREATE OR REPLACE VIEW` |
# MAGIC | Facilitar a interpretação | Gráfico de colunas com rótulos nas barras |
# MAGIC
# MAGIC Dessa forma, a análise não apenas **identificou e ranqueou** os alimentos mais adequados para dietas low-carb, mas também **disponibilizou o resultado em uma view persistente** e em uma **visualização gráfica**, cumprindo integralmente o objetivo da Questão 05.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2.6 - Questão 06 - Itens com maior quantidade de gorduras saturadas

# COMMAND ----------

# DBTITLE 1,Questão 06 - Itens com maior quantidade de gorduras saturadas
# MAGIC %sql
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC -- Análises Nutricionais - Tabelas gold.fato_nutricao + dimensões
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC
# MAGIC -- ===========================================================================
# MAGIC -- 6. Itens com maior quantidade de gorduras saturadas
# MAGIC -- ===========================================================================
# MAGIC SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.gordura_saturada, fn.gordura, fn.valor_calorico
# MAGIC FROM MVP_ENG_DADOS.gold.fato_nutricao fn
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
# MAGIC WHERE fn.gordura_saturada IS NOT NULL
# MAGIC ORDER BY fn.gordura_saturada DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,VIEW - gordura saturada
spark.sql("""
CREATE OR REPLACE VIEW MVP_ENG_DADOS.analise.vw_maior_gordura_saturada AS
SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.gordura_saturada, fn.gordura, fn.valor_calorico
FROM MVP_ENG_DADOS.gold.fato_nutricao fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
WHERE fn.gordura_saturada IS NOT NULL
""")

spark.sql("""
SELECT alimento, fonte, gordura_saturada, gordura, valor_calorico
FROM MVP_ENG_DADOS.analise.vw_maior_gordura_saturada
ORDER BY gordura_saturada DESC
LIMIT 10
""").display()

# COMMAND ----------

# DBTITLE 1,Gráfico - gordura saturada 
import matplotlib.pyplot as plt

# Consulta os dados da view criada na célula acima
df = spark.sql("""
    SELECT alimento, fonte, gordura_saturada, gordura, valor_calorico
    FROM MVP_ENG_DADOS.analise.vw_maior_gordura_saturada
    ORDER BY gordura_saturada DESC
    LIMIT 10
""").toPandas()

# Combina alimento e fonte para o rótulo do eixo X
df['alimento_fonte'] = df['alimento'] + '\n(' + df['fonte'] + ')'

# Gráfico de colunas: Maior Teor de Gordura Saturada
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['alimento_fonte'], df['gordura_saturada'], color='firebrick', edgecolor='darkred')
ax.set_title('Top 10 Alimentos: Maior Teor de Gordura Saturada', fontsize=14, fontweight='bold')
ax.set_xlabel('Alimento (Fonte)', fontsize=11)
ax.set_ylabel('Gordura Saturada (g)', fontsize=11)
ax.set_xticks(range(len(df['alimento_fonte'])))
ax.set_xticklabels(df['alimento_fonte'], rotation=45, ha='right')

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1,
            f'{height:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 5.2.6.1 - Explicação do Resultado
# MAGIC
# MAGIC A consulta acima retorna os **10 alimentos com o maior teor de gordura saturada**, ou seja, aqueles que apresentam a maior quantidade de gordura saturada em gramas por porção, juntamente com a gordura total e o valor calórico.
# MAGIC
# MAGIC #### Colunas retornadas
# MAGIC
# MAGIC | Coluna | Descrição |
# MAGIC |---|---|
# MAGIC | **alimento** | Nome do alimento (de `dim_alimento`) |
# MAGIC | **fonte** | Origem dos dados — ex.: TACO, USDA (de `dim_fonte`) |
# MAGIC | **gordura_saturada** | Quantidade de gordura saturada em gramas — g (de `fato_nutricao`) |
# MAGIC | **gordura** | Quantidade de gordura total em gramas — g (de `fato_nutricao`) |
# MAGIC | **valor_calorico** | Valor calórico do alimento em kcal (de `fato_nutricao`) |
# MAGIC
# MAGIC #### Como interpretar
# MAGIC
# MAGIC - **Quanto maior** o valor de `gordura_saturada`, **mais elevado** é o teor de gordura saturada do alimento.
# MAGIC - A consulta filtra apenas alimentos com `gordura_saturada IS NOT NULL` para excluir registros sem informação de gordura saturada.
# MAGIC - Os resultados estão ordenados de forma **decrescente**, do maior para o menor teor de gordura saturada.
# MAGIC - A coluna `gordura` permite comparar a gordura saturada com a gordura total, evidenciando a proporção de gordura saturada no perfil lipídico do alimento.
# MAGIC
# MAGIC #### Insight
# MAGIC
# MAGIC Alimentos com alto teor de gordura saturada merecem atenção especial, pois o consumo excessivo está associado a:
# MAGIC - Aumento do **colesterol LDL** ("colesterol ruim")
# MAGIC - Maior risco de **doenças cardiovasculares**, como aterosclerose e infarto
# MAGIC - Acúmulo de **placas de gordura** nas artérias
# MAGIC - Maior probabilidade de **obesidade** e dislipidemias
# MAGIC
# MAGIC Identificar esses alimentos é fundamental para orientar dietas com **redução de gordura saturada**, especialmente para pacientes com dislipidemias, risco cardiovascular e restrições médicas.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Justificativa de Resposta à Questão 06
# MAGIC
# MAGIC A **Questão 06** solicitava a identificação dos **itens com maior quantidade de gorduras saturadas** — ou seja, aqueles alimentos que apresentam a maior quantidade de gordura saturada por porção.
# MAGIC
# MAGIC #### Pontos-chave que garantem o atendimento
# MAGIC
# MAGIC | Critério da questão | Como foi atendido |
# MAGIC |---|---|
# MAGIC | Identificar alimentos com maior teor de gordura saturada | Consulta SQL seleciona `gordura_saturada` e ordena de forma decrescente |
# MAGIC | Origem dos dados | `fato_nutricao` (fn) com JOIN em `dim_alimento` (d) e `dim_fonte` (f) |
# MAGIC | Evitar registros sem informação de gordura saturada | Filtro `WHERE gordura_saturada IS NOT NULL` |
# MAGIC | Disponibilizar gordura total e valor calórico complementares | Colunas `gordura` e `valor_calorico` incluídas |
# MAGIC | Persistir o resultado para reuso | View criada no schema `analise` com `CREATE OR REPLACE VIEW` |
# MAGIC | Facilitar a interpretação | Gráfico de colunas com rótulos nas barras |
# MAGIC
# MAGIC Dessa forma, a análise não apenas **identificou e ranqueou** os alimentos com maior teor de gordura saturada, mas também **disponibilizou o resultado em uma view persistente** e em uma **visualização gráfica**, cumprindo integralmente o objetivo da Questão 06.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2.7 - Questão 07 - Alimentos mais indicados para ganho de massa muscular

# COMMAND ----------

# DBTITLE 1,Questão 07 - Alimentos mais indicados para ganho de massa muscular
# MAGIC %sql
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC -- Análises Nutricionais - Tabelas gold.fato_nutricao + dimensões
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC
# MAGIC -- ===========================================================================
# MAGIC -- 7. Alimentos mais indicados para ganho de massa muscular
# MAGIC -- ===========================================================================
# MAGIC SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.proteina, fn.valor_calorico, fn.carboidratos, fn.gordura,
# MAGIC        ROUND(fn.proteina * (fn.valor_calorico / 100), 2) AS score_muscular
# MAGIC FROM MVP_ENG_DADOS.gold.fato_nutricao fn
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
# MAGIC WHERE fn.proteina IS NOT NULL
# MAGIC ORDER BY score_muscular DESC
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# DBTITLE 1,VIEW - maior massa muscular
spark.sql("""
CREATE OR REPLACE VIEW MVP_ENG_DADOS.analise.vw_maior_massa_muscular AS
SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.proteina, fn.valor_calorico, fn.carboidratos, fn.gordura,
       ROUND(fn.proteina * (fn.valor_calorico / 100), 2) AS score_muscular
FROM MVP_ENG_DADOS.gold.fato_nutricao fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
WHERE fn.proteina IS NOT NULL
""")

spark.sql("""
SELECT alimento, fonte, proteina, valor_calorico, carboidratos, gordura, score_muscular
FROM MVP_ENG_DADOS.analise.vw_maior_massa_muscular
ORDER BY score_muscular DESC
LIMIT 10
""").display()

# COMMAND ----------

# DBTITLE 1,Gráfico - maior massa muscular 
import matplotlib.pyplot as plt

# Consulta os dados da view criada na célula acima
df = spark.sql("""
    SELECT alimento, fonte, proteina, valor_calorico, carboidratos, gordura, score_muscular
    FROM MVP_ENG_DADOS.analise.vw_maior_massa_muscular
    ORDER BY score_muscular DESC
    LIMIT 10
""").toPandas()

# Combina alimento e fonte para o rótulo do eixo X
df['alimento_fonte'] = df['alimento'] + '\n(' + df['fonte'] + ')'

# Gráfico de colunas: Alimentos mais indicados para ganho de massa muscular
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['alimento_fonte'], df['score_muscular'], color='steelblue', edgecolor='navy')
ax.set_title('Top 10 Alimentos: Mais Indicados para Ganho de Massa Muscular', fontsize=14, fontweight='bold')
ax.set_xlabel('Alimento (Fonte)', fontsize=11)
ax.set_ylabel('Score Muscular', fontsize=11)
ax.set_xticks(range(len(df['alimento_fonte'])))
ax.set_xticklabels(df['alimento_fonte'], rotation=45, ha='right')

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1,
            f'{height:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 5.2.7.1 - Explicação do Resultado
# MAGIC
# MAGIC A consulta acima retorna os **10 alimentos mais indicados para ganho de massa muscular**, ou seja, aqueles que apresentam a maior combinação de proteína e valor calórico por porção, refletida pelo score muscular calculado.
# MAGIC
# MAGIC #### Colunas retornadas
# MAGIC
# MAGIC | Coluna | Descrição |
# MAGIC |---|---|
# MAGIC | **alimento** | Nome do alimento (de `dim_alimento`) |
# MAGIC | **fonte** | Origem dos dados — ex.: TACO, USDA (de `dim_fonte`) |
# MAGIC | **proteina** | Quantidade de proteína em gramas — g (de `fato_nutricao`) |
# MAGIC | **valor_calorico** | Valor calórico do alimento em kcal (de `fato_nutricao`) |
# MAGIC | **carboidratos** | Quantidade de carboidratos em gramas — g (de `fato_nutricao`) |
# MAGIC | **gordura** | Quantidade de gordura total em gramas — g (de `fato_nutricao`) |
# MAGIC | **score_muscular** | Índice que combina proteína e valor calórico (calculado: `proteina * (valor_calorico / 100)`) |
# MAGIC
# MAGIC #### Como interpretar
# MAGIC
# MAGIC - **Quanto maior** o valor de `score_muscular`, **mais indicado** é o alimento para ganho de massa muscular.
# MAGIC - O score combina a quantidade de proteína com o valor calórico, refletindo alimentos que oferecem **alta densidade proteica aliada a energia suficiente** para hipertrofia.
# MAGIC - A consulta filtra apenas alimentos com `proteina IS NOT NULL` para excluir registros sem informação de proteína.
# MAGIC - Os resultados estão ordenados de forma **decrescente**, do maior para o menor score muscular.
# MAGIC - As colunas `carboidratos` e `gordura` permitem avaliar o equilíbrio macronutricional do alimento.
# MAGIC
# MAGIC #### Insight
# MAGIC
# MAGIC Alimentos com alto score muscular são especialmente indicados para:
# MAGIC - **Hipertrofia** e ganho de massa muscular em treinos de força
# MAGIC - Dietas de **superávit calórico** com foco em proteína de alto valor biológico
# MAGIC - **Recuperação muscular** pós-treino, favorecendo a síntese proteica
# MAGIC - Planos alimentares de **bulking** com balanceamento entre proteína e energia
# MAGIC - Atletas e praticantes de musculação que necessitam de **alta ingestão proteica**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Justificativa de Resposta à Questão 07
# MAGIC
# MAGIC A **Questão 07** solicitava a identificação dos **alimentos mais indicados para ganho de massa muscular** — ou seja, aqueles que combinam alto teor de proteína com valor calórico adequado.
# MAGIC
# MAGIC #### Pontos-chave que garantem o atendimento
# MAGIC
# MAGIC | Critério da questão | Como foi atendido |
# MAGIC |---|---|
# MAGIC | Identificar alimentos com alto teor de proteína | Consulta SQL seleciona `proteina` como critério principal |
# MAGIC | Combinar proteína com valor calórico | Coluna calculada `score_muscular` usando `ROUND(proteina * (valor_calorico / 100), 2)` |
# MAGIC | Origem dos dados | `fato_nutricao` (fn) com JOIN em `dim_alimento` (d) e `dim_fonte` (f) |
# MAGIC | Evitar registros sem informação de proteína | Filtro `WHERE proteina IS NOT NULL` |
# MAGIC | Disponibilizar macronutrientes complementares | Colunas `carboidratos`, `gordura` e `valor_calorico` incluídas |
# MAGIC | Persistir o resultado para reuso | View criada no schema `analise` com `CREATE OR REPLACE VIEW` |
# MAGIC | Facilitar a interpretação | Gráfico de colunas com rótulos nas barras |
# MAGIC
# MAGIC Dessa forma, a análise não apenas **identificou e ranqueou** os alimentos mais indicados para ganho de massa muscular, mas também **disponibilizou o resultado em uma view persistente** e em uma **visualização gráfica**, cumprindo integralmente o objetivo da Questão 07.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2.8 - Questão 08 - Mais eficientes para saciedade com poucas calorias

# COMMAND ----------

# DBTITLE 1,Questão 08 - Mais eficientes para saciedade com poucas calorias
# MAGIC %sql
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC -- Análises Nutricionais - Tabelas gold.fato_nutricao + dimensões
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC
# MAGIC -- ===========================================================================
# MAGIC -- 8. Mais eficientes para saciedade com poucas calorias
# MAGIC -- ===========================================================================
# MAGIC SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.proteina, fn.fibras_alimentar, fn.valor_calorico,
# MAGIC        ROUND((fn.proteina + fn.fibras_alimentar) / fn.valor_calorico, 4) AS indice_saciedade
# MAGIC FROM MVP_ENG_DADOS.gold.fato_nutricao fn
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
# MAGIC WHERE fn.valor_calorico > 0
# MAGIC   AND fn.proteina IS NOT NULL
# MAGIC   AND fn.fibras_alimentar IS NOT NULL
# MAGIC ORDER BY indice_saciedade DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,VIEW - maior saciedade
spark.sql("""
CREATE OR REPLACE VIEW MVP_ENG_DADOS.analise.vw_maior_saciedade AS
SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.proteina, fn.fibras_alimentar, fn.valor_calorico,
       ROUND((fn.proteina + fn.fibras_alimentar) / fn.valor_calorico, 4) AS indice_saciedade
FROM MVP_ENG_DADOS.gold.fato_nutricao fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
WHERE fn.valor_calorico > 0
  AND fn.proteina IS NOT NULL
  AND fn.fibras_alimentar IS NOT NULL
""")

spark.sql("""
SELECT alimento, fonte, proteina, fibras_alimentar, valor_calorico, indice_saciedade
FROM MVP_ENG_DADOS.analise.vw_maior_saciedade
ORDER BY indice_saciedade DESC
LIMIT 10
""").display()

# COMMAND ----------

# DBTITLE 1,Gráfico - maior saciedade
import matplotlib.pyplot as plt

# Consulta os dados da view criada na célula acima
df = spark.sql("""
    SELECT alimento, fonte, proteina, fibras_alimentar, valor_calorico, indice_saciedade
    FROM MVP_ENG_DADOS.analise.vw_maior_saciedade
    ORDER BY indice_saciedade DESC
    LIMIT 10
""").toPandas()

# Combina alimento e fonte para o rótulo do eixo X
df['alimento_fonte'] = df['alimento'] + '\n(' + df['fonte'] + ')'

# Gráfico de colunas: Mais eficientes para saciedade com poucas calorias
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['alimento_fonte'], df['indice_saciedade'], color='seagreen', edgecolor='darkgreen')
ax.set_title('Top 10 Alimentos: Mais Eficientes para Saciedade com Poucas Calorias', fontsize=14, fontweight='bold')
ax.set_xlabel('Alimento (Fonte)', fontsize=11)
ax.set_ylabel('Índice de Saciedade', fontsize=11)
ax.set_xticks(range(len(df['alimento_fonte'])))
ax.set_xticklabels(df['alimento_fonte'], rotation=45, ha='right')

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.001,
            f'{height:.4f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC    
# MAGIC #### 5.2.8.1 - Explicação do Resultado
# MAGIC
# MAGIC A consulta acima retorna os **10 alimentos mais eficientes para saciedade com poucas calorias**, ou seja, aqueles que apresentam a maior combinação de proteína e fibras em relação ao valor calórico, refletida pelo índice de saciedade calculado.
# MAGIC
# MAGIC #### Colunas retornadas
# MAGIC
# MAGIC | Coluna | Descrição |
# MAGIC |---|---|
# MAGIC | **alimento** | Nome do alimento (de `dim_alimento`) |
# MAGIC | **fonte** | Origem dos dados — ex.: TACO, USDA (de `dim_fonte`) |
# MAGIC | **proteina** | Quantidade de proteína em gramas — g (de `fato_nutricao`) |
# MAGIC | **fibras_alimentar** | Quantidade de fibras alimentares em gramas — g (de `fato_nutricao`) |
# MAGIC | **valor_calorico** | Valor calórico do alimento em kcal (de `fato_nutricao`) |
# MAGIC | **indice_saciedade** | Índice que combina proteína e fibras em relação ao valor calórico (`(proteína + fibras) / valor_calórico`) |
# MAGIC
# MAGIC #### Como interpretar
# MAGIC
# MAGIC - **Quanto maior** o valor de `indice_saciedade`, **mais eficiente** é o alimento para promover saciedade com poucas calorias.
# MAGIC - O índice combina a quantidade de proteína e fibras alimentares, ambos nutrientes altamente saciantes, dividida pelo valor calórico, evidenciando alimentos que oferecem **alta saciedade por caloria consumida**.
# MAGIC - A consulta filtra apenas alimentos com `valor_calorico > 0`, `proteina IS NOT NULL` e `fibras_alimentar IS NOT NULL` para garantir resultados válidos e evitar divisão por zero.
# MAGIC - Os resultados estão ordenados de forma **decrescente**, do maior para o menor índice de saciedade.
# MAGIC - As colunas `proteina` e `fibras_alimentar` permitem avaliar a contribuição individual de cada nutriente para a saciedade.
# MAGIC
# MAGIC #### Insight
# MAGIC
# MAGIC Alimentos com alto índice de saciedade são especialmente indicados para:
# MAGIC - Dietas de **emagrecimento** com restrição calórica sem comprometer a saciedade
# MAGIC - Planos alimentares com **controle de apetite** e redução da fome entre as refeições
# MAGIC - Estratégias de **comer menos calorias** mantendo a sensação de plenitude
# MAGIC - Controle de **glicemia** com alimentos de alta densidade nutritiva e baixa densidade calórica
# MAGIC - Dietas ricas em **fibras e proteínas** para manutenção da massa magra durante o emagrecimento
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Justificativa de Resposta à Questão 08
# MAGIC
# MAGIC A **Questão 08** solicitava a identificação dos **alimentos mais eficientes para saciedade com poucas calorias** — ou seja, aqueles que combinam alto teor de proteína e fibras com baixo valor calórico.
# MAGIC
# MAGIC #### Pontos-chave que garantem o atendimento
# MAGIC
# MAGIC | Critério da questão | Como foi atendido |
# MAGIC |---|---|
# MAGIC | Identificar alimentos com alto teor de proteína e fibras | Consulta SQL seleciona `proteina` e `fibras_alimentar` como critérios principais |
# MAGIC | Combinar saciedade com baixo valor calórico | Coluna calculada `indice_saciedade` usando `ROUND((proteina + fibras_alimentar) / valor_calorico, 4)` |
# MAGIC | Origem dos dados | `fato_nutricao` (fn) com JOIN em `dim_alimento` (d) e `dim_fonte` (f) |
# MAGIC | Evitar registros sem informação ou com valor calórico zero | Filtros `WHERE valor_calorico > 0 AND proteina IS NOT NULL AND fibras_alimentar IS NOT NULL` |
# MAGIC | Disponibilizar valor calórico complementar | Coluna `valor_calorico` incluída |
# MAGIC | Persistir o resultado para reuso | View criada no schema `analise` com `CREATE OR REPLACE VIEW` |
# MAGIC | Facilitar a interpretação | Gráfico de colunas com rótulos nas barras |
# MAGIC
# MAGIC Dessa forma, a análise não apenas **identificou e ranqueou** os alimentos mais eficientes para saciedade com poucas calorias, mas também **disponibilizou o resultado em uma view persistente** e em uma **visualização gráfica**, cumprindo integralmente o objetivo da Questão 08.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2.9 - Questão 09 - Alimentos com maior quantidade de açúcar

# COMMAND ----------

# DBTITLE 1,Questão 09 - Alimentos com maior quantidade de açúcar
# MAGIC %sql
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC -- Análises Nutricionais - Tabelas gold.fato_nutricao + dimensões
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC
# MAGIC -- ===========================================================================
# MAGIC -- 9. Alimentos com maior quantidade de açúcar
# MAGIC -- ===========================================================================
# MAGIC SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.acucares, fn.carboidratos, fn.valor_calorico
# MAGIC FROM MVP_ENG_DADOS.gold.fato_nutricao fn
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
# MAGIC WHERE fn.acucares IS NOT NULL
# MAGIC ORDER BY fn.acucares DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,VIEW - maiores açucares
spark.sql("""
CREATE OR REPLACE VIEW MVP_ENG_DADOS.analise.vw_maior_acucares AS
SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.acucares, fn.carboidratos, fn.valor_calorico
FROM MVP_ENG_DADOS.gold.fato_nutricao fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
WHERE fn.acucares IS NOT NULL
""")

spark.sql("""
SELECT alimento, fonte, acucares, carboidratos, valor_calorico
FROM MVP_ENG_DADOS.analise.vw_maior_acucares
ORDER BY acucares DESC
LIMIT 10
""").display()

# COMMAND ----------

# DBTITLE 1,Gráfico - maiores açucares
import matplotlib.pyplot as plt

# Consulta os dados da view criada na célula acima
df = spark.sql("""
    SELECT alimento, fonte, acucares, carboidratos, valor_calorico
    FROM MVP_ENG_DADOS.analise.vw_maior_acucares
    ORDER BY acucares DESC
    LIMIT 10
""").toPandas()

# Combina alimento e fonte para o rótulo do eixo X
df['alimento_fonte'] = df['alimento'] + '\n(' + df['fonte'] + ')'

# Gráfico de colunas: Alimentos com maior quantidade de açúcar
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['alimento_fonte'], df['acucares'], color='darkorange', edgecolor='saddlebrown')
ax.set_title('Top 10 Alimentos: Maior Quantidade de Açúcar', fontsize=14, fontweight='bold')
ax.set_xlabel('Alimento (Fonte)', fontsize=11)
ax.set_ylabel('Açúcares (g)', fontsize=11)
ax.set_xticks(range(len(df['alimento_fonte'])))
ax.set_xticklabels(df['alimento_fonte'], rotation=45, ha='right')

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
            f'{height:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### 5.2.9.1 - Explicação do Resultado
# MAGIC
# MAGIC A consulta acima retorna os **10 alimentos com a maior quantidade de açúcar**, ou seja, aqueles que apresentam a maior quantidade de açúcares em gramas por porção, juntamente com os carboidratos totais e o valor calórico.
# MAGIC
# MAGIC #### Colunas retornadas
# MAGIC
# MAGIC | Coluna | Descrição |
# MAGIC |---|---|
# MAGIC | **alimento** | Nome do alimento (de `dim_alimento`) |
# MAGIC | **fonte** | Origem dos dados — ex.: TACO, USDA (de `dim_fonte`) |
# MAGIC | **acucares** | Quantidade de açúcares em gramas — g (de `fato_nutricao`) |
# MAGIC | **carboidratos** | Quantidade de carboidratos totais em gramas — g (de `fato_nutricao`) |
# MAGIC | **valor_calorico** | Valor calórico do alimento em kcal (de `fato_nutricao`) |
# MAGIC
# MAGIC #### Como interpretar
# MAGIC
# MAGIC - **Quanto maior** o valor de `acucares`, **mais elevado** é o teor de açúcar do alimento.
# MAGIC - A consulta filtra apenas alimentos com `acucares IS NOT NULL` para excluir registros sem informação de açúcares.
# MAGIC - Os resultados estão ordenados de forma **decrescente**, do maior para o menor teor de açúcar.
# MAGIC - A coluna `carboidratos` permite comparar os açúcares com os carboidratos totais, evidenciando a proporção de açúcares no perfil glicídico do alimento.
# MAGIC - A coluna `valor_calorico` auxilia na avaliação do impacto calórico do consumo de açúcares.
# MAGIC
# MAGIC #### Insight
# MAGIC
# MAGIC Alimentos com alto teor de açúcar merecem atenção especial, pois o consumo excessivo está associado a:
# MAGIC - Aumento rápido da **glicemia** e picos de insulina
# MAGIC - Maior risco de **diabetes tipo 2** e resistência insulínica
# MAGIC - Acúmulo de **gordura visceral** e ganho de peso
# MAGIC - Maior probabilidade de **obesidade** e síndrome metabólica
# MAGIC - Maior risco de **doenças cardiovasculares** e inflamação crônica
# MAGIC
# MAGIC Identificar esses alimentos é fundamental para orientar dietas com **redução de açúcares adicionais**, especialmente para pacientes com diabetes, resistência insulínica, obesidade e restrições médicas.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Justificativa de Resposta à Questão 09
# MAGIC
# MAGIC A **Questão 09** solicitava a identificação dos **alimentos com maior quantidade de açúcar** — ou seja, aqueles alimentos que apresentam a maior quantidade de açúcares por porção.
# MAGIC
# MAGIC #### Pontos-chave que garantem o atendimento
# MAGIC
# MAGIC | Critério da questão | Como foi atendido |
# MAGIC |---|---|
# MAGIC | Identificar alimentos com maior teor de açúcar | Consulta SQL seleciona `acucares` e ordena de forma decrescente |
# MAGIC | Origem dos dados | `fato_nutricao` (fn) com JOIN em `dim_alimento` (d) e `dim_fonte` (f) |
# MAGIC | Evitar registros sem informação de açúcares | Filtro `WHERE acucares IS NOT NULL` |
# MAGIC | Disponibilizar carboidratos totais e valor calórico complementares | Colunas `carboidratos` e `valor_calorico` incluídas |
# MAGIC | Persistir o resultado para reuso | View criada no schema `analise` com `CREATE OR REPLACE VIEW` |
# MAGIC | Facilitar a interpretação | Gráfico de colunas com rótulos nas barras |
# MAGIC
# MAGIC Dessa forma, a análise não apenas **identificou e ranqueou** os alimentos com maior teor de açúcar, mas também **disponibilizou o resultado em uma view persistente** e em uma **visualização gráfica**, cumprindo integralmente o objetivo da Questão 09.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2.10 - Questão 10 - Alimentos mais adequados para dietas veganas ou vegetarianas

# COMMAND ----------

# DBTITLE 1,Questão 10 - Alimentos mais adequados para dietas veganas ou vegetarianas
# MAGIC %sql
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC -- Análises Nutricionais - Tabelas gold.fato_nutricao + dimensões
# MAGIC -- ---------------------------------------------------------------------------
# MAGIC
# MAGIC -- ===========================================================================
# MAGIC -- 10. Alimentos mais adequados para dietas veganas ou vegetarianas
# MAGIC -- ===========================================================================
# MAGIC SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.proteina, fn.fibras_alimentar, fn.colesterol, fn.gordura_saturada,
# MAGIC        ROUND(COALESCE(fn.proteina, 0)
# MAGIC            + COALESCE(fn.fibras_alimentar, 0)
# MAGIC            - COALESCE(fn.colesterol, 0)
# MAGIC            - COALESCE(fn.gordura_saturada, 0), 2) AS score_vegano
# MAGIC FROM MVP_ENG_DADOS.gold.fato_nutricao fn
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
# MAGIC JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
# MAGIC WHERE fn.colesterol IS NULL OR fn.colesterol <= 5
# MAGIC ORDER BY score_vegano DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,VIEW - dietas veganas ou vegetarianas
spark.sql("""
CREATE OR REPLACE VIEW MVP_ENG_DADOS.analise.vw_melhor_vegano AS
SELECT d.nome_alimento AS alimento, f.nome_fonte AS fonte, fn.proteina, fn.fibras_alimentar, fn.colesterol, fn.gordura_saturada,
       ROUND(COALESCE(fn.proteina, 0)
           + COALESCE(fn.fibras_alimentar, 0)
           - COALESCE(fn.colesterol, 0)
           - COALESCE(fn.gordura_saturada, 0), 2) AS score_vegano
FROM MVP_ENG_DADOS.gold.fato_nutricao fn
JOIN MVP_ENG_DADOS.gold.dim_alimento d ON fn.alimento_id = d.alimento_id
JOIN MVP_ENG_DADOS.gold.dim_fonte f ON fn.fonte_id = f.fonte_id
WHERE fn.colesterol IS NULL OR fn.colesterol <= 5
""")

spark.sql("""
SELECT alimento, fonte, proteina, fibras_alimentar, colesterol, gordura_saturada, score_vegano
FROM MVP_ENG_DADOS.analise.vw_melhor_vegano
ORDER BY score_vegano DESC
LIMIT 10
""").display()

# COMMAND ----------

# DBTITLE 1,Gráfico - dietas veganas ou vegetarianas
import matplotlib.pyplot as plt

# Consulta os dados da view criada na célula acima
df = spark.sql("""
    SELECT alimento, fonte, proteina, fibras_alimentar, colesterol, gordura_saturada, score_vegano
    FROM MVP_ENG_DADOS.analise.vw_melhor_vegano
    ORDER BY score_vegano DESC
    LIMIT 10
""").toPandas()

# Combina alimento e fonte para o rótulo do eixo X
df['alimento_fonte'] = df['alimento'] + '\n(' + df['fonte'] + ')'

# Gráfico de colunas: Alimentos mais adequados para dietas veganas ou vegetarianas
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['alimento_fonte'], df['score_vegano'], color='forestgreen', edgecolor='darkgreen')
ax.set_title('Top 10 Alimentos: Mais Adequados para Dietas Veganas ou Vegetarianas', fontsize=14, fontweight='bold')
ax.set_xlabel('Alimento (Fonte)', fontsize=11)
ax.set_ylabel('Score Vegano', fontsize=11)
ax.set_xticks(range(len(df['alimento_fonte'])))
ax.set_xticklabels(df['alimento_fonte'], rotation=45, ha='right')

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
            f'{height:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC    
# MAGIC
# MAGIC #### 5.2.10.1 - Explicação do Resultado
# MAGIC
# MAGIC A consulta acima retorna os **10 alimentos mais adequados para dietas veganas ou vegetarianas**, ou seja, aqueles que apresentam a maior combinação de proteína e fibras alimentares, com baixo teor de colesterol e gordura saturada, refletida pelo score vegano calculado.
# MAGIC
# MAGIC #### Colunas retornadas
# MAGIC
# MAGIC | Coluna | Descrição |
# MAGIC |---|---|
# MAGIC | **alimento** | Nome do alimento (de `dim_alimento`) |
# MAGIC | **fonte** | Origem dos dados — ex.: TACO, USDA (de `dim_fonte`) |
# MAGIC | **proteina** | Quantidade de proteína em gramas — g (de `fato_nutricao`) |
# MAGIC | **fibras_alimentar** | Quantidade de fibras alimentares em gramas — g (de `fato_nutricao`) |
# MAGIC | **colesterol** | Quantidade de colesterol em miligramas — mg (de `fato_nutricao`) |
# MAGIC | **gordura_saturada** | Quantidade de gordura saturada em gramas — g (de `fato_nutricao`) |
# MAGIC | **score_vegano** | Índice que combina proteína e fibras (positivo) menos colesterol e gordura saturada (negativo) (`proteína + fibras − colesterol − gordura_saturada`) |
# MAGIC
# MAGIC #### Como interpretar
# MAGIC
# MAGIC - **Quanto maior** o valor de `score_vegano`, **mais adequado** é o alimento para dietas veganas ou vegetarianas.
# MAGIC - O score combina nutrientes benéficos (`proteina` e `fibras_alimentar`) somados, e nutrientes a evitar (`colesterol` e `gordura_saturada`) subtraídos, evidenciando alimentos de **origem vegetal com alto valor nutritivo**.
# MAGIC - A consulta filtra apenas alimentos com `colesterol IS NULL OR colesterol <= 5`, priorizando alimentos sem colesterol ou com teor muito baixo — característica típica de alimentos de origem vegetal.
# MAGIC - A função `COALESCE` é utilizada para tratar valores nulos, atribuindo zero aos nutrientes ausentes, garantindo que o cálculo do score não seja comprometido por dados faltantes.
# MAGIC - Os resultados estão ordenados de forma **decrescente**, do maior para o menor score vegano.
# MAGIC - As colunas `colesterol` e `gordura_saturada` permitem avaliar a adequação do alimento a dietas sem produtos de origem animal.
# MAGIC
# MAGIC #### Insight
# MAGIC
# MAGIC Alimentos com alto score vegano são especialmente indicados para:
# MAGIC - Dietas **veganas** (sem nenhum produto de origem animal) e **vegetarianas** (sem carne, podendo incluir derivados)
# MAGIC - Garantir **ingestão adequada de proteína** sem recorrer a fontes animais
# MAGIC - Aumentar o consumo de **fibras alimentares**, essenciais para a saúde intestinal e controle glicêmico
# MAGIC - Reduzir a ingestão de **colesterol** e **gordura saturada**, minimizando riscos cardiovasculares
# MAGIC - Planos alimentares com foco em **densidade nutritiva** e sustentabilidade ambiental
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Justificativa de Resposta à Questão 10
# MAGIC
# MAGIC A **Questão 10** solicitava a identificação dos **alimentos mais adequados para dietas veganas ou vegetarianas** — ou seja, aqueles que combinam alto teor de proteína e fibras com baixo teor de colesterol e gordura saturada.
# MAGIC
# MAGIC #### Pontos-chave que garantem o atendimento
# MAGIC
# MAGIC | Critério da questão | Como foi atendido |
# MAGIC |---|---|
# MAGIC | Identificar alimentos com alto teor de proteína e fibras | Consulta SQL seleciona `proteina` e `fibras_alimentar` como critérios positivos |
# MAGIC | Priorizar alimentos sem colesterol ou com baixo teor | Filtro `WHERE colesterol IS NULL OR colesterol <= 5` |
# MAGIC | Penalizar alimentos com colesterol e gordura saturada | Coluna calculada `score_vegano` subtrai `colesterol` e `gordura_saturada` |
# MAGIC | Origem dos dados | `fato_nutricao` (fn) com JOIN em `dim_alimento` (d) e `dim_fonte` (f) |
# MAGIC | Tratar valores nulos adequadamente | Uso de `COALESCE(..., 0)` para todos os nutrientes no cálculo do score |
# MAGIC | Persistir o resultado para reuso | View criada no schema `analise` com `CREATE OR REPLACE VIEW` |
# MAGIC | Facilitar a interpretação | Gráfico de colunas com rótulos nas barras |
# MAGIC
# MAGIC Dessa forma, a análise não apenas **identificou e ranqueou** os alimentos mais adequados para dietas veganas ou vegetarianas, mas também **disponibilizou o resultado em uma view persistente** e em uma **visualização gráfica**, cumprindo integralmente o objetivo da Questão 10.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5.3 - Evidência da Criação da VW de Analise
# MAGIC
# MAGIC ![image_1790216300539.png](./image_1790216300539.png "image_1790216300539.png")

# COMMAND ----------

# MAGIC %md
# MAGIC # 6.0 - Autoavaliação

# COMMAND ----------

# MAGIC %md
# MAGIC ##6.1 - Primeiros passos
# MAGIC
# MAGIC Escolhi e tema, pois além de ser formado no P15 da PUC em 2003, eu também fiz faculdade de gastronomia, pois é um Hobbie que eu pratico e gostaria de fazer um investimento em alimentação saudável, a partir disso comecei a elabroar o que seria necessário para isso, pesquisei sobre o assunto e a princípal para fazer uma comida suadável os macronutrientes poderia me dar uma caminho, então elaborei as 10 perguntas da sessão 1.0 - Contexto de Negócio e Perguntas.

# COMMAND ----------

# MAGIC %md
# MAGIC ##6.2 - Expectativas
# MAGIC Esperava que todas as perguntas fossem respondidas e que trouxesse alguns insights para empreender nessa nova área que estou querendo atuar. Acredito que fazendo essa pós-graduação ajudaria muito nas tomadas de decisão e no crescimento de conhecimento com o aprendizado em ciências de dados, ter o poder decisão com as informações de qualidade e análise com uma precisão alta.
# MAGIC
# MAGIC Escolhi a base de dados que utilizei nas 2 sprints anteriores para poder responder as perguntas.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##6.3 - Mudança de Rota
# MAGIC
# MAGIC Quando analisei os dados utilizados anteriormente nas 2 sprints passadas, vi que não me atenderia, pois nessa base não tinha todos os campos necessários para responder as perguntas.
# MAGIC
# MAGIC Base de dados inicial:
# MAGIC
# MAGIC ![image_1790286082234.png](./image_1790286082234.png "image_1790286082234.png")
# MAGIC
# MAGIC
# MAGIC Então fui procurar bases de dados em diferentes sites de repositórios de dados públicos e encontrei as duas bases de dados, a garimpagem foi difícil, pois ou tinham bases muito complexas com campos multivalorados com números divididos por "," e texto junto, o que demandaria muito tempo para fazer a limpeza de dados e isso fez com que eu desistisse deles, pois não teria tempo hábil.
# MAGIC
# MAGIC O problema da primeira base que eu encontrei não continham muitos dados, somente 124 linhas, então fui procurar outra fonte e encontrei a segunda com 597 linhas, então resolvi juntar as duas e com elas eu conseguiria responder as perguntas.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##6.4 - Avaliação
# MAGIC
# MAGIC Aprendi muito com a pós e principalmente com o MVP, nele pude colocar em prática o que vi nas aulas gravadas.
# MAGIC Fazendo esse projeto pude entender as dificuldades que podem aparecer durante a escolha dos dados que serão utilizados, principalmente se tiver que realizar muitas alterações na limpeza de dados e nas escolhas dos campos que devem ser utilizados para se atingir o objetivo.
# MAGIC
# MAGIC Sei que a minha base de dados não tem muitas informações, mas da forma que foi estruturado o meu projeto, fica mais fácil realizar um novo projeto com dados mais robustos, pois já tenho a espinha dorsal pronta. 
# MAGIC
# MAGIC Para Atender resolvi juntar duas bases, isso também é bom para saber as diferenças entre os dados de regiões diferentes, no caso utilizei uma base brasileira e outra estadunidense e as vezes alimentos equivalentes podem ter medidas de nutrientes diferentes em diferentes países.
# MAGIC
# MAGIC No mais fiquei muito satisfeito com o meu progresso e acredito que eu aprendi muito com o projeto.
# MAGIC
# MAGIC