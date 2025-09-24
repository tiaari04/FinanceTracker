from sqlalchemy.orm import Session, joinedload

from app.schemas import TransactionCreate, TransactionFilter
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


def get_filtered_transactions(db: Session,
    filter_params: TransactionFilter,
    orderby_param: str,
    top_param: int,
    skip_param: int,
    expand_param: str
):
    """
    Builds and returns a SQLAlchemy query based on provided parameters.
    This function handles all the query-building logic.
    """
    query = db.query(Transaction)

    # Handle filter
    # Only allowing user to filter by amount, category_id and date
    # and they will only be able to filter using eq, gt, lt, and, or, not
    query = filter_params.filter(query)

    # Handle expand
    if not expand_param:
        pass
    elif expand_param == "category":
        query = query.options(joinedload(Transaction.category)) 
    else:
        return {"msg": "Cannot expand on given parameter. Check parameter spelling or word order"}
    

    # Handle orderby
    # able to order by date or amount
    if orderby_param:
        sort_clauses = []
        # Split sort criteria by ","
        sort_criteria = orderby_param.split(',')
        for criteria in sort_criteria:
            criteria = criteria.strip()
            print(criteria)
            if "date desc" in criteria.lower():
                sort_clauses.append(Transaction.date.desc())
            elif "date asc" in criteria.lower():
                sort_clauses.append(Transaction.date.asc())
            elif "amount desc" in criteria.lower():
                sort_clauses.append(Transaction.amount.desc())
            elif "amount asc" in criteria.lower():
                sort_clauses.append(Transaction.amount.asc())
            else:
                return {"msg": "Cannot order by given parameters. Check parameter spelling or word order"}

        if sort_clauses:
            query = query.order_by(*sort_clauses)
        # else:
        #     return {"msg": "Cannot order by given parameters. Check parameter spelling or word order"}
    
    # Handle top
    if top_param:
        query= query.limit(top_param)

    # Handle skip
    if skip_param:
        query = query.offset(skip_param)
    
    transactions = query.all()
    return transactions