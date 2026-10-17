from decimal import Decimal
from datetime import datetime, timezone
from app.extensions import db
from app.models.commerce import Product, Category, InventoryAdjustment, Order, OrderItem, ProductReview
from app.models.operations import PaymentTransaction
from app.services.audit_service import AuditService


class CommerceService:
    @staticmethod
    def adjust_inventory(product_id: int, quantity_change: int, reason: str, admin_user, notes: str = None) -> Product:
        """
        Thread-safe stock adjustment using row-level locking (with_for_update).
        Prevents concurrency race conditions and logs to inventory audit history.
        """
        # Lock product row
        product = Product.query.filter_by(id=product_id).with_for_update().first()
        if not product:
            raise ValueError(f"Product ID {product_id} not found.")

        old_stock = product.stock_quantity
        new_stock = old_stock + quantity_change
        if new_stock < 0:
            raise ValueError(f"Cannot reduce stock below zero. Current stock is {old_stock}.")

        product.stock_quantity = new_stock

        adjustment = InventoryAdjustment(
            product_id=product.id,
            admin_user_id=admin_user.id if admin_user else None,
            quantity_change=quantity_change,
            previous_stock=old_stock,
            new_stock=new_stock,
            reason=reason,
            notes=notes,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(adjustment)
        db.session.commit()

        AuditService.log(
            action="STOCK_ADJUSTMENT",
            module="commerce",
            actor_email=admin_user.email if admin_user else "system",
            actor_user_id=admin_user.id if admin_user else None,
            entity_type="Product",
            entity_id=str(product.id),
            details={
                "sku": product.sku,
                "product_name": product.name,
                "previous_stock": old_stock,
                "new_stock": new_stock,
                "change": quantity_change,
                "reason": reason,
            },
        )
        return product

    @staticmethod
    def update_order_status(order_id: int, new_status: str, admin_user, notes: str = None) -> Order:
        order = Order.query.filter_by(id=order_id).first()
        if not order:
            raise ValueError(f"Order ID {order_id} not found.")

        valid_statuses = {"pending", "processing", "shipped", "delivered", "cancelled"}
        if new_status.lower() not in valid_statuses:
            raise ValueError(f"Invalid order status: {new_status}")

        old_status = order.order_status
        order.order_status = new_status.lower()
        if notes:
            order.admin_notes = f"{order.admin_notes or ''}\n[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}] {notes}".strip()

        db.session.commit()

        AuditService.log(
            action="ORDER_STATUS_CHANGE",
            module="commerce",
            actor_email=admin_user.email if admin_user else "system",
            actor_user_id=admin_user.id if admin_user else None,
            entity_type="Order",
            entity_id=str(order.id),
            details={
                "order_number": order.order_number,
                "old_status": old_status,
                "new_status": new_status,
            },
        )
        return order

    @staticmethod
    def process_refund(order_id: int, amount: Decimal, reason: str, admin_user) -> PaymentTransaction:
        order = Order.query.filter_by(id=order_id).first()
        if not order:
            raise ValueError(f"Order ID {order_id} not found.")

        if amount <= 0 or amount > order.total_amount:
            raise ValueError(f"Refund amount ₹{amount} is invalid for order total ₹{order.total_amount}.")

        order.payment_status = "refunded"
        order.order_status = "cancelled"

        txn = PaymentTransaction(
            transaction_number=f"REF-{order.order_number.replace('#', '')}-{int(datetime.now(timezone.utc).timestamp())}",
            order_id=order.id,
            amount=amount,
            currency="INR",
            gateway=order.payment_method or "Razorpay",
            status="refunded",
            customer_name=order.customer_name,
            customer_email=order.customer_email,
            error_message=f"Refund reason: {reason}",
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(txn)
        db.session.commit()

        AuditService.log(
            action="ORDER_REFUND",
            module="commerce",
            actor_email=admin_user.email if admin_user else "system",
            actor_user_id=admin_user.id if admin_user else None,
            entity_type="Order",
            entity_id=str(order.id),
            details={
                "order_number": order.order_number,
                "refund_amount": str(amount),
                "reason": reason,
            },
        )
        return txn

    @staticmethod
    def moderate_review(review_id: int, is_approved: bool, admin_user) -> ProductReview:
        review = ProductReview.query.filter_by(id=review_id).first()
        if not review:
            raise ValueError(f"Review ID {review_id} not found.")

        review.is_approved = is_approved
        db.session.commit()

        AuditService.log(
            action="REVIEW_MODERATION",
            module="commerce",
            actor_email=admin_user.email if admin_user else "system",
            actor_user_id=admin_user.id if admin_user else None,
            entity_type="ProductReview",
            entity_id=str(review.id),
            details={"approved": is_approved, "product_id": review.product_id},
        )
        return review
