from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.product import Product

product_bp = Blueprint("product", __name__)

# Rota para listar todos os produtos
@product_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

# Rota para obter um produto específico pelo ID
@product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

# Rota para criar um novo produto
@product_bp.route("/products", methods=["POST"])
def create_product():
    data = request.json
    if not data or not data.get("name") or not data.get("sku"):
        return jsonify({"error": "Nome e SKU são obrigatórios"}), 400

    # Verifica se SKU já existe
    if Product.query.filter_by(sku=data["sku"]).first():
        return jsonify({"error": f"SKU {data["sku"]} já existe"}), 409 # Conflict

    new_product = Product(
        name=data["name"],
        description=data.get("description"),
        sku=data["sku"],
        quantity=data.get("quantity", 0),
        unit_price=data.get("unit_price")
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

# Rota para atualizar um produto existente
@product_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json

    # Verifica se o novo SKU já existe em outro produto
    new_sku = data.get("sku")
    if new_sku and new_sku != product.sku and Product.query.filter_by(sku=new_sku).first():
         return jsonify({"error": f"SKU {new_sku} já pertence a outro produto"}), 409

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.sku = new_sku if new_sku else product.sku
    # A quantidade não deve ser atualizada diretamente aqui, mas via movimentação de estoque
    # product.quantity = data.get("quantity", product.quantity)
    product.unit_price = data.get("unit_price", product.unit_price)

    db.session.commit()
    return jsonify(product.to_dict())

# Rota para deletar um produto
@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    # Adicionar verificação se há estoque ou movimentos associados antes de deletar?
    # Por enquanto, permite deletar.
    db.session.delete(product)
    db.session.commit()
    return "", 204

