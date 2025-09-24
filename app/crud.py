from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.schemas import TransactionCreate, TransactionResponse, TransactionFilter
from app.database import get_db
from app.routes.transactions import create_new_transaction, get_one_transaction, update_a_transaction
from app.routes.transactions import delete_a_transaction, get_filtered_transactions

from typing import List, Optional

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
            detail=f"Transaction with id {id} not found"
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

@router.delete("/transactions/{id}")
def delete_transaction(id: int, db:Session = Depends(get_db)):
    transaction_msg = delete_a_transaction(id, db)
    if not transaction_msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {id} not found"
        )
    return transaction_msg

'''
For if the user wants to check the categories they already have so they don't create another 
similar category
'''
# @router.get("/categories/{name}")
# def 

@router.get("/transactions")
def get_transactions(
    db: Session = Depends(get_db),
    filter: TransactionFilter = Depends(TransactionFilter),
    orderby_param: Optional[str] = Query(None, alias="$orderby"),
    top_param: Optional[int] = Query(None, alias="$top", ge=1, le=100),
    skip_param: Optional[int] = Query(None, alias="$skip", ge=0),
    expand_param: Optional[str] = Query(None, alias="$expand"),
):
    # Call the new function to get the built query
    transactions = get_filtered_transactions(
        db=db,
        filter_params=filter,
        orderby_param=orderby_param,
        top_param=top_param,
        skip_param=skip_param,
        expand_param=expand_param
    )
    if isinstance(transactions, List) and transactions:
        return transactions
    elif isinstance(transactions, dict):
        return transactions
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No transactions found under these filters"
        )