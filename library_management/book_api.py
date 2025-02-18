import frappe
from frappe import _

# Function to handle GET request for retrieving all books
@frappe.whitelist(allow_guest=True)
def get_books():
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    try:
        books = frappe.get_all("Book", fields=["name", "book_title", "author", "isbn", "publisher", "status", "publish_date", "description"])
        return books
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}

# Function to handle GET request for retrieving a single book
@frappe.whitelist(allow_guest=True)
def get_book(book_title):
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    try:
        book = frappe.get_doc("Book", book_title)
        return {
            "name": book.name,
            "book_title": book.book_title,
            "author": book.author,
            "isbn": book.isbn,
            "publisher": book.publisher,
            "status": book.status,
            "publish_date": book.publish_date,
            "description": book.description
        }
    except frappe.DoesNotExistError:
        return {"Error": "Book not found."}
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}

# Function to handle POST request for creating a new book
@frappe.whitelist(allow_guest=True)
def create_book(book_title, author, isbn, publisher, status, publish_date, description):
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    try:
        existing_book = frappe.get_all("Book", filters={"isbn": isbn}, fields=["name"])
        if existing_book:
            return {"Error": "A book with this ISBN already exists."}
        
        book = frappe.get_doc({
            "doctype": "Book",
            "book_title": book_title,
            "author": author,
            "isbn": isbn,
            "publisher": publisher,
            "status": status,
            "publish_date": publish_date,
            "description": description
        })
        book.insert()
        return {
            "name": book.name,
            "book_title": book.book_title,
            "author": book.author,
            "isbn": book.isbn,
            "publisher": book.publisher,
            "status": book.status,
            "publish_date": book.publish_date,
            "description": book.description
        }
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}

# Function to handle PUT request for updating a book
@frappe.whitelist(allow_guest=True)
def update_book(name, book_title, author, isbn, publisher, status, publish_date, description):
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    try:
        book = frappe.get_doc("Book", name)

        book.book_title = book_title
        book.author = author
        book.isbn = isbn
        book.publisher = publisher
        book.status = status
        book.publish_date = publish_date
        book.description = description
        
        book.save()

        return {
            "name": book.name,
            "book_title": book.book_title,
            "author": book.author,
            "isbn": book.isbn,
            "publisher": book.publisher,
            "status": book.status,
            "publish_date": book.publish_date,
            "description": book.description
        }
    except frappe.DoesNotExistError:
        return {"Error": "Book not found."}
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}

# Function to handle DELETE request for deleting a book
@frappe.whitelist(allow_guest=True)
def delete_book(book_title):
    if frappe.session.user == "Guest":
        return {"Error": "You must be logged in to access this data."}
    try:
        book = frappe.get_doc("Book", book_title)
        book.delete()  
        return {"message": _("Book deleted successfully")}
    except frappe.DoesNotExistError:
        return {"Error": "Book not found."}
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}
