from datetime import datetime
from src.models.user import db

class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    movement_type = db.Column(db.String(10), nullable=False)  # e.g., 'entrada', 'saida', 'ajuste'
    quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True) # Optional: link to user who made the change

    product = db.relationship("Product", backref=db.backref("movements", lazy=True))
    user = db.relationship("User", backref=db.backref("stock_movements", lazy=True))

    def __repr__(self):
        return f'<StockMovement {self.movement_type} {self.quantity} for Product ID {self.product_id} at {self.timestamp}>'

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'movement_type': self.movement_type,
            'quantity': self.quantity,
            'reason': self.reason,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'user_id': self.user_id
        }

