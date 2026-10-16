CREATE TABLE IF NOT EXISTS operacoes (
    -- ID numérico positivo com exatamente 10 dígitos, único e autoincrementável (Primary Key)
    id BIGINT PRIMARY KEY,
    
    -- Data em que a operação foi realizada (pode ser DATE ou TIMESTAMP)
    data DATE NOT NULL,
    
    -- Código do ativo negociado (4 letras maiúsculas + 1 ou 2 números)
    ativo VARCHAR(6) NOT NULL,
    
    -- Quantidade de ativos (número inteiro positivo)
    quantidade INT NOT NULL CHECK (quantidade > 0),
    
    -- Preço unitário (valor monetário positivo, ex: até 12 dígitos inteiros e 2 decimais)
    valor_unitario NUMERIC(14, 2) NOT NULL CHECK (valor_unitario >= 0),
    
    -- Tipo da operação (ex: 1 para Compra, 2 para Venda)
    tipo_operacao INT NOT NULL CHECK (tipo_operacao IN (1, 2)),
    
    -- Valor bruto (quantidade * valor_unitario)
    valor_bruto NUMERIC(14, 2) NOT NULL,
    
    -- Taxas incidentes (0,03% do valor bruto)
    taxas NUMERIC(14, 2) NOT NULL,
    
    -- Valor líquido final (calculado conforme o tipo de operação)
    valor_liquido NUMERIC(14, 2) NOT NULL
);
