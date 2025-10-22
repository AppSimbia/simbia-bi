-- Tabela principal da pesquisa Simbia
-- Armazena as informações gerais sobre a empresa respondente
CREATE TABLE pesquisa_simbia (
    id SERIAL PRIMARY KEY, -- Identificador único da pesquisa

    -- Qual o porte da empresa em que trabalha?
    industry_size VARCHAR(50) CHECK (industry_size IN ('Microempresa','Pequena empresa','Média empresa','Grande empresa')),

    -- Onde sua empresa atua predominantemente?
    industry_atuation VARCHAR(100) CHECK (industry_atuation IN ('Apenas em um estado','Em mais de um estado, mas dentro da mesma região','Em várias regiões do Brasil')),

    -- Em qual estado sua empresa está localizada? 
    industry_location VARCHAR(100) CHECK (industry_location IN ( 'Acre (AC)','Alagoas (AL)','Amapá (AP)','Amazonas (AM)','Bahia (BA)','Ceará (CE)','Distrito Federal (DF)','Espírito Santo (ES)','Goiás (GO)','Maranhão (MA)','Mato Grosso (MT)','Mato Grosso do Sul (MS)','Minas Gerais (MG)','Pará (PA)','Paraíba (PB)','Paraná (PR)','Pernambuco (PE)','Piauí (PI)','Rio de Janeiro (RJ)','Rio Grande do Norte (RN)','Rio Grande do Sul (RS)','Rondônia (RO)','Roraima (RR)','Santa Catarina (SC)','São Paulo (SP)','Sergipe (SE)','Tocantins (TO)')),

    -- Sua empresa já possui algum sistema de gestão de resíduos?
    has_waste_management VARCHAR(50) CHECK (has_waste_management IN ('Sim','Parcialmente','Não')),

    -- Qual a frequência de geração de resíduos na sua empresa?
    frequency_of_waste_generation VARCHAR(50) CHECK (frequency_of_waste_generation IN ('Diária','Semanal','Mensal','Sazonal')),

    --Quantos KG de resíduos sua indústria produz mensalmente
    waste_quantity_monthly INT CHECK (waste_quantity_monthly >= 0),

    -- Já houve práticas incorretas de descarte de resíduos na sua empresa?
    incorrect_waste_disposal VARCHAR(50) CHECK (incorrect_waste_disposal IN ('Sim','Não','Não sei informar')),

    -- Você vê propósito em adotar o Simbia na sua empresa?
    would_use_simbia VARCHAR(50) CHECK (would_use_simbia IN ('Sim','Parcialmente','Não')),

    -- O recurso de Match Inteligente com IA, que sugere automaticamente empresas que podem reutilizar resíduos, seria útil para sua empresa?
    would_use_match VARCHAR(20) CHECK (would_use_match IN ('Sim','Não','Preciso testar antes')),

    -- Você teria mais confiança no app se as transações financeiras fossem realizadas dentro dele via PicPay? 
    would_like_picpay VARCHAR(20) CHECK (would_like_picpay IN ('Sim','Parcialmente','Não')),

    -- Uma assistente virtual (EVA), com funções como análise de demandas, recomendações inteligentes e esclarecimento de dúvidas, seria útil para sua empresa?
    would_like_ia VARCHAR(20) CHECK (would_like_ia IN ('Sim','Não','Preciso testar antes')),

    -- Sua empresa estaria disposta a se conectar com outras para reaproveitamento de resíduos?
    connect_with_other_industry VARCHAR(20) CHECK (connect_with_other_industry IN ('Sim','Parcialmente','Não','Não sei informar')),

    -- Profissionais especializados em legislação ambiental
    -- has_professional_specialization VARCHAR(20) CHECK (has_professional_specialization IN ('Sim','Não')),

    -- A empresa possui meios para atualizar colaboradores sobre leis ambientais ?
    has_methods_in_environmental_laws VARCHAR(20) CHECK (has_methods_in_environmental_laws  IN ('Sim','Não')),

    -- Você acredita que seria útil um aplicativo que atualiza funcionários sobre leis ambientais vigentes?
    uptade_other_managers VARCHAR(20) CHECK (uptade_other_managers IN ('Sim','Parcialmente','Não')),

    -- Você considera útil um sistema de postagens onde empresas compartilhem dúvidas e desafios sobre sustentabilidade, descarte e reciclagem?
    see_utility_in_posts_and_doubt VARCHAR(20) CHECK (see_utility_in_posts_and_doubt IN ('Sim','Parcialmente','Não')),

    -- Você considera relevante ter um catálogo de resíduos com sugestões de reaproveitamento, integrado a um sistema de match e chat para colaboração entre empresas?
    residue_catalogue VARCHAR(20) CHECK (residue_catalogue IN ('Sim','Parcialmente','Não')), 
    data_forms TIMESTAMP
);-- Tabela auxiliar: setor de atuação da empresa
CREATE TABLE industry_sector (
    id_pesquisa INT REFERENCES pesquisa_simbia(id) ON DELETE CASCADE,
    sector VARCHAR(100) CHECK (sector IN ('Químico','Têxtil','Alimentícia','Construção civil','Mineração','Pesquisa','Sustentabilidade','Outros')),
    PRIMARY KEY (id_pesquisa, sector)
);

-- Tipos de resíduos gerados em maior volume
CREATE TABLE industry_waste_type (
    id_pesquisa INT REFERENCES pesquisa_simbia(id) ON DELETE CASCADE,
    waste_type VARCHAR(100) CHECK (waste_type IN ('Orgânicos','Têxteis','Plásticos','Químicos','Industriais perigosos', 'Outros')),
    PRIMARY KEY (id_pesquisa, waste_type)
);

-- Destino mais comum dos resíduos
CREATE TABLE industry_waste_destiny (
    id_pesquisa INT REFERENCES pesquisa_simbia(id) ON DELETE CASCADE,
    waste_destiny VARCHAR(100) CHECK (waste_destiny IN ('Aterro sanitário','Reaproveitamento interno','Incineração','Não sei informar','Outros')),
    PRIMARY KEY (id_pesquisa, waste_destiny)
);

-- Influência na escolha do destino dos resíduos
CREATE TABLE industry_waste_influence (
    id_pesquisa INT REFERENCES pesquisa_simbia(id) ON DELETE CASCADE,
    influence VARCHAR(100) CHECK (influence IN ('Custo de destinação (ex: Transporte/taxa de aterro/ etc.)','Conformidade com normas ambientais','Facilidade logística','Potencial de reaproveitamento ou geração de receita','Falta de alternativas viáveis','Não sei informar')),
    PRIMARY KEY (id_pesquisa, influence)
);

-- Maiores desafios enfrentados na gestão de resíduos
CREATE TABLE industry_challenge (
    id_pesquisa INT REFERENCES pesquisa_simbia(id) ON DELETE CASCADE,
    challenge VARCHAR(100) CHECK (challenge IN ('Falta de conhecimento técnico','Custos de logística','Burocracia','Falta de parceiros para reaproveitamento','Outros')),
    PRIMARY KEY (id_pesquisa, challenge)
);

-- Possíveis dificuldades para adesão ao Simbia
CREATE TABLE industry_difficulty (
    id_pesquisa INT REFERENCES pesquisa_simbia(id) ON DELETE CASCADE,
    difficulty VARCHAR(50) CHECK (difficulty IN ('Falta de verba ou retorno financeiro','Falta de equipe dedicada','Processos internos burocráticos','Nenhum dos motivos acimas', 'Outros')),
    PRIMARY KEY (id_pesquisa, difficulty)
);





-- ALTER TABLE pesquisa_simbia
-- ADD CONSTRAINT pesquisa_simbia_data_forms_unique UNIQUE (data_forms);

ALTER TABLE industry_challenge DROP CONSTRAINT industry_challenge_pkey;
ALTER TABLE industry_challenge ADD CONSTRAINT industry_challenge_pkey PRIMARY KEY (id_pesquisa, challenge);