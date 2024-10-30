import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from database_operations import DatabaseManager, College
import sys
class CollegeRecommenderGUI:
    def __init__(self):
        self.root = ttk.Window(themename="cosmo")
        self.root.title("College Recommender System")
        self.root.geometry("900x700")

        self.db_manager = DatabaseManager('career_counseling.db')

        self.main_container = ttk.Frame(self.root, padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.create_header()
        self.create_input_form()
        self.create_results_area()
        self.populate_exam_types()

    def create_header(self):
        """Create the application header."""
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title = ttk.Label(
            header_frame,
            text="College Recommender System",
            font=("Helvetica", 24, "bold")
        )
        title.pack()

        subtitle = ttk.Label(
            header_frame,
            text="Find the best colleges based on your exam scores",
            font=("Helvetica", 12)
        )
        subtitle.pack()

    def create_input_form(self):
        """Create the input form section."""
        self.form_frame = ttk.LabelFrame(
            self.main_container,
            text="Enter Your Details",
            padding="20"
        )
        self.form_frame.pack(fill=tk.X, pady=(0, 20))

        exam_frame = ttk.Frame(self.form_frame)
        exam_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(exam_frame, text="Select Exam:").pack(side=tk.LEFT)
        self.exam_var = tk.StringVar()
        self.exam_combobox = ttk.Combobox(
            exam_frame,
            textvariable=self.exam_var,
            state="readonly",
            width=30
        )
        self.exam_combobox.pack(side=tk.LEFT, padx=(10, 0))

        score_frame = ttk.Frame(self.form_frame)
        score_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(score_frame, text="Your Score:").pack(side=tk.LEFT)
        self.score_var = tk.StringVar()
        score_entry = ttk.Entry(
            score_frame,
            textvariable=self.score_var,
            width=32
        )
        score_entry.pack(side=tk.LEFT, padx=(10, 0))

        category_frame = ttk.Frame(self.form_frame)
        category_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(category_frame, text="Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar(value="General")
        categories = ["General", "OBC", "SC", "ST"]
        self.category_combobox = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=30
        )
        self.category_combobox.pack(side=tk.LEFT, padx=(10, 0))

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
            width=30
        )
        self.field_combobox.pack(side=tk.LEFT, padx=(10, 0))

        budget_frame = ttk.Frame(self.form_frame)
        budget_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(budget_frame, text="Max Budget (₹):").pack(side=tk.LEFT)
        self.budget_var = tk.StringVar()
        budget_entry = ttk.Entry(
            budget_frame,
            textvariable=self.budget_var,
            width=32
        )
        budget_entry.pack(side=tk.LEFT, padx=(10, 0))

        self.search_button = ttk.Button(
            self.form_frame,
            text="Find Colleges",
            command=self.search_colleges,
            style="primary.TButton",
            width=20
        )
        self.search_button.pack(pady=(10, 0))

    def create_results_area(self):
        """Create the results display area."""
        self.results_frame = ttk.LabelFrame(
            self.main_container,
            text="Recommended Colleges",
            padding="20"
        )
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        self.scrolled_frame = ScrolledFrame(self.results_frame, autohide=True)
        self.scrolled_frame.pack(fill=tk.BOTH, expand=True)

    def populate_exam_types(self):
        """Populate exam types from database."""
        try:
            exams = self.db_manager.get_exam_types()
            self.exam_combobox['values'] = exams
            if exams:
                self.exam_combobox.set(exams[0])
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def search_colleges(self):
        """Search for colleges based on user input."""
        try:
            score = float(self.score_var.get())
            budget = float(self.budget_var.get()) if self.budget_var.get() else None
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for score and budget.")
            return

        for widget in self.scrolled_frame.winfo_children():
            widget.destroy()

        try:
            colleges = self.db_manager.search_colleges(
                exam_name=self.exam_var.get(),
                field=self.field_var.get(),
                category=self.category_var.get(),
                score=score,
                budget=budget
            )

            if not colleges:
                no_results_label = ttk.Label(
                    self.scrolled_frame,
                    text="No colleges found matching your criteria.",
                    font=("Helvetica", 12)
                )
                no_results_label.pack(pady=20)
                return

            for college in colleges:
                self.create_college_card(college)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def create_college_card(self, college: College):
        """Create a card-style display for a college."""
        card = ttk.Frame(self.scrolled_frame, style="Card.TFrame")
        card.pack(fill=tk.X, pady=5, padx=5)

        name_label = ttk.Label(
            card,
            text=college.name,
            font=("Helvetica", 14, "bold")
        )
        name_label.pack(anchor=tk.W, pady=(10, 5), padx=10)

        details_frame = ttk.Frame(card)
        details_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        location_frame = ttk.Frame(details_frame)
        location_frame.pack(fill=tk.X)
        ttk.Label(
            location_frame,
            text="Location:",
            font=("Helvetica", 10, "bold")
        ).pack(side=tk.LEFT)
        ttk.Label(
            location_frame,
            text=college.location
        ).pack(side=tk.LEFT, padx=(5, 0))

        field_frame = ttk.Frame(details_frame)
        field_frame.pack(fill=tk.X)
        ttk.Label(
            field_frame,
            text="Field:",
            font=("Helvetica", 10, "bold")
        ).pack(side=tk.LEFT)
        ttk.Label(
            field_frame,
            text=college.field
        ).pack(side=tk.LEFT, padx=(5, 0))

        cutoff_frame = ttk.Frame(details_frame)
        cutoff_frame.pack(fill=tk.X)
        ttk.Label(
            cutoff_frame,
            text="Cutoff Score:",
            font=("Helvetica", 10, "bold")
        ).pack(side=tk.LEFT)
        ttk.Label(
            cutoff_frame,
            text=f"{college.cutoff_score:.2f}"
        ).pack(side=tk.LEFT, padx=(5, 0))

        fee_frame = ttk.Frame(details_frame)
        fee_frame.pack(fill=tk.X)
        ttk.Label(
            fee_frame,
            text="Annual Tuition Fee:",
            font=("Helvetica", 10, "bold")
        ).pack(side=tk.LEFT)
        ttk.Label(
            fee_frame,
            text=f"₹{college.tuition_fee:,.2f}"
        ).pack(side=tk.LEFT, padx=(5, 0))

        ttk.Separator(self.scrolled_frame).pack(fill=tk.X, pady=5)


def main():
    if len(sys.argv) != 2:
        print("Access Denied: Please launch through the main app.")
        return
    token = sys.argv[1]
    app = CollegeRecommenderGUI()
    app.root.mainloop()


if __name__ == "__main__":
    main()