"""Lab 2.2 - Bookstore CRUD Operations
Basic Create, Read, Update, Delete with PyMongo.
"""

import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
for p in [parent_dir, current_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

from config.connection import get_db, reset_collection, banner, export_collection_to_json
from rich.console import Console
from rich.table import Table

console = Console(width=110)

BOOKS = [
    {"title": "The Pragmatic Programmer", "author": "David Thomas & Andrew Hunt",
     "year": 2019, "genre": "Software Engineering", "price": 49.99, "isbn": "978-0135957059",
     "tags": ["programming", "career", "best-practices"],
     "publisher": {"name": "Addison-Wesley", "location": "Boston"}},
    {"title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann",
     "year": 2017, "genre": "Databases", "price": 45.99, "isbn": "978-1449373320",
     "tags": ["databases", "distributed-systems", "architecture"],
     "publisher": {"name": "O'Reilly Media", "location": "Sebastopol"}},
    {"title": "Deep Learning", "author": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
     "year": 2016, "genre": "Machine Learning", "price": 72.00, "isbn": "978-0262035613",
     "tags": ["AI", "neural-networks", "theory"],
     "publisher": {"name": "MIT Press", "location": "Cambridge"}},
    {"title": "Clean Code", "author": "Robert C. Martin",
     "year": 2008, "genre": "Software Engineering", "price": 39.99, "isbn": "978-0132350884",
     "tags": ["programming", "clean-code", "refactoring"],
     "publisher": {"name": "Prentice Hall", "location": "Upper Saddle River"}},
    {"title": "Hands-On Machine Learning", "author": "Aurelien Geron",
     "year": 2022, "genre": "Machine Learning", "price": 59.99, "isbn": "978-1098125974",
     "tags": ["AI", "scikit-learn", "tensorflow", "practical"],
     "publisher": {"name": "O'Reilly Media", "location": "Sebastopol"}},
]


def main():
    banner("Lab 2.2: Bookstore CRUD Operations")
    db = get_db("bookstore")
    col = reset_collection("bookstore", "books")

    # --- 1. CREATE ---
    print("=== CREATE: Inserting 5 Books ===")
    result = col.insert_many(BOOKS)
    print(f"[OK] Inserted {len(result.inserted_ids)} books successfully.")
    print(f"  Inserted IDs: {[str(_id)[:8] + '...' for _id in result.inserted_ids]}")

    # Initial Catalog Table
    table_init = Table(title="Initial Bookstore Inventory", show_lines=True)
    table_init.add_column("Title", style="cyan", width=36)
    table_init.add_column("Author", width=30)
    table_init.add_column("Year", justify="center", width=8)
    table_init.add_column("Genre", style="magenta", width=22)
    table_init.add_column("Price", justify="right", style="green", width=10)

    for b in col.find():
        table_init.add_row(b["title"], b["author"], str(b["year"]), b["genre"], f"${b['price']:.2f}")
    console.print()
    console.print(table_init)
    console.print()

    # --- 2. READ QUERIES ---
    print("=== READ: Querying Documents ===")

    print("\n[A] Filter by year > 2020:")
    recent = list(col.find({"year": {"$gt": 2020}}, {"title": 1, "year": 1, "price": 1, "_id": 0}))
    for b in recent:
        print(f"  {b['title']:<42} ({b['year']}) - ${b['price']:.2f}")

    print("\n[B] Filter by genre == 'Machine Learning':")
    ml_books = col.find({"genre": "Machine Learning"}, {"title": 1, "author": 1, "_id": 0})
    for b in ml_books:
        print(f"  {b['title']:<42} by {b['author']}")

    print("\n[C] Filter by price range $40 - $60:")
    mid_range = col.find({"price": {"$gte": 40, "$lte": 60}}, {"title": 1, "price": 1, "_id": 0})
    for b in mid_range:
        print(f"  {b['title']:<42} ${b['price']:.2f}")

    print("\n[D] Filter by tags array containing 'AI':")
    ai_books = col.find({"tags": "AI"}, {"title": 1, "tags": 1, "_id": 0})
    for b in ai_books:
        print(f"  {b['title']:<42} tags: {b['tags']}")

    # --- 3. UPDATE: 10% price increase on catalog ---
    print("\n=== UPDATE: 10% Global Price Increase ===")
    before = {b["title"]: b["price"] for b in col.find({}, {"title": 1, "price": 1, "_id": 0})}
    update_result = col.update_many({}, {"$mul": {"price": 1.10}})
    print(f"[OK] Modified {update_result.modified_count} book document(s).")
    after = {b["title"]: b["price"] for b in col.find({}, {"title": 1, "price": 1, "_id": 0})}
    for title, old_price in before.items():
        new_price = after[title]
        print(f"  {title:<42} ${old_price:.2f} -> ${new_price:.2f}")

    # --- 4. DELETE: Remove one book ---
    print("\n=== DELETE: Removing 'Clean Code' ===")
    del_result = col.delete_one({"title": "Clean Code"})
    print(f"[OK] Deleted {del_result.deleted_count} document(s).")
    print(f"  Remaining books count: {col.count_documents({})}")

    # Final Inventory Table
    print("\n=== Final Collection State ===")
    table_final = Table(title="Final Bookstore State in MongoDB", show_lines=True)
    table_final.add_column("Title", style="cyan", width=38)
    table_final.add_column("Year", justify="center", width=8)
    table_final.add_column("Genre", style="magenta", width=22)
    table_final.add_column("Updated Price", justify="right", style="bold green", width=14)

    for b in col.find({}, {"_id": 0}):
        table_final.add_row(b["title"], str(b["year"]), b["genre"], f"${b['price']:.2f}")
    console.print()
    console.print(table_final)
    console.print()

    # Export to respective MongoDB JSON file
    json_path = os.path.join(current_dir, "bookstore_books.json")
    export_collection_to_json("bookstore", "books", json_path)

    banner("Lab 2.2 Complete")


if __name__ == "__main__":
    main()
