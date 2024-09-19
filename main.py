import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from db_manager import conectar
from estoque import (
    adicionar_novo_material,
    entrada_estoque,
    saida_estoque,
    listar_materiais,
    listar_movimentacoes,
    atualizar_material,
    remover_material,
    remover_movimentacao,
    verificar_estoque_minimo
)

# Configuração da página
st.set_page_config(page_title="Gerenciamento de Estoque", layout="wide")

# Interface Streamlit
st.title("SOSTI - Estoque do TI")

# Função para adicionar material
def adicionar_material(nome, quantidade, unidade, estoque_minimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO materiais (nome, quantidade, unidade, estoque_minimo) VALUES (?, ?, ?, ?)",
        (nome, quantidade, unidade, estoque_minimo)
    )
    conn.commit()
    conn.close()

# Função para registrar movimentação de estoque
def registrar_movimentacao(material_id, quantidade, tipo):
    conn = conectar()
    cursor = conn.cursor()
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO movimentacoes (material_id, quantidade, tipo, data) VALUES (?, ?, ?, ?)",
        (material_id, quantidade, tipo, data_atual)
    )
    # Atualiza a quantidade de material no estoque
    cursor.execute(
        "UPDATE materiais SET quantidade = quantidade + ? WHERE id = ?",
        (quantidade if tipo == 'Entrada' else -quantidade, material_id)
    )
    conn.commit()
    conn.close()

# Função para visualizar o estoque
def visualizar_estoque():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM materiais", conn)
    conn.close()
    return df

# Seção de Cadastro de Materiais e Visualização de Estoque
st.header("Gerenciamento de Estoque")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Cadastro de Materiais")
    nome = st.text_input("Nome do Material")
    quantidade = st.number_input("Quantidade Inicial", min_value=0)
    unidade = st.text_input("Unidade (ex: kg, m, unidades)")
    estoque_minimo = st.number_input("Estoque Mínimo", min_value=0)
    if st.button("Adicionar Material", key="botao_adicionar_material"):
        adicionar_material(nome, quantidade, unidade, estoque_minimo)    
        st.success(f"Material '{nome}' adicionado com sucesso!")
    
    # Limpar os inputs
    st.session_state["nome_material"] = ""
    st.session_state["quantidade_material"] = 0
    st.session_state["unidade_material"] = ""
    st.session_state["estoque_minimo_material"] = 0    

    st.subheader("Movimentação de Estoque")
    material_id = st.number_input("ID do Material", min_value=1, key="mov_id")
    quantidade_mov = st.number_input("Quantidade", min_value=1, key="mov_quantidade")
    tipo_mov = st.selectbox("Tipo de Movimentação", ["Entrada", "Saída"], key="mov_tipo")
    if st.button("Registrar Movimentação", key="botao_registrar_movimentacao"):
        registrar_movimentacao(material_id, quantidade_mov, tipo_mov)
        st.success("Movimentação registrada com sucesso!")

with col2:
    st.subheader("Visualizar Estoque")
    estoque_df = visualizar_estoque()
    st.dataframe(estoque_df)

# Seção de Edição e Remoção de Materiais
st.header("Editar ou Remover Materiais")

col3, col4 = st.columns(2)

with col3:
    materiais = listar_materiais()
    material_id_selecionado = st.selectbox("Selecione o Material para Editar/Remover", [m[0] for m in materiais])

    if material_id_selecionado:
        material_selecionado = next(m for m in materiais if m[0] == material_id_selecionado)
        novo_nome = st.text_input("Nome do Material", value=material_selecionado[1])
        nova_quantidade = st.number_input("Quantidade", value=material_selecionado[2], min_value=0)
        nova_unidade = st.text_input("Unidade", value=material_selecionado[3])
        novo_estoque_minimo = st.number_input("Estoque Mínimo", value=material_selecionado[4], min_value=0)

        if st.button("Atualizar Material", key="botao_atualizar_material"):
            atualizar_material(material_id_selecionado, novo_nome, nova_quantidade, nova_unidade, novo_estoque_minimo)
            st.success(f"Material '{novo_nome}' atualizado com sucesso!")

        if st.button("Remover Material", key="botao_remover_material"):
            remover_material(material_id_selecionado)
            st.success(f"Material '{material_selecionado[1]}' removido com sucesso!")

with col4:
    st.subheader("Remover Movimentações")
    movimentacoes = listar_movimentacoes()
    movimentacao_id_selecionada = st.selectbox("Selecione a Movimentação para Remover", [m[0] for m in movimentacoes])

    if movimentacao_id_selecionada:
        movimentacao_selecionada = next(m for m in movimentacoes if m[0] == movimentacao_id_selecionada)

        st.write(f"Material ID: {movimentacao_selecionada[1]}, Quantidade: {movimentacao_selecionada[2]}, Tipo: {movimentacao_selecionada[3]}, Data: {movimentacao_selecionada[4]}")

        if st.button("Remover Movimentação", key="botao_remover_movimentacao"):
            remover_movimentacao(movimentacao_id_selecionada)
            st.success("Movimentação removida com sucesso!")

# Estilo personalizado para os botões
st.markdown("""
<style>
.stButton button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
}

.stButton button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)
