from app.database import engine, Base
from app import models  # Import all your models so SQLAlchemy knows about them

Base.metadata.create_all(bind=engine)
print("Tables created!")