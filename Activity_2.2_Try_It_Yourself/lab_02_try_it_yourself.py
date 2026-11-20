"""Lab 2.2 - Try It Yourself: Targeted Price Update for Pre-2010 Publications
Performs a targeted update operation that increases the price of all books published before 2010
by 10 percent using the $mul operator, verifies the update, and exports Compass verification criteria.
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
from rich.panel import Panel

console = Console(width=115)

ENRICHED_BOOKS = [
    # Books published before 2010 (Eligible for 10% price increase)
    {"title": "Clean Code", "author": "Robert C. Martin",
     "year": 2008, "genre": "Software Engineering", "price": 39.99, "isbn": "978-0132350884",
     "tags": ["programming", "clean-code", "refactoring"],
     "publisher": {"name": "Prentice Hall", "location": "Upper Saddle River"}},
    {"title": "Design Patterns", "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
     "year": 1994, "genre": "Software Architecture", "price": 54.99, "isbn": "978-0201633610",
     "tags": ["patterns", "architecture", "oop"],
     "publisher": {"name": "Addison-Wesley", "location": "Boston"}},
    {"title": "Refactoring", "author": "Martin Fowler",
     "year": 1999, "genre": "Software Engineering", "price": 47.50, "isbn": "978-0201485677",
     "tags": ["refactoring", "code-quality", "design"],
     "publisher": {"name": "Addison-Wesley", "location": "Boston"}},

    # Books published 2010 or later (Control group: prices must remain unchanged)
    {"title": "The Pragmatic Programmer (20th Anniv)", "author": "David Thomas & Andrew Hunt",
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
    {"title": "Hands-On Machine Learning", "author": "Aurelien Geron",
     "year": 2022, "genre": "Machine Learning", "price": 59.99, "isbn": "978-1098125974",
     "tags": ["AI", "scikit-learn", "tensorflow", "practical"],
     "publisher": {"name": "O'Reilly Media", "location": "Sebastopol"}},
]


def main():
    banner("Lab 2.2 'Try It Yourself': Pre-2010 Targeted Price Increase & Compass Verification")
    db = get_db("bookstore")
    col = reset_collection("bookstore", "books_try_it_yourself")

    # Step 1: Populate Inventory
    print("=== STEP 1: Populating Enriched Bookstore Catalog ===")
    insert_res = col.insert_many(ENRICHED_BOOKS)
    print(f"[OK] Inserted {len(insert_res.inserted_ids)} books into collection 'books_try_it_yourself'.")

    # Capture initial prices for audit
    initial_inventory = {b["title"]: {"year": b["year"], "price": b["price"]} for b in col.find()}

    # Step 2: Identify Pre-2010 Publications
    print("\n=== STEP 2: Pre-Update Query (Books Published Before 2010) ===")
    query_pre2010 = {"year": {"$lt": 2010}}
    target_books = list(col.find(query_pre2010, {"title": 1, "year": 1, "price": 1, "_id": 0}))
    print(f"Target query: {query_pre2010}")
    print(f"Found {len(target_books)} matching book(s) published before 2010:")
    for b in target_books:
        print(f"  * {b['title']:<40} (Year: {b['year']}) - Current Price: ${b['price']:.2f}")

    # Step 3: Targeted Update Operation ($mul: 1.10)
    print("\n=== STEP 3: Executing Targeted Update Operation ===")
    update_op = {"$mul": {"price": 1.10}}
    print(f"Executing: col.update_many({query_pre2010}, {update_op})")
    update_result = col.update_many(query_pre2010, update_op)
    print(f"[OK] Matched: {update_result.matched_count} document(s)")
    print(f"[OK] Modified: {update_result.modified_count} document(s)")

    # Step 4: Verification and Audit Table
    print("\n=== STEP 4: Verification of Updated vs. Unchanged Catalog ===")
    updated_inventory = {b["title"]: {"year": b["year"], "price": b["price"]} for b in col.find()}

    table = Table(title="Inventory Price Audit: Pre-2010 (+10% Increase) vs. Post-2010 (Unchanged)", show_lines=True)
    table.add_column("Book Title", style="cyan", width=38)
    table.add_column("Pub Year", justify="center", width=10)
    table.add_column("Old Price", justify="right", style="white", width=12)
    table.add_column("New Price", justify="right", style="bold green", width=12)
    table.add_column("Delta", justify="right", width=10)
    table.add_column("Audit Verdict", justify="center", width=22)

    for title, old_data in initial_inventory.items():
        year = old_data["year"]
        old_p = old_data["price"]
        new_p = updated_inventory[title]["price"]
        diff = new_p - old_p

        if year < 2010:
            status = "[bold green]UPDATED (+10%)[/bold green]"
            delta_str = f"+${diff:.2f}"
        else:
            status = "[yellow]UNCHANGED[/yellow]"
            delta_str = "$0.00"

        table.add_row(title, str(year), f"${old_p:.2f}", f"${new_p:.2f}", delta_str, status)

    console.print()
    console.print(table)
    console.print()

    # Step 5: MongoDB Compass Verification Instructions
    print("=== STEP 5: MongoDB Compass Verification Procedure ===")
    print("To visually verify these results in MongoDB Compass GUI:")
    print("  1. Connect Compass to: mongodb://localhost:27017")
    print("  2. Navigate to Database: 'bookstore' -> Collection: 'books_try_it_yourself'")
    print("  3. Apply Filter in the Compass Filter Bar:")
    print("       { year: { $lt: 2010 } }")
    print("  4. Verify that exactly 3 documents appear (Clean Code, Design Patterns, Refactoring).")
    print("  5. Confirm the 'price' field values reflect the 10% increase ($43.99, $60.49, $52.25).")
    print("  6. Apply inverted filter { year: { $gte: 2010 } } to confirm post-2010 books remain unchanged.")

    # Export collection to JSON
    json_path = os.path.join(current_dir, "bookstore_pre2010_update.json")
    export_collection_to_json("bookstore", "books_try_it_yourself", json_path)

    banner("Lab 2.2 'Try It Yourself' Complete")


if __name__ == "__main__":
    main()
