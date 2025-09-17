from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import TransactionCreate, TransactionResponse, TransactionListResponse
from app.schemas import TransactionsGet
from app.database import get_db
from app.routes.transactions import create_new_transaction, get_one_transaction, update_a_transaction
from app.routes.transactions import delete_a_transaction

router = APIRouter()

@router.post("/transactions")
def create_transaction(user : TransactionCreate, db: Session = Depends(get_db)):
    transaction = create_new_transaction(user, db)
    return transaction

@router.get("/transactions/{id}")
def get_transaction(id: int, db: Session = Depends(get_db) ) -> TransactionResponse:
    transaction = get_one_transaction(id, db)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction

@router.put("/transactions/{id}")
def update_transaction(id: int, new_transaction: TransactionCreate, db: Session = Depends(get_db)) -> TransactionResponse:
    transaction = update_a_transaction(id, new_transaction, db)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {id} not found"
        )
    return transaction

@router.delete("/transaction/{id}")
def delete_transaction(id: int, db:Session = Depends(get_db)):
    transaction_msg = delete_a_transaction(id, db)
    if not transaction_msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {id} not found"
        )
    return transaction_msg
