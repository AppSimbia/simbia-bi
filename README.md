# SIMBIA - RPA Forms

Este projeto visa automatizar a **extração e sincronização de dados** entre o Google Sheets e o banco de dados PostgreSQL do aplicativo **SIMBIA**, garantindo que todas as informações estejam sempre atualizadas e consistentes.

---

## Funcionalidades

- Conectar à planilha do Google Forms e extrair os registros de respostas;
- Limpar e padronizar os dados (datas, números e valores nulos);
- Inserir os dados na tabela principal `pesquisa_simbia`;
- Atualizar registros existentes usando `ON CONFLICT DO UPDATE`;
- Inserir dados complementares nas tabelas relacionadas:
  - `industry_sector`
  - `industry_waste_type`
  - `industry_waste_destiny`
  - `industry_waste_influence`
  - `industry_challenge`
  - `industry_difficulty`;
- Garantir consistência e integridade no banco de dados.

---

## Modelagens

A seguir, são apresentadas as modelagens utilizadas para os bancos de dados SQL do projeto.

### Google Sheets → PostgreSQL

### Modelagem das Tabelas no Banco de Destino

<img width="1848" height="1704" alt="public" src="https://github.com/user-attachments/assets/520ba321-b178-4f25-972e-dfe523830e07" />

---

## Tabelas Contempladas

A seguir, estão as tabelas que tiveram os dados transferidos do **Google Sheets → PostgreSQL**:

- Pesquisa principal → `pesquisa_simbia`
- Setores de atuação → `industry_sector`
- Tipos de resíduos → `industry_waste_type`
- Destino dos resíduos → `industry_waste_destiny`
- Influência na escolha do destino → `industry_waste_influence`
- Desafios enfrentados → `industry_challenge`
- Dificuldades de adesão → `industry_difficulty`

Cada tabela utiliza a chave `id_pesquisa` para relacionar os dados complementares à pesquisa principal.

---

## Normalização

Durante a etapa de transformação, foram aplicados conceitos de normalização para manter a consistência dos dados.

### Pesquisa principal
- Conversão de datas brasileiras para `datetime`;
- Tratamento de valores nulos e números inteiros;
- Evitar duplicidade de registros com `ON CONFLICT DO UPDATE`.

### Tabelas complementares
- Separação de múltiplos valores em linhas distintas (ex.: setores, tipos de resíduos);
- Evitar duplicidade com `ON CONFLICT DO NOTHING`.

---

## Dependências

Para executar este projeto, você precisará instalar as seguintes bibliotecas e ferramentas:

### Python
- Python 3.12 ou superior
- gspread 6.9.0
- oauth2client 4.1.3
- psycopg2-binary 2.9.9
- python-dotenv 1.0.0

Instalação:
```bash
pip install -r requirements.txt
```

### Banco de Dados
- PostgreSQL (banco relacional de destino)

#### Criar Banco de Dados
Para criar o banco de dados, execute o script `script.sql` no seu SGBD.  
⚠️ Não se esqueça de criar previamente o banco e configurar as variáveis de ambiente no arquivo `.env`.

Exemplo de `.env`:
```bash
DB_NAME=nome_banco
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=host
DB_PORT=5432
```

---

## Outras Ferramentas

- Git
- AWS EC2 (para execução em nuvem)
- dotenv (gerenciamento seguro de variáveis de ambiente)
- Google Service Account (arquivo JSON para autenticação no Google Sheets)

---

## Autores

- [@MatheusMakita](https://github.com/MatheusMakita)
- [@Valenaantunes](https://github.com/Valenaantunes)
