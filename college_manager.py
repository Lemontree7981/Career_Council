import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from database_operations import DatabaseManager, College
import sqlite3

class CollegeManagerGUI:
    def __init__(self):
        self.root = ttk.Window(themename="cosmo")
        self.root.title("College Database Manager")
        self.root.geometry("1000x800")

        self.db_manager = DatabaseManager('career_counseling.db')

        # Main container
        self.main_container = ttk.Frame(self.root, padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Create the interface sections
        self.create_header()
        self.create_add_college_form()
        self.create_college_list()
        self.load_colleges()

    def create_header(self):
        """Create the application header."""
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title = ttk.Label(
            header_frame,
            text="College Database Manager",
            font=("Helvetica", 24, "bold")
        )
        title.pack()

        subtitle = ttk.Label(
            header_frame,
            text="Add, Update, or Delete College Information",
            font=("Helvetica", 12)
        )
        subtitle.pack()

    def create_add_college_form(self):
        """Create the form for adding/editing college details."""
        self.form_frame = ttk.LabelFrame(
            self.main_container,
            text="College Details",
            padding="20"
        )
        self.form_frame.pack(fill=tk.X, pady=(0, 20))

        # College Name
        name_frame = ttk.Frame(self.form_frame)
        name_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(name_frame, text="College Name:").pack(side=tk.LEFT)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            name_frame,
            textvariable=self.name_var,
            width=50
        )
        self.name_entry.pack(side=tk.LEFT, padx=(10, 0))

        # Location
        location_frame = ttk.Frame(self.form_frame)
        location_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(location_frame, text="Location:").pack(side=tk.LEFT)
        self.location_var = tk.StringVar()
        self.location_entry = ttk.Entry(
            location_frame,
            textvariable=self.location_var,
            width=50
        )
        self.location_entry.pack(side=tk.LEFT, padx=(10, 0))

        # Field
        field_frame = ttk.Frame(self.form_frame)
        field_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(field_frame, text="Field:").pack(side=tk.LEFT)
        self.field_var = tk.StringVar(value="Engineering")
        fields = ["Engineering", "Medicine", "Architecture"]
        self.field_combobox = ttk.Combobox(
            field_frame,
            textvariable=self.field_var,
            values=fields,
            state="readonly",
            width=47
        )
        self.field_combobox.pack(side=tk.LEFT, padx=(10, 0))

        # Tuition Fee
        fee_frame = ttk.Frame(self.form_frame)
        fee_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(fee_frame, text="Tuition Fee (₹):").pack(side=tk.LEFT)
        self.fee_var = tk.StringVar()
        self.fee_entry = ttk.Entry(
            fee_frame,
            textvariable=self.fee_var,
            width=50
        )
        self.fee_entry.pack(side=tk.LEFT, padx=(10, 0))

        # Cutoff Details
        cutoff_frame = ttk.LabelFrame(self.form_frame, text="Cutoff Scores", padding="10")
        cutoff_frame.pack(fill=tk.X, pady=(10, 10))

        # Exam Selection
        exam_frame = ttk.Frame(cutoff_frame)
        exam_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(exam_frame, text="Exam:").pack(side=tk.LEFT)
        self.exam_var = tk.StringVar()
        self.exam_combobox = ttk.Combobox(
            exam_frame,
            textvariable=self.exam_var,
            values=self.get_exams(),
            state="readonly",
            width=30
        )
        self.exam_combobox.pack(side=tk.LEFT, padx=(10, 0))

        # Cutoff scores for different categories
        categories_frame = ttk.Frame(cutoff_frame)
        categories_frame.pack(fill=tk.X)

        self.cutoff_vars = {}
        categories = ["General", "OBC", "SC", "ST"]
        for category in categories:
            frame = ttk.Frame(categories_frame)
            frame.pack(fill=tk.X, pady=(0, 5))
            ttk.Label(frame, text=f"{category}:").pack(side=tk.LEFT)
            var = tk.StringVar()
            self.cutoff_vars[category] = var
            entry = ttk.Entry(frame, textvariable=var, width=20)
            entry.pack(side=tk.LEFT, padx=(10, 0))

        # Buttons
        button_frame = ttk.Frame(self.form_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        self.add_button = ttk.Button(
            button_frame,
            text="Add College",
            command=self.add_college,
            style="primary.TButton",
            width=15
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))

        self.update_button = ttk.Button(
            button_frame,
            text="Update College",
            command=self.update_college,
            style="info.TButton",
            width=15,
            state="disabled"
        )
        self.update_button.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_button = ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            width=15
        )
        self.clear_button.pack(side=tk.LEFT)

    def create_college_list(self):
        """Create the area displaying the list of colleges."""
        self.list_frame = ttk.LabelFrame(
            self.main_container,
            text="Existing Colleges",
            padding="20"
        )
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        self.scrolled_frame = ScrolledFrame(self.list_frame, autohide=True)
        self.scrolled_frame.pack(fill=tk.BOTH, expand=True)

    def get_exams(self):
        """Get list of exams from database."""
        try:
            conn = sqlite3.connect('career_counseling.db')
            cursor = conn.cursor()
            cursor.execute("SELECT ExamName FROM Exams ORDER BY ExamName")
            exams = [row[0] for row in cursor.fetchall()]
            conn.close()
            return exams
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading exams: {e}")
            return []

    def load_colleges(self):
        """Load and display existing colleges."""
        for widget in self.scrolled_frame.winfo_children():
            widget.destroy()

        try:
            conn = sqlite3.connect('career_counseling.db')
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    c.CollegeID,
                    c.CollegeName,
                    c.Location,
                    c.Field,
                    c.TuitionFee
                FROM Colleges c
                ORDER BY c.CollegeName
            """)

            colleges = cursor.fetchall()
            conn.close()

            for college in colleges:
                self.create_college_card(college)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading colleges: {e}")

    def create_college_card(self, college_data):
        """Create a display card for a college."""
        college_id, name, location, field, fee = college_data

        card = ttk.Frame(self.scrolled_frame, style="Card.TFrame")
        card.pack(fill=tk.X, pady=5, padx=5)

        # College details
        details_frame = ttk.Frame(card)
        details_frame.pack(fill=tk.X, padx=10, pady=10)

        name_label = ttk.Label(
            details_frame,
            text=name,
            font=("Helvetica", 12, "bold")
        )
        name_label.pack(anchor=tk.W)

        info_text = f"Location: {location} | Field: {field} | Tuition Fee: ₹{fee:,.2f}"
        info_label = ttk.Label(details_frame, text=info_text)
        info_label.pack(anchor=tk.W)

        # Buttons
        button_frame = ttk.Frame(details_frame)
        button_frame.pack(anchor=tk.W, pady=(5, 0))

        edit_button = ttk.Button(
            button_frame,
            text="Edit",
            command=lambda c=college_data: self.load_college_for_edit(c),
            style="info.TButton",
            width=10
        )
        edit_button.pack(side=tk.LEFT, padx=(0, 5))

        delete_button = ttk.Button(
            button_frame,
            text="Delete",
            command=lambda cid=college_id: self.delete_college(cid),
            style="danger.TButton",
            width=10
        )
        delete_button.pack(side=tk.LEFT)

        ttk.Separator(self.scrolled_frame).pack(fill=tk.X, pady=5)

    def load_college_for_edit(self, college_data):
        """Load college data into the form for editing."""
        college_id, name, location, field, fee = college_data

        self.current_college_id = college_id
        self.name_var.set(name)
        self.location_var.set(location)
        self.field_var.set(field)
        self.fee_var.set(str(fee))

        # Load cutoff scores
        try:
            conn = sqlite3.connect('career_counseling.db')
            cursor = conn.cursor()

            cursor.execute("""
                SELECT e.ExamName, ct.Category, ct.CutoffScore
                FROM Cutoffs ct
                JOIN Exams e ON ct.ExamID = e.ExamID
                WHERE ct.CollegeID = ?
            """, (college_id,))

            cutoffs = cursor.fetchall()
            conn.close()

            if cutoffs:
                self.exam_var.set(cutoffs[0][0])
                for exam_name, category, score in cutoffs:
                    if category in self.cutoff_vars:
                        self.cutoff_vars[category].set(str(score))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading cutoff scores: {e}")

        self.add_button.configure(state="disabled")
        self.update_button.configure(state="normal")

    def clear_form(self):
        """Clear all form fields."""
        self.current_college_id = None
        self.name_var.set("")
        self.location_var.set("")
        self.field_var.set("Engineering")
        self.fee_var.set("")
        self.exam_var.set("")

        for var in self.cutoff_vars.values():
            var.set("")

        self.add_button.configure(state="normal")
        self.update_button.configure(state="disabled")

    def add_college(self):
        """Add a new college to the database."""
        try:
            # Validate inputs
            if not all([self.name_var.get(), self.location_var.get(),
                        self.field_var.get(), self.fee_var.get()]):
                messagebox.showerror("Input Error", "Please fill all college details.")
                return

            fee = float(self.fee_var.get())

            conn = sqlite3.connect('career_counseling.db')
            cursor = conn.cursor()

            # Insert college
            cursor.execute("""
                INSERT INTO Colleges (CollegeName, Location, Field, TuitionFee)
                VALUES (?, ?, ?, ?)
            """, (self.name_var.get(), self.location_var.get(),
                  self.field_var.get(), fee))

            college_id = cursor.lastrowid

            # Insert cutoff scores
            if self.exam_var.get():
                cursor.execute("SELECT ExamID FROM Exams WHERE ExamName = ?",
                            (self.exam_var.get(),))
                exam_id = cursor.fetchone()[0]

                for category, var in self.cutoff_vars.items():
                    if var.get():
                        cursor.execute("""
                            INSERT INTO Cutoffs (CollegeID, ExamID, Category, CutoffScore)
                            VALUES (?, ?, ?, ?)
                        """, (college_id, exam_id, category, float(var.get())))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "College added successfully!")
            self.clear_form()
            self.load_colleges()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for fee and cutoff scores.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding college: {e}")

    def update_college(self):
        """Update an existing college in the database."""
        try:
            if not self.current_college_id:
                return

                # Validate inputs
            if not all([self.name_var.get(), self.location_var.get(),
                        self.field_var.get(), self.fee_var.get()]):
                messagebox.showerror("Input Error", "Please fill all college details.")
                return

            fee = float(self.fee_var.get())

            conn = sqlite3.connect('career_counseling.db')
            cursor = conn.cursor()

                # Update college
            cursor.execute("""
                UPDATE Colleges 
            SET CollegeName = ?, Location = ?, Field = ?, TuitionFee = ?
                    WHERE CollegeID = ?
            """, (self.name_var.get(), self.location_var.get(),
                    self.field_var.get(), fee, self.current_college_id))

            # Update cutoff scores
            if self.exam_var.get():
                # Get exam ID
                cursor.execute("SELECT ExamID FROM Exams WHERE ExamName = ?",
                                (self.exam_var.get(),))
                exam_id = cursor.fetchone()[0]

                # Delete existing cutoff scores
                cursor.execute("""
                    DELETE FROM Cutoffs 
                    WHERE CollegeID = ? AND ExamID = ?
                """, (self.current_college_id, exam_id))

                # Insert new cutoff scores
                for category, var in self.cutoff_vars.items():
                    if var.get():
                        cursor.execute("""
                            INSERT INTO Cutoffs (CollegeID, ExamID, Category, CutoffScore)
                            VALUES (?, ?, ?, ?)
                        """, (self.current_college_id, exam_id, category, float(var.get())))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "College updated successfully!")
            self.clear_form()
            self.load_colleges()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for fee and cutoff scores.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error updating college: {e}")

    def delete_college(self, college_id):
        """Delete a college from the database."""
        if not messagebox.askyesno("Confirm Delete",
                                    "Are you sure you want to delete this college?"):
            return

        try:
            conn = sqlite3.connect('career_counseling.db')
            cursor = conn.cursor()

            # Delete cutoff scores first (foreign key constraint)
            cursor.execute("DELETE FROM Cutoffs WHERE CollegeID = ?", (college_id,))

            # Delete college
            cursor.execute("DELETE FROM Colleges WHERE CollegeID = ?", (college_id,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "College deleted successfully!")
            self.load_colleges()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting college: {e}")

    def run(self):
        """Start the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = CollegeManagerGUI()
    app.run()