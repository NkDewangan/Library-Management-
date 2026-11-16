import json
from datetime import date

# Load and Save Data
def load(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


books = load("books.json")
students = load("students.json")
issued = load("issued_books.json")


# Add Book
def add_book():
    bid = input("Enter Book ID: ")

    if any(b["book_id"] == bid for b in books):
        print("Book ID already exists!")
        return

    name = input("Book Name: ")
    author = input("Author Name: ")
    category = input("Category: ")

    try:
        copies = int(input("Number of Copies: "))
        if copies <= 0:
            print("Copies must be greater than zero!")
            return
    except ValueError:
        print("Invalid number!")
        return

    books.append({
        "book_id": bid,
        "book_name": name,
        "author": author,
        "category": category,
        "available_copies": copies,
        "total_copies": copies
    })

    save("books.json", books)
    print("Book Added Successfully!")


# Display Books
def display_books():
    if not books:
        print("No Books Available!")
        return

    for b in sorted(books, key=lambda x: x["book_name"].lower()):
        print(b)


# Search Book
def search_book():
    key = input("Enter Book ID, Name or Author: ").lower()

    found = False
    for b in books:
        if (key in b["book_id"].lower()
                or key in b["book_name"].lower()
                or key in b["author"].lower()):
            print(b)
            found = True

    if not found:
        print("Book Not Found!")


# Register Student
def register_student():
    sid = input("Enter Student ID: ")

    if any(s["student_id"] == sid for s in students):
        print("Student ID already exists!")
        return

    student = {
        "student_id": sid,
        "student_name": input("Student Name: "),
        "department": input("Department: "),
        "contact_number": input("Contact Number: ")
    }

    students.append(student)
    save("students.json", students)
    print("Student Registered Successfully!")


# Issue Book
def issue_book():
    sid = input("Enter Student ID: ")
    bid = input("Enter Book ID: ")

    student = next((s for s in students if s["student_id"] == sid), None)
    book = next((b for b in books if b["book_id"] == bid), None)

    if not student or not book:
        print("Student or Book Not Found!")
        return

    count = sum(1 for i in issued if i["student_id"] == sid)

    if book["available_copies"] <= 0:
        print("Book Not Available!")
    elif count >= 3:
        print("Maximum 3 Books Allowed!")
    else:
        book["available_copies"] -= 1
        issued.append({
            "student_id": sid,
            "book_id": bid,
            "issue_date": str(date.today())
        })
        save("books.json", books)
        save("issued_books.json", issued)
        print("Book Issued Successfully!")


# Return Book
def return_book():
    sid = input("Enter Student ID: ")
    bid = input("Enter Book ID: ")

    for i in issued:
        if i["student_id"] == sid and i["book_id"] == bid:
            issued.remove(i)

            book = next((b for b in books if b["book_id"] == bid), None)
            if book:
                book["available_copies"] += 1
                save("books.json", books)

            save("issued_books.json", issued)
            print("Book Returned Successfully!")
            return

    print("Issue Record Not Found!")


# Display Issued Books
def display_issued():
    if not issued:
        print("No Books Issued!")
    else:
        for i in issued:
            print(i)


# Delete Book
def delete_book():
    bid = input("Enter Book ID: ")

    if any(i["book_id"] == bid for i in issued):
        print("Book is currently issued!")
        return

    for b in books:
        if b["book_id"] == bid:
            books.remove(b)
            save("books.json", books)
            print("Book Deleted Successfully!")
            return

    print("Book Not Found!")


# Main Menu
while True:
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Add New Book")
    print("2. Display All Books")
    print("3. Search Book")
    print("4. Register Student")
    print("5. Issue Book")
    print("6. Return Book")
    print("7. Display Issued Books")
    print("8. Delete Book")
    print("9. Exit")

    choice = input("Enter Your Choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        display_books()
    elif choice == "3":
        search_book()
    elif choice == "4":
        register_student()
    elif choice == "5":
        issue_book()
    elif choice == "6":
        return_book()
    elif choice == "7":
        display_issued()
    elif choice == "8":
        delete_book()
    elif choice == "9":
        print("Thank You!")
        break
    else:
        print("Invalid Choice!")
