import json
import os

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Define the database file name
db_file = os.path.abspath("server/db/ivy_store.db")

# Set up the database engine and session
engine = create_engine(f"sqlite:///{db_file}")
Session = sessionmaker(bind=engine)
session = Session()

# Define the base class for ORM models
Base = declarative_base()


# Define the models
class Category(Base):
    __tablename__ = "Category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "Product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    out_of_stock = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey("Category.id"), nullable=False)
    category = relationship("Category", back_populates="products")
    sizes = Column(String, nullable=True)  # Comma-separated list of sizes
    images = Column(String, nullable=True)  # Comma-separated list of image URLs
    url = Column(String, nullable=True)


# Create the tables
Base.metadata.create_all(engine)


def load_json_to_db(json_file):
    """Load products from a JSON file to the database."""
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    for product in data["products"]:
        # Check if the category exists, create it if not
        category_name = product["category"]
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            session.add(category)
            session.commit()

        # Add the product
        new_product = Product(
            name=product["name"],
            description=product.get("description"),
            price=product["price"],
            out_of_stock=product["out_of_stock"],
            category=category,
            sizes=",".join(product.get("sizes", [])),
            images=",".join(
                product.get("images", [])
            ),  # Join image URLs into a single string
            url=product.get("url", f"https://ivymoda.com?q={product['name']}"),
        )
        session.add(new_product)

    # Commit all changes
    session.commit()


if __name__ == "__main__":
    # Path to your JSON file
    json_file = os.path.abspath("server/data/products.json")

    # Load data into the database
    load_json_to_db(json_file)
    print("Data has been loaded into the database.")
