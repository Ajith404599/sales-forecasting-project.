from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.product import Product
from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleResponse
from app.core.audit_helper import log_audit_event

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def record_sale(
    sale_in: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.product_id == sale_in.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {sale_in.product_id} not found"
        )
    if not product.active_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot record sale for an inactive product"
        )

    unit_price = sale_in.unit_price if sale_in.unit_price is not None else product.base_price
    discount = sale_in.discount_amount or Decimal("0.00")
    total_amount = max(Decimal("0.00"), (Decimal(sale_in.quantity) * Decimal(unit_price)) - discount)

    new_sale = Sale(
        product_id=product.product_id,
        user_id=current_user.user_id,
        quantity=sale_in.quantity,
        unit_price=unit_price,
        discount_amount=discount,
        total_amount=total_amount
    )
    db.add(new_sale)
    db.flush()

    log_audit_event(
        db=db,
        user_id=current_user.user_id,
        action="RECORD_SALE",
        module="SALES",
        description=f"Recorded sale #{new_sale.sale_id} for product '{product.product_name}' (Qty: {new_sale.quantity}, Total: ${new_sale.total_amount})"
    )
    db.commit()
    db.refresh(new_sale)
    return new_sale


@router.get("", response_model=List[SaleResponse])
def get_sales(
    product_id: Optional[int] = Query(None, description="Filter by product ID"),
    user_id: Optional[int] = Query(None, description="Filter by user/staff ID"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Sale)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if user_id:
        query = query.filter(Sale.user_id == user_id)

    return query.order_by(Sale.sale_date.desc()).offset(offset).limit(limit).all()