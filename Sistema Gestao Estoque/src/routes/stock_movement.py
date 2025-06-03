from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.product import Product
from src.models.stock_movement import StockMovement
from datetime import datetime

stock_movement_bp = Blueprint("stock_movement", __name__)

# Rota para registrar uma nova movimentação de estoque
@stock_movement_bp.route("/stock_movements", methods=["POST"])
def create_stock_movement():
    data = request.json
    if not data or not data.get("product_id") or not data.get("movement_type") or data.get("quantity") is None:
        return jsonify({"error": "product_id, movement_type e quantity são obrigatórios"}), 400

    product_id = data["product_id"]
    movement_type = data["movement_type"].lower()
    quantity = data["quantity"]
    reason = data.get("reason")
    user_id = data.get("user_id") # Opcional

    if movement_type not in ["entrada", "saida", "ajuste"]:
        return jsonify({"error": "movement_type inválido. Use 'entrada', 'saida' ou 'ajuste'."}), 400

    if not isinstance(quantity, int) or quantity <= 0:
         return jsonify({"error": "quantity deve ser um inteiro positivo."}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": f"Produto com ID {product_id} não encontrado."}), 404

    # Atualiza a quantidade do produto
    if movement_type == "entrada":
        product.quantity += quantity
    elif movement_type == "saida":
        if product.quantity < quantity:
            return jsonify({"error": "Quantidade em estoque insuficiente para a saída."}), 400
        product.quantity -= quantity
    elif movement_type == "ajuste":
        # Para ajuste, a quantidade enviada é a nova quantidade total
        # Mas vamos registrar a diferença como a quantidade movimentada
        # Ou podemos mudar a lógica para enviar a *diferença* no ajuste?
        # Decisão: Por simplicidade, vamos registrar a quantidade do ajuste como enviada
        # e assumir que o frontend/usuário calcula a diferença se necessário.
        # A quantidade do produto será atualizada para um novo valor (se fornecido)
        # Vamos manter a lógica original: 'quantity' é a quantidade movimentada.
        # Se for ajuste positivo, é como entrada. Se negativo, como saída.
        # Para simplificar, vamos tratar ajuste como entrada/saída com motivo específico.
        # Ou melhor: Ajuste define a quantidade *final*. Registramos a diferença.
        # Decisão 2: Manter simples. 'quantity' é a quantidade adicionada/removida.
        # Se 'ajuste', pode ser positivo ou negativo. Permitir quantidade negativa aqui.
        # if quantity < 0:
        #     if product.quantity < abs(quantity):
        #          return jsonify({"error": "Ajuste negativo maior que estoque atual."}), 400
        # product.quantity += quantity # Permite ajuste negativo
        # Decisão 3: Ajuste define a quantidade *final*. O campo quantity na movimentação será a diferença.
        new_quantity = data.get("new_total_quantity")
        if new_quantity is None or not isinstance(new_quantity, int) or new_quantity < 0:
             return jsonify({"error": "Para 'ajuste', 'new_total_quantity' (inteiro não negativo) é obrigatório."}), 400
        
        quantity_diff = new_quantity - product.quantity
        product.quantity = new_quantity
        # A 'quantity' registrada na movimentação será a diferença
        quantity = quantity_diff # Atualiza a variável local quantity para registrar a diferença

    # Cria o registro da movimentação
    new_movement = StockMovement(
        product_id=product_id,
        movement_type=movement_type,
        quantity=quantity, # Registra a quantidade movimentada (ou a diferença no caso de ajuste)
        reason=reason,
        user_id=user_id,
        timestamp=datetime.utcnow()
    )

    try:
        db.session.add(new_movement)
        db.session.commit()
        return jsonify(new_movement.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao registrar movimentação", "details": str(e)}), 500

# Rota para listar todas as movimentações (pode precisar de filtros/paginação)
@stock_movement_bp.route("/stock_movements", methods=["GET"])
def get_stock_movements():
    # Adicionar filtros por produto, tipo, data?
    product_id_filter = request.args.get("product_id")
    query = StockMovement.query
    if product_id_filter:
        query = query.filter_by(product_id=int(product_id_filter))
    
    movements = query.order_by(StockMovement.timestamp.desc()).all()
    return jsonify([movement.to_dict() for movement in movements])

# Rota para obter uma movimentação específica
@stock_movement_bp.route("/stock_movements/<int:movement_id>", methods=["GET"])
def get_stock_movement(movement_id):
    movement = StockMovement.query.get_or_404(movement_id)
    return jsonify(movement.to_dict())

