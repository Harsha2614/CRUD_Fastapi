from fastapi import FastAPI,Depends
from models import Product
from database import session, engine
import database_models
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
app = FastAPI()
app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_methods=["*"]
      
)
database_models.Base.metadata.create_all(bind=engine)
     
products= [
    Product(id=1,name="pen",description="Helps to write on the book",price=10,quantity=2),
    Product(id=2,name="Book",description="Helps to note something",price=15,quantity=1),
    Product(id=3,name="Scale",description="Helps to draw something",price=10,quantity=3)

]

def get_db():
     db=session()
     try:
          yield db
     finally:
          db.close()
     pass


def initdb():
     db=session()
     if db.query(database_models.Product).count() == 0:
               for product in products:
                    db.add(database_models.Product(**product.model_dump()))
               db.commit()
initdb()


@app.get("/")
def greet():
    return "Hello from harsha"

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
     db_products=db.query(database_models.Product).all()

     return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int,db: Session = Depends(get_db)):
     db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
     if db_product:
               return db_product
     return "product not found"

@app.post("/products")
def add_a_product( product: Product,db: Session=Depends(get_db)):
      db.add(database_models.Product(**product.model_dump()))
      db.commit()
     
      return product
      

@app.put("/products/{id}")
def update_product(id:int,Updated_product:Product,db:Session =Depends(get_db)):
     db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
     if db_product:
           db_product.name=Updated_product.name
           db_product.description=Updated_product.description
           db_product.price=Updated_product.price
           db_product.quantity=Updated_product.quantity
           db.commit()
           return "Product updated"
     else:
           return "Produt not found"


@app.delete("/products")
def delete_product(id:int,db:Session=Depends(get_db)):
          db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
          if db_product:
               db.delete(db_product)
               db.commit()
     
               return "product deleted successfully"
          else:
                
           return "Product not found"