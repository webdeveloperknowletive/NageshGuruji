import pytest
from decimal import Decimal
from app.models.commerce import Product, Order, InventoryAdjustment
from app.models.user import AdminUser
from app.services.commerce_service import CommerceService


def test_inventory_adjustment(app):
    with app.app_context():
        admin = AdminUser.query.filter_by(email="super@japam.in").first()
        prod = Product.query.filter_by(sku="RM-001").first()
        initial_stock = prod.stock_quantity

        # Add 15 units
        CommerceService.adjust_inventory(prod.id, 15, "Restock Received", admin)
        assert prod.stock_quantity == initial_stock + 15

        # Check audit adjustment entry
        adj = InventoryAdjustment.query.filter_by(product_id=prod.id).order_by(InventoryAdjustment.id.desc()).first()
        assert adj.quantity_change == 15
        assert adj.previous_stock == initial_stock
        assert adj.new_stock == initial_stock + 15

        # Attempt to subtract more units than available should raise ValueError
        with pytest.raises(ValueError):
            CommerceService.adjust_inventory(prod.id, -1000, "Invalid Deduct", admin)


def test_order_status_and_refund(app):
    with app.app_context():
        admin = AdminUser.query.filter_by(email="super@japam.in").first()

        order = Order(
            order_number="#ORD-TEST-001",
            customer_name="Test Devotee",
            customer_email="devotee@test.in",
            total_amount=Decimal("1500.00"),
            order_status="pending",
            payment_status="paid",
        )
        app.extensions["sqlalchemy"].session.add(order)
        app.extensions["sqlalchemy"].session.commit()

        # Update order status to shipped
        CommerceService.update_order_status(order.id, "shipped", admin, "Dispatched via courier")
        assert order.order_status == "shipped"

        # Process refund
        txn = CommerceService.process_refund(order.id, Decimal("1500.00"), "Damaged item", admin)
        assert order.payment_status == "refunded"
        assert order.order_status == "cancelled"
        assert txn.status == "refunded"
