import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date, datetime
from database import connect_db, create_table, check_admin


# Create tables before opening the application.
create_table()


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1200x760")
        self.root.minsize(950, 620)
        self.root.configure(bg="#f1f5f9")

        self.selected_book_id = None
        self.selected_student_id = None

        self.setup_style()
        self.show_login()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=27, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("TButton", font=("Arial", 10), padding=6)
        style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=9)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- LOGIN ----------------

    def show_login(self):
        self.clear_window()
        self.root.title("Library Management System - Admin Login")

        wrapper = tk.Frame(self.root, bg="#e2e8f0")
        wrapper.pack(fill="both", expand=True)

        card = tk.Frame(wrapper, bg="white", padx=45, pady=35)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card, text="LIBRARY MANAGEMENT",
            font=("Arial", 21, "bold"), bg="white", fg="#0f172a"
        ).pack(pady=(0, 8))

        tk.Label(
            card, text="Admin Login",
            font=("Arial", 13), bg="white", fg="#475569"
        ).pack(pady=(0, 22))

        tk.Label(card, text="Username", bg="white", anchor="w").pack(fill="x")
        self.username_entry = tk.Entry(card, width=32, font=("Arial", 11))
        self.username_entry.pack(pady=(5, 14), ipady=5)

        tk.Label(card, text="Password", bg="white", anchor="w").pack(fill="x")
        self.password_entry = tk.Entry(
            card, width=32, font=("Arial", 11), show="*"
        )
        self.password_entry.pack(pady=(5, 18), ipady=5)

        ttk.Button(
            card, text="Login", command=self.login
        ).pack(fill="x")

        tk.Label(
            card, text="Default: admin / admin123",
            bg="white", fg="#64748b", font=("Arial", 9)
        ).pack(pady=(15, 0))

        self.password_entry.bind("<Return>", lambda event: self.login())
        self.username_entry.focus_set()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if check_admin(username, password):
            self.show_dashboard()
        else:
            messagebox.showerror(
                "Login Failed", "Incorrect username or password."
            )

    # ---------------- MAIN DASHBOARD ----------------

    def show_dashboard(self):
        self.clear_window()
        self.root.title("Library Management System")
        self.root.geometry("1200x760")

        header = tk.Frame(self.root, bg="#0f172a", height=62)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="LIBRARY MANAGEMENT SYSTEM",
            bg="#0f172a", fg="white",
            font=("Arial", 18, "bold")
        ).pack(side="left", padx=20, pady=14)

        ttk.Button(
            header, text="Logout", command=self.logout
        ).pack(side="right", padx=18, pady=12)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.dashboard_tab = tk.Frame(self.notebook, bg="#f1f5f9")
        self.book_tab = tk.Frame(self.notebook, bg="#f1f5f9")
        self.student_tab = tk.Frame(self.notebook, bg="#f1f5f9")
        self.issue_tab = tk.Frame(self.notebook, bg="#f1f5f9")
        self.overdue_tab = tk.Frame(self.notebook, bg="#f1f5f9")

        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.book_tab, text="Book Management")
        self.notebook.add(self.student_tab, text="Student Management")
        self.notebook.add(self.issue_tab, text="Issue / Return")
        self.notebook.add(self.overdue_tab, text="Overdue Books")

        self.build_dashboard_tab()
        self.build_book_tab()
        self.build_student_tab()
        self.build_issue_tab()
        self.build_overdue_tab()

        self.refresh_all()

    def logout(self):
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            self.show_login()

    def make_tree(self, parent, columns, widths=None, height=10):
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=14, pady=10)

        tree = ttk.Treeview(
            frame, columns=columns, show="headings", height=height
        )
        for index, col in enumerate(columns):
            tree.heading(col, text=col)
            width = widths[index] if widths else 130
            tree.column(col, width=width, anchor="center")

        yscroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        return tree

    # ---------------- DASHBOARD ----------------

    def build_dashboard_tab(self):
        tk.Label(
            self.dashboard_tab, text="Dashboard",
            font=("Arial", 23, "bold"), bg="#f1f5f9", fg="#0f172a"
        ).pack(pady=28)

        cards = tk.Frame(self.dashboard_tab, bg="#f1f5f9")
        cards.pack(pady=25)

        self.stat_labels = {}
        stats = [
            ("Total Books", "#2563eb"),
            ("Total Students", "#16a34a"),
            ("Issued Books", "#ea580c"),
            ("Returned Books", "#7c3aed"),
            ("Overdue Books", "#dc2626"),
        ]

        for title, color in stats:
            card = tk.Frame(cards, bg="white", padx=20, pady=20)
            card.pack(side="left", padx=8, pady=8)
            tk.Label(
                card, text=title, bg="white", fg="#475569",
                font=("Arial", 10, "bold")
            ).pack()
            value = tk.Label(
                card, text="0", bg="white", fg=color,
                font=("Arial", 24, "bold")
            )
            value.pack(pady=(8, 0))
            self.stat_labels[title] = value

        tk.Label(
            self.dashboard_tab,
            text="Use the tabs above to manage books, students and issue records.",
            bg="#f1f5f9", fg="#475569", font=("Arial", 11)
        ).pack(pady=20)

    def refresh_dashboard(self):
        conn = connect_db()
        cur = conn.cursor()
        queries = {
            "Total Books": "SELECT COUNT(*) FROM books",
            "Total Students": "SELECT COUNT(*) FROM students",
            "Issued Books": "SELECT COUNT(*) FROM issue_records WHERE status='Issued'",
            "Returned Books": "SELECT COUNT(*) FROM issue_records WHERE status='Returned'",
            "Overdue Books": """
                SELECT COUNT(*) FROM issue_records
                WHERE status='Issued' AND due_date < ?
            """
        }
        for label, query in queries.items():
            if label == "Overdue Books":
                cur.execute(query, (date.today().isoformat(),))
            else:
                cur.execute(query)
            self.stat_labels[label].config(text=str(cur.fetchone()[0]))
        conn.close()

    # ---------------- BOOK MANAGEMENT ----------------

    def build_book_tab(self):
        tk.Label(
            self.book_tab, text="Book Management",
            font=("Arial", 21, "bold"), bg="#f1f5f9"
        ).pack(pady=12)

        form = tk.Frame(self.book_tab, bg="#f1f5f9")
        form.pack(pady=5)

        self.book_title = self.add_field(form, "Book Title", 0, 0)
        self.book_author = self.add_field(form, "Author", 0, 2)
        self.book_category = self.add_field(form, "Category", 1, 0)
        self.book_quantity = self.add_field(form, "Quantity", 1, 2)

        buttons = tk.Frame(self.book_tab, bg="#f1f5f9")
        buttons.pack(pady=7)
        ttk.Button(buttons, text="Add Book", command=self.add_book).pack(side="left", padx=4)
        ttk.Button(buttons, text="Update Selected", command=self.update_book).pack(side="left", padx=4)
        ttk.Button(buttons, text="Delete Selected", command=self.delete_book).pack(side="left", padx=4)
        ttk.Button(buttons, text="Clear", command=self.clear_book_form).pack(side="left", padx=4)

        search_frame = tk.Frame(self.book_tab, bg="#f1f5f9")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:", bg="#f1f5f9").pack(side="left", padx=5)
        self.book_search = tk.Entry(search_frame, width=30)
        self.book_search.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_books).pack(side="left", padx=3)
        ttk.Button(search_frame, text="Show All", command=self.refresh_books).pack(side="left", padx=3)

        self.book_tree = self.make_tree(
            self.book_tab,
            ("ID", "Title", "Author", "Category", "Quantity"),
            (70, 240, 200, 150, 100), 9
        )
        self.book_tree.bind("<<TreeviewSelect>>", self.select_book)

    def add_field(self, parent, label, row, col):
        tk.Label(parent, text=label, bg="#f1f5f9").grid(
            row=row, column=col, padx=7, pady=6, sticky="e"
        )
        entry = tk.Entry(parent, width=25)
        entry.grid(row=row, column=col + 1, padx=7, pady=6)
        return entry

    def clear_book_form(self):
        self.selected_book_id = None
        for entry in (
            self.book_title, self.book_author,
            self.book_category, self.book_quantity
        ):
            entry.delete(0, tk.END)

    def add_book(self):
        title = self.book_title.get().strip()
        author = self.book_author.get().strip()
        category = self.book_category.get().strip()
        quantity_text = self.book_quantity.get().strip()

        if not title or not author or not quantity_text:
            messagebox.showerror("Error", "Title, Author and Quantity are required.")
            return
        try:
            quantity = int(quantity_text)
            if quantity < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be zero or a positive whole number.")
            return

        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO books (title, author, category, quantity) VALUES (?, ?, ?, ?)",
            (title, author, category, quantity)
        )
        conn.commit()
        conn.close()
        self.clear_book_form()
        self.refresh_all()
        messagebox.showinfo("Success", "Book added successfully.")

    def refresh_books(self):
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT book_id, title, author, category, quantity FROM books ORDER BY book_id")
        for row in cur.fetchall():
            self.book_tree.insert("", "end", values=row)
        conn.close()

    def search_books(self):
        keyword = self.book_search.get().strip()
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT book_id, title, author, category, quantity
            FROM books
            WHERE title LIKE ? OR author LIKE ? OR category LIKE ?
            ORDER BY book_id
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        for row in cur.fetchall():
            self.book_tree.insert("", "end", values=row)
        conn.close()

    def select_book(self, event=None):
        selected = self.book_tree.selection()
        if not selected:
            return
        values = self.book_tree.item(selected[0], "values")
        self.selected_book_id = values[0]
        self.clear_entries_only(
            self.book_title, self.book_author,
            self.book_category, self.book_quantity
        )
        self.book_title.insert(0, values[1])
        self.book_author.insert(0, values[2])
        self.book_category.insert(0, values[3] or "")
        self.book_quantity.insert(0, values[4])

    def update_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("Select Book", "Select a book from the table first.")
            return
        title = self.book_title.get().strip()
        author = self.book_author.get().strip()
        category = self.book_category.get().strip()
        try:
            quantity = int(self.book_quantity.get().strip())
            if quantity < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid non-negative quantity.")
            return
        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required.")
            return

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE books SET title=?, author=?, category=?, quantity=?
            WHERE book_id=?
        """, (title, author, category, quantity, self.selected_book_id))
        conn.commit()
        conn.close()
        self.clear_book_form()
        self.refresh_all()
        messagebox.showinfo("Success", "Book updated successfully.")

    def delete_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("Select Book", "Select a book from the table first.")
            return
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM issue_records WHERE book_id=? AND status='Issued'",
            (self.selected_book_id,)
        )
        active = cur.fetchone()[0]
        if active:
            conn.close()
            messagebox.showerror("Cannot Delete", "This book has an active issue record. Return it first.")
            return
        if messagebox.askyesno("Confirm", "Delete the selected book?"):
            cur.execute("DELETE FROM books WHERE book_id=?", (self.selected_book_id,))
            conn.commit()
            conn.close()
            self.clear_book_form()
            self.refresh_all()
            messagebox.showinfo("Success", "Book deleted.")
        else:
            conn.close()

    # ---------------- STUDENT MANAGEMENT ----------------

    def build_student_tab(self):
        tk.Label(
            self.student_tab, text="Student Management",
            font=("Arial", 21, "bold"), bg="#f1f5f9"
        ).pack(pady=12)

        form = tk.Frame(self.student_tab, bg="#f1f5f9")
        form.pack(pady=5)
        self.student_id = self.add_field(form, "Student ID", 0, 0)
        self.student_name = self.add_field(form, "Name", 0, 2)
        self.student_email = self.add_field(form, "Email", 1, 0)
        self.student_phone = self.add_field(form, "Phone", 1, 2)

        buttons = tk.Frame(self.student_tab, bg="#f1f5f9")
        buttons.pack(pady=7)
        ttk.Button(buttons, text="Add Student", command=self.add_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Update Selected", command=self.update_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Delete Selected", command=self.delete_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Clear", command=self.clear_student_form).pack(side="left", padx=4)

        search_frame = tk.Frame(self.student_tab, bg="#f1f5f9")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:", bg="#f1f5f9").pack(side="left", padx=5)
        self.student_search = tk.Entry(search_frame, width=30)
        self.student_search.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_students).pack(side="left", padx=3)
        ttk.Button(search_frame, text="Show All", command=self.refresh_students).pack(side="left", padx=3)

        self.student_tree = self.make_tree(
            self.student_tab,
            ("Student ID", "Name", "Email", "Phone"),
            (150, 220, 240, 160), 9
        )
        self.student_tree.bind("<<TreeviewSelect>>", self.select_student)

    @staticmethod
    def clear_entries_only(*entries):
        for entry in entries:
            entry.delete(0, tk.END)

    def clear_student_form(self):
        self.selected_student_id = None
        self.clear_entries_only(
            self.student_id, self.student_name,
            self.student_email, self.student_phone
        )
        self.student_id.config(state="normal")

    def add_student(self):
        sid = self.student_id.get().strip()
        name = self.student_name.get().strip()
        email = self.student_email.get().strip()
        phone = self.student_phone.get().strip()
        if not sid or not name:
            messagebox.showerror("Error", "Student ID and Name are required.")
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO students (student_id, name, email, phone) VALUES (?, ?, ?, ?)",
                (sid, name, email, phone)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            messagebox.showerror("Error", "That Student ID already exists.")
            return
        conn.close()
        self.clear_student_form()
        self.refresh_all()
        messagebox.showinfo("Success", "Student added successfully.")

    def refresh_students(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT student_id, name, email, phone FROM students ORDER BY student_id")
        for row in cur.fetchall():
            self.student_tree.insert("", "end", values=row)
        conn.close()

    def search_students(self):
        keyword = self.student_search.get().strip()
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT student_id, name, email, phone FROM students
            WHERE student_id LIKE ? OR name LIKE ? OR email LIKE ?
            ORDER BY student_id
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        for row in cur.fetchall():
            self.student_tree.insert("", "end", values=row)
        conn.close()

    def select_student(self, event=None):
        selected = self.student_tree.selection()
        if not selected:
            return
        values = self.student_tree.item(selected[0], "values")
        self.selected_student_id = values[0]
        self.clear_entries_only(
            self.student_id, self.student_name,
            self.student_email, self.student_phone
        )
        self.student_id.insert(0, values[0])
        self.student_name.insert(0, values[1])
        self.student_email.insert(0, values[2] or "")
        self.student_phone.insert(0, values[3] or "")
        self.student_id.config(state="disabled")

    def update_student(self):
        if self.selected_student_id is None:
            messagebox.showwarning("Select Student", "Select a student from the table first.")
            return
        name = self.student_name.get().strip()
        email = self.student_email.get().strip()
        phone = self.student_phone.get().strip()
        if not name:
            messagebox.showerror("Error", "Student name is required.")
            return
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE students SET name=?, email=?, phone=? WHERE student_id=?",
            (name, email, phone, self.selected_student_id)
        )
        conn.commit()
        conn.close()
        self.clear_student_form()
        self.refresh_all()
        messagebox.showinfo("Success", "Student updated successfully.")

    def delete_student(self):
        if self.selected_student_id is None:
            messagebox.showwarning("Select Student", "Select a student from the table first.")
            return
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM issue_records WHERE student_id=? AND status='Issued'",
            (self.selected_student_id,)
        )
        active = cur.fetchone()[0]
        if active:
            conn.close()
            messagebox.showerror("Cannot Delete", "This student has an unreturned book. Return it first.")
            return
        if messagebox.askyesno("Confirm", "Delete the selected student?"):
            cur.execute("DELETE FROM students WHERE student_id=?", (self.selected_student_id,))
            conn.commit()
            conn.close()
            self.clear_student_form()
            self.refresh_all()
            messagebox.showinfo("Success", "Student deleted.")
        else:
            conn.close()

    # ---------------- ISSUE / RETURN ----------------

    def build_issue_tab(self):
        tk.Label(
            self.issue_tab, text="Issue / Return Management",
            font=("Arial", 21, "bold"), bg="#f1f5f9"
        ).pack(pady=12)

        form = tk.Frame(self.issue_tab, bg="#f1f5f9")
        form.pack(pady=8)

        tk.Label(form, text="Book ID", bg="#f1f5f9").grid(row=0, column=0, padx=7, pady=6)
        self.issue_book_id = tk.Entry(form, width=22)
        self.issue_book_id.grid(row=0, column=1, padx=7, pady=6)

        tk.Label(form, text="Student ID", bg="#f1f5f9").grid(row=0, column=2, padx=7, pady=6)
        self.issue_student_id = tk.Entry(form, width=22)
        self.issue_student_id.grid(row=0, column=3, padx=7, pady=6)

        tk.Label(form, text="Due Date (YYYY-MM-DD)", bg="#f1f5f9").grid(row=1, column=0, padx=7, pady=6)
        self.issue_due_date = tk.Entry(form, width=22)
        self.issue_due_date.grid(row=1, column=1, padx=7, pady=6)
        self.issue_due_date.insert(0, date.today().isoformat())

        buttons = tk.Frame(self.issue_tab, bg="#f1f5f9")
        buttons.pack(pady=7)
        ttk.Button(buttons, text="Issue Book", command=self.issue_book).pack(side="left", padx=5)
        ttk.Button(buttons, text="Return Selected Book", command=self.return_book).pack(side="left", padx=5)
        ttk.Button(buttons, text="Refresh Records", command=self.refresh_issues).pack(side="left", padx=5)

        columns = (
            "Issue ID", "Book ID", "Book Title", "Student ID",
            "Student Name", "Issue Date", "Due Date", "Return Date", "Status"
        )
        self.issue_tree = self.make_tree(
            self.issue_tab, columns,
            (70, 70, 160, 100, 150, 110, 110, 110, 90), 12
        )

    def refresh_issues(self):
        for item in self.issue_tree.get_children():
            self.issue_tree.delete(item)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT ir.issue_id, ir.book_id, COALESCE(b.title, ''),
                   ir.student_id, COALESCE(s.name, ''),
                   ir.issue_date, ir.due_date, COALESCE(ir.return_date, ''),
                   ir.status
            FROM issue_records ir
            LEFT JOIN books b ON b.book_id = ir.book_id
            LEFT JOIN students s ON s.student_id = ir.student_id
            ORDER BY ir.issue_id DESC
        """)
        for row in cur.fetchall():
            self.issue_tree.insert("", "end", values=row)
        conn.close()

    def issue_book(self):
        book_id = self.issue_book_id.get().strip()
        student_id = self.issue_student_id.get().strip()
        due_date = self.issue_due_date.get().strip()

        if not book_id or not student_id or not due_date:
            messagebox.showerror("Error", "Fill in Book ID, Student ID and Due Date.")
            return
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Use YYYY-MM-DD, for example 2026-11-10.")
            return
        if due_date < date.today().isoformat():
            messagebox.showerror("Invalid Date", "Due date cannot be before today.")
            return

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT quantity FROM books WHERE book_id=?", (book_id,))
        book = cur.fetchone()
        if book is None:
            conn.close()
            messagebox.showerror("Error", "Book ID not found.")
            return
        if book[0] <= 0:
            conn.close()
            messagebox.showerror("Unavailable", "No copy of this book is currently available.")
            return

        cur.execute("SELECT 1 FROM students WHERE student_id=?", (student_id,))
        if cur.fetchone() is None:
            conn.close()
            messagebox.showerror("Error", "Student ID not found.")
            return

        cur.execute("""
            INSERT INTO issue_records
            (book_id, student_id, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, 'Issued')
        """, (book_id, student_id, date.today().isoformat(), due_date))
        cur.execute(
            "UPDATE books SET quantity=quantity-1 WHERE book_id=?",
            (book_id,)
        )
        conn.commit()
        conn.close()

        self.issue_book_id.delete(0, tk.END)
        self.issue_student_id.delete(0, tk.END)
        self.issue_due_date.delete(0, tk.END)
        self.issue_due_date.insert(0, date.today().isoformat())
        self.refresh_all()
        messagebox.showinfo("Success", "Book issued successfully.")

    def return_book(self):
        selected = self.issue_tree.selection()
        if not selected:
            messagebox.showwarning("Select Record", "Select an issue record first.")
            return
        values = self.issue_tree.item(selected[0], "values")
        issue_id, book_id, status = values[0], values[1], values[8]
        if status == "Returned":
            messagebox.showinfo("Already Returned", "This book has already been returned.")
            return

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE issue_records
            SET status='Returned', return_date=?
            WHERE issue_id=? AND status='Issued'
        """, (date.today().isoformat(), issue_id))
        if cur.rowcount == 0:
            conn.close()
            messagebox.showwarning("Notice", "This record has already been returned.")
            return
        cur.execute(
            "UPDATE books SET quantity=quantity+1 WHERE book_id=?",
            (book_id,)
        )
        conn.commit()
        conn.close()
        self.refresh_all()
        messagebox.showinfo("Success", "Book returned successfully.")

    # ---------------- OVERDUE BOOKS ----------------

    def build_overdue_tab(self):
        tk.Label(
            self.overdue_tab, text="Overdue Books",
            font=("Arial", 21, "bold"), bg="#f1f5f9", fg="#0f172a"
        ).pack(pady=12)

        self.overdue_count = tk.Label(
            self.overdue_tab, text="Total Overdue Books: 0",
            font=("Arial", 13, "bold"), bg="#f1f5f9", fg="#dc2626"
        )
        self.overdue_count.pack(pady=6)

        columns = (
            "Issue ID", "Book ID", "Book Title", "Student ID",
            "Student Name", "Issue Date", "Due Date", "Days Late"
        )
        self.overdue_tree = self.make_tree(
            self.overdue_tab, columns,
            (75, 75, 180, 100, 160, 110, 110, 90), 14
        )
        ttk.Button(
            self.overdue_tab, text="Refresh Overdue Books",
            command=self.refresh_overdue
        ).pack(pady=8)

    def refresh_overdue(self):
        for item in self.overdue_tree.get_children():
            self.overdue_tree.delete(item)

        today = date.today()
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT ir.issue_id, ir.book_id, COALESCE(b.title, ''),
                   ir.student_id, COALESCE(s.name, ''),
                   ir.issue_date, ir.due_date
            FROM issue_records ir
            LEFT JOIN books b ON b.book_id=ir.book_id
            LEFT JOIN students s ON s.student_id=ir.student_id
            WHERE ir.status='Issued' AND ir.due_date < ?
            ORDER BY ir.due_date
        """, (today.isoformat(),))
        rows = cur.fetchall()
        conn.close()

        for row in rows:
            try:
                due = datetime.strptime(row[6], "%Y-%m-%d").date()
                days_late = (today - due).days
            except (ValueError, TypeError):
                days_late = "Date error"
            self.overdue_tree.insert(
                "", "end",
                values=(*row, days_late)
            )
        self.overdue_count.config(text=f"Total Overdue Books: {len(rows)}")

    # ---------------- REFRESH ----------------

    def refresh_all(self):
        self.refresh_books()
        self.refresh_students()
        self.refresh_issues()
        self.refresh_overdue()
        self.refresh_dashboard()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
