from models import (
    adicionar_material,
    registrar_movimentacao,
    obter_materiais,
    obter_movimentacoes,
    editar_material,
    deletar_material,
    deletar_movimentacao
)

# Função para adicionar um novo material ao estoque
def adicionar_novo_material(nome, quantidade, unidade, estoque_minimo):
    adicionar_material(nome, quantidade, unidade, estoque_minimo)

# Função para registrar a entrada de um material no estoque
def entrada_estoque(material_id, quantidade):
    registrar_movimentacao(material_id, quantidade, tipo='Entrada')

# Função para registrar a saída de um material do estoque
def saida_estoque(material_id, quantidade):
    registrar_movimentacao(material_id, quantidade, tipo='Saída')

# Função para listar todos os materiais no estoque
def listar_materiais():
    return obter_materiais()

# Função para listar todas as movimentações de estoque
def listar_movimentacoes():
    return obter_movimentacoes()

# Função para verificar se algum material está abaixo do estoque mínimo
def verificar_estoque_minimo():
    materiais = obter_materiais()
    materiais_abaixo_minimo = []
    for material in materiais:
        if material[2] < material[4]:  # quantidade < estoque_minimo
            materiais_abaixo_minimo.append(material)
    return materiais_abaixo_minimo

# Função para editar um material existente
def atualizar_material(material_id, nome, quantidade, unidade, estoque_minimo):
    editar_material(material_id, nome, quantidade, unidade, estoque_minimo)

# Função para deletar um material do estoque
def remover_material(material_id):
    deletar_material(material_id)

# Função para deletar uma movimentação específica
def remover_movimentacao(movimentacao_id):
    deletar_movimentacao(movimentacao_id)
