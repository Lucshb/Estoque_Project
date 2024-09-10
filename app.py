import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configurações iniciais
st.set_page_config(page_title="Gestão de Estoque", layout="wide")

# Simulando dados de produtos (peças de caminhões)
np.random.seed(42)
produtos = {
    'Código': [f'P{str(i).zfill(3)}' for i in range(1, 11)],
    'Nome': [
        'Pneu 295/80R22.5', 'Filtro de Óleo Motor', 'Pastilha de Freio Dianteira',
        'Disco de Embreagem', 'Radiador de Água', 'Correia Dentada',
        'Amortecedor Traseiro', 'Kit de Embreagem', 'Filtro de Combustível', 'Eixo Cardan'
    ],
    'Categoria': [
        'Suspensão e Freios', 'Motor', 'Suspensão e Freios',
        'Transmissão', 'Arrefecimento', 'Transmissão',
        'Suspensão e Freios', 'Transmissão', 'Motor', 'Transmissão'
    ],
    'Quantidade': np.random.randint(10, 100, size=10),
    'Quantidade mínima': np.random.randint(5, 20, size=10),
    'Custo unitário (R$)': np.round(np.random.uniform(100, 2000, size=10), 2),
    'Fornecedor': np.random.choice(['AutoPeças São Carlos', 'Distribuidora DieselTec', 'Mecânica Caminhões Ltda.'], size=10),
}

df_produtos = pd.DataFrame(produtos)

# Simulando dados de movimentações
movimentacoes = {
    'Data': [datetime.today() - timedelta(days=np.random.randint(1, 30)) for _ in range(20)],
    'Tipo': np.random.choice(['Entrada', 'Saída'], size=20),
    'Quantidade': np.random.randint(1, 50, size=20),
    'Produto': np.random.choice(df_produtos['Nome'], size=20),
    'Motivo': np.random.choice(['Compra', 'Venda', 'Perda'], size=20),
    'Valor (R$)': np.round(np.random.uniform(10, 1000, size=20), 2)
}

df_movimentacoes = pd.DataFrame(movimentacoes)
df_movimentacoes['Data'] = df_movimentacoes['Data'].dt.strftime('%Y-%m-%d')

# Simulando dados de clientes
clientes = {
    'Nome': ['Transportadora ABC', 'Transportes Dourados', 'Caminhões e Cia', 'Logística São Pedro', 'Frota Nacional Ltda'],
    'CNPJ/CPF': ['00.000.000/0001-91', '11.111.111/1111-11', '22.222.222/2222-22', '33.333.333/3333-33', '44.444.444/4444-44'],
    'Telefone': ['(11) 1111-1111', '(21) 2222-2222', '(31) 3333-3333', '(41) 4444-4444', '(51) 5555-5555'],
    'E-mail': ['abc@transp.com', 'dourados@transp.com', 'cia@caminhoes.com', 'pedro@logistica.com', 'nacional@frota.com'],
    'Endereço': ['Rua A, 100', 'Avenida B, 200', 'Estrada C, 300', 'Rua D, 400', 'Avenida E, 500']
}

df_clientes = pd.DataFrame(clientes)

# Layout da aplicação
st.title("Sistema de Gestão de Estoque")

# ======================= CARDS DE MÉTRICAS =======================
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Relatório financeiro (valorização do estoque)
    df_produtos['Valor Total (R$)'] = df_produtos['Quantidade'] * df_produtos['Custo unitário (R$)']
    valor_total = df_produtos['Valor Total (R$)'].sum()
    st.metric(label="Valor Total do Estoque", value=f"R${valor_total:,.0f}")

with col2:
    # Número total de produtos
    total_produtos = df_produtos.shape[0]
    st.metric(label="Total de Produtos", value=total_produtos)

with col3:
    # Número total de movimentações
    total_movimentacoes = df_movimentacoes.shape[0]
    st.metric(label="Total de Movimentações", value=total_movimentacoes)

with col4:
    # Número total de clientes cadastrados
    total_clientes = df_clientes.shape[0]
    st.metric(label="Total de Clientes", value=total_clientes)

# ======================= CADASTRO DE PRODUTOS =======================
st.header("Cadastro de Produtos")

with st.form("cadastro_produtos"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        codigo = st.text_input("Código do Produto")
        nome = st.text_input("Nome do Produto")
        categoria = st.selectbox("Categoria", ['Suspensão e Freios', 'Motor', 'Transmissão', 'Arrefecimento'])
        
    with col2:
        quantidade = st.number_input("Quantidade Inicial", min_value=0, step=1)
        quantidade_minima = st.number_input("Quantidade Mínima", min_value=0, step=1)
        custo = st.number_input("Custo Unitário (R$)", min_value=0.0, step=0.01)
        
    with col3:
        fornecedor = st.text_input("Fornecedor")
    
    # Botão para enviar
    submit_produto = st.form_submit_button("Cadastrar Produto")

    if submit_produto:
        # Adicionando novo produto ao dataframe
        novo_produto = pd.DataFrame({
            'Código': [codigo],
            'Nome': [nome],
            'Categoria': [categoria],
            'Quantidade': [quantidade],
            'Quantidade mínima': [quantidade_minima],
            'Custo unitário (R$)': [custo],
            'Fornecedor': [fornecedor]
        })
        
        df_produtos = pd.concat([df_produtos, novo_produto], ignore_index=True)
        st.success(f"Produto {nome} cadastrado com sucesso!")

# Visualização de Produtos
st.header("Produtos em Estoque")
st.dataframe(df_produtos, use_container_width=True)  # Largura ajustável

# ======================= CADASTRO DE MOVIMENTAÇÕES =======================
st.header("Cadastro de Movimentações de Estoque")

with st.form("cadastro_movimentacoes"):
    col1, col2 = st.columns(2)
    
    with col1:
        data_mov = st.date_input("Data da Movimentação", value=datetime.today())
        tipo_mov = st.selectbox("Tipo de Movimentação", ["Entrada", "Saída"])
        produto_mov = st.selectbox("Produto", df_produtos['Nome'].unique())
    
    with col2:
        quantidade_mov = st.number_input("Quantidade", min_value=0, step=1)
        motivo_mov = st.selectbox("Motivo", ["Compra", "Venda", "Perda"])
        valor_mov = st.number_input("Valor (R$)", min_value=0.0, step=0.01)

        # Se for uma venda, permitir selecionar um cliente
        if tipo_mov == 'Saída':
            cliente_mov = st.selectbox("Cliente", df_clientes['Nome'].unique())
        else:
            cliente_mov = None
    
    # Botão para enviar
    submit_mov = st.form_submit_button("Cadastrar Movimentação")

    if submit_mov:
        # Adicionando nova movimentação ao dataframe
        nova_movimentacao = pd.DataFrame({
            'Data': [data_mov.strftime('%Y-%m-%d')],
            'Tipo': [tipo_mov],
            'Quantidade': [quantidade_mov],
            'Produto': [produto_mov],
            'Motivo': [motivo_mov],
            'Valor (R$)': [valor_mov]
        })
        
        df_movimentacoes = pd.concat([df_movimentacoes, nova_movimentacao], ignore_index=True)
        st.success(f"Movimentação de {tipo_mov} cadastrada com sucesso!")

# Visualização de Movimentações
st.header("Movimentações de Estoque")
st.dataframe(df_movimentacoes, use_container_width=True)  # Largura ajustável

# Indicador de produtos abaixo do estoque mínimo
st.subheader("Produtos com Estoque Baixo")
df_estoque_baixo = df_produtos[df_produtos['Quantidade'] < df_produtos['Quantidade mínima']]
st.table(df_estoque_baixo[['Código', 'Nome', 'Quantidade', 'Quantidade mínima']])


# Gráfico de movimentação por tipo
st.subheader("Gráfico de Movimentação por Tipo")
df_movimentacao_tipo = df_movimentacoes.groupby('Tipo').agg({'Quantidade': 'sum'}).reset_index()
st.bar_chart(df_movimentacao_tipo.set_index('Tipo'))

