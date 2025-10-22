from dotenv import load_dotenv
from os import getenv
import gspread
import psycopg2
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime



# --- Funções utilitárias ---
def clean_int(value):
    return int(value) if str(value).isdigit() else None

def clean_value(value):
    if value in ("", None):
        return None
    return value

def parse_datetime_br(value):
    """Converte data brasileira (dd/mm/yyyy hh:mm:ss) em datetime do Python"""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        return None

# --- Configuração ---
load_dotenv(dotenv_path=r"C:\Users\valentinaantunes-ieg\OneDrive - Instituto J&F\Área de Trabalho\TECH2\BI\forms_bi\.env")

# --- Autenticação Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    r"C:\Users\valentinaantunes-ieg\OneDrive - Instituto J&F\Área de Trabalho\TECH2\BI\forms_bi\rpa-forms-4bd220c5b22b.json",
    scope
)
client = gspread.authorize(creds)

# Abrir planilha
sheet = client.open("Pesquisa de Aceitação & Aplicativo Simbia (respostas)").worksheet("forms_simbia2")
rows = sheet.get_all_records()
rows = [{k.strip(): v for k, v in row.items()} for row in rows]


# --- Conexão PostgreSQL ---
conn = psycopg2.connect(
    dbname=getenv("DB_NAME"),
    user=getenv("DB_USER"),
    password=getenv("DB_PASSWORD"),
    host=getenv("DB_HOST"),
    port=getenv("DB_PORT")
)
cur = conn.cursor()

# --- Inserir dados ---
for row in rows:
    cur.execute("""
        INSERT INTO pesquisa_simbia (
            industry_size,
            industry_atuation,
            industry_location,
            has_waste_management,
            frequency_of_waste_generation,
            waste_quantity_monthly,
            incorrect_waste_disposal,
            would_use_simbia,
            would_use_match,
            would_like_picpay,
            would_like_ia,
            connect_with_other_industry, 
            has_methods_in_environmental_laws,
            uptade_other_managers, 
            see_utility_in_posts_and_doubt,
            residue_catalogue, 
            data_forms
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (data_forms) DO UPDATE SET
            industry_size = EXCLUDED.industry_size,
            industry_atuation = EXCLUDED.industry_atuation,
            industry_location = EXCLUDED.industry_location,
            has_waste_management = EXCLUDED.has_waste_management,
            frequency_of_waste_generation = EXCLUDED.frequency_of_waste_generation,
            waste_quantity_monthly = EXCLUDED.waste_quantity_monthly,
            incorrect_waste_disposal = EXCLUDED.incorrect_waste_disposal,
            would_use_simbia = EXCLUDED.would_use_simbia,
            would_use_match = EXCLUDED.would_use_match,
            would_like_picpay = EXCLUDED.would_like_picpay,
            would_like_ia = EXCLUDED.would_like_ia,
            connect_with_other_industry = EXCLUDED.connect_with_other_industry,
            has_methods_in_environmental_laws = EXCLUDED.has_methods_in_environmental_laws,
            uptade_other_managers = EXCLUDED.uptade_other_managers,
            see_utility_in_posts_and_doubt = EXCLUDED.see_utility_in_posts_and_doubt,
            residue_catalogue = EXCLUDED.residue_catalogue
        RETURNING id
    """, (
        row.get("Qual o porte da empresa em que trabalha?"),
        row.get("Onde sua empresa atua predominantemente?"),
        row.get("Em qual estado sua empresa está localizada?"),
        row.get("Sua empresa já possui algum sistema de gestão de resíduos?"),
        row.get("Qual a frequência de geração de resíduos na sua empresa?"),
        row.get("Quantos KG de resíduos sua indústria produz mensalmente"),
        row.get("Já houve práticas incorretas de descarte de resíduos na sua empresa?"),
        row.get("Você vê propósito em adotar o Simbia na sua empresa?"),
        row.get("O recurso de Match Inteligente com IA, que sugere automaticamente empresas que podem reutilizar resíduos, seria útil para sua empresa?"),
        row.get("Você teria mais confiança no app se as transações financeiras fossem realizadas dentro dele via PicPay?"),
        row.get("Uma assistente virtual (EVA), com funções como análise de demandas, recomendações inteligentes e esclarecimento de dúvidas, seria útil para sua empresa?"),
        row.get("Sua empresa estaria disposta a se conectar com outras para reaproveitamento de resíduos?"), 
        row.get("A empresa possui meios para atualizar colaboradores sobre leis ambientais ?"),
        row.get("Você acredita que seria útil um aplicativo que atualiza funcionários sobre leis ambientais vigentes?"), 
        row.get("Você considera útil um sistema de postagens onde empresas compartilhem dúvidas e desafios sobre sustentabilidade, descarte e reciclagem?"), 
        row.get("Você considera relevante ter um catálogo de resíduos com sugestões de reaproveitamento, integrado a um sistema de match e chat para colaboração entre empresas?"),
        parse_datetime_br(row.get("Carimbo de data/hora"))
    ))

    result = cur.fetchone()
    if result:
        id_simbia = result[0]
        print("Dados inseridos na tabela db_simbia")
    else:
        cur.execute("SELECT id FROM pesquisa_simbia WHERE data_forms = %s", (parse_datetime_br(row.get("Carimbo de data/hora")),))
        id_simbia = cur.fetchone()[0]
    

    # --- Dados complementares ---
    industry_sector = row.get("Qual setor de atuação da sua empresa ?")
    if industry_sector:
        for sector in industry_sector.split(","):
            cur.execute("""
                INSERT INTO industry_sector (id_pesquisa, sector)
                VALUES (%s, %s)
                ON CONFLICT (id_pesquisa, sector) DO NOTHING
            """, (id_simbia, sector.strip()))

    industry_waste_type = row.get("Quais tipos de resíduos a empresa gera em maior volume?")
    if industry_waste_type:
        for waste_type in industry_waste_type.split(","):
            cur.execute("""
                INSERT INTO industry_waste_type (id_pesquisa, waste_type)
                VALUES (%s, %s)
                ON CONFLICT (id_pesquisa, waste_type) DO NOTHING
            """, (id_simbia, waste_type.strip()))

    industry_waste_destiny = row.get("Qual destino é mais comum dado aos resíduos da sua empresa?")
    if industry_waste_destiny:
        for waste_destiny in industry_waste_destiny.split(","):
            cur.execute("""
                INSERT INTO industry_waste_destiny (id_pesquisa, waste_destiny)
                VALUES (%s, %s)
                ON CONFLICT (id_pesquisa, waste_destiny) DO NOTHING
            """, (id_simbia, waste_destiny.strip()))

    industry_waste_influence = row.get("O que mais influencia na escolha do destino dos resíduos?")
    if industry_waste_influence:
        for influence in industry_waste_influence.split(","):
            cur.execute("""
                INSERT INTO industry_waste_influence (id_pesquisa, influence)
                VALUES (%s, %s)
                ON CONFLICT (id_pesquisa, influence) DO NOTHING
            """, (id_simbia, influence.strip()))

    industry_challenge = row.get("Quais os maiores desafios enfrentados hoje na gestão de resíduos?")
    if industry_challenge:
        for challenge in industry_challenge.split(","):
            cur.execute("""
                INSERT INTO industry_challenge (id_pesquisa, challenge)
                VALUES (%s, %s)
                ON CONFLICT (id_pesquisa, challenge) DO NOTHING
            """, (id_simbia, challenge.strip()))

    industry_difficulty = row.get("O que poderia dificultar a adesão ao Simbia na sua empresa?")
    if industry_difficulty:
        for difficulty in industry_difficulty.split(","):
            cur.execute("""
                INSERT INTO industry_difficulty (id_pesquisa, difficulty)
                VALUES (%s, %s)
                ON CONFLICT (id_pesquisa, difficulty) DO NOTHING
            """, (id_simbia, difficulty.strip()))

# --- Finalizar ---
conn.commit()
cur.close()
conn.close()
