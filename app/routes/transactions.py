from sqlalchemy.orm import Session

from app.schemas import TransactionCreate, TransactionsGet
from app.models import Transaction, Category

from datetime import date

def create_new_transaction(transaction:TransactionCreate, db:Session):
    db_category = db.query(Category).filter(Category.name == transaction.category.lower()).first()
    
    if not db_category:
        db_category = Category(name=transaction.category.lower())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)  # Refresh to get the new category_id from the database
    
    new_transaction = Transaction(
        amount = transaction.amount,
        date = transaction.date if transaction.date else date.today(),
        description = transaction.description,
        category_id = db_category.category_id
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

def get_one_transaction(id:int, db:Session):
    db_transaction = db.query(Transaction).filter(Transaction.transaction_id == id).first()
    return db_transaction

def update_a_transaction(id:int, new_transaction:TransactionCreate, db:Session):
    db_transaction = db.query(Transaction).filter(Transaction.transaction_id == id).first()

    if not db_transaction:
        return
    
    db_category = db.query(Category).filter(Category.name == new_transaction.category.lower()).first()
    
    if not db_category:
        db_category = Category(name=new_transaction.category.lower())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)  # Refresh to get the new category_id from the database

    db_transaction.amount = new_transaction.amount
    db_transaction.date = new_transaction.date if new_transaction.date else date.today()
    db_transaction.description = new_transaction.description
    db_transaction.category_id = db_category.category_id

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_a_transaction(id: int, db:Session):
    db_transaction = db.query(Transaction).filter(Transaction.transaction_id == id)

    if not db_transaction.first():
        return
    
    db_transaction.delete()
    db.commit()
    return {"msg":f"deleted transaction with id {id}"}
