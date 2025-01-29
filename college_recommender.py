import logging
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
        self.root.minsize(800, 600)

        self.db_manager = DatabaseManager('career_counseling.db')

        # Add state variables for form validation
        self.form_valid = False
        self.validation_errors = []

        # Add state variable for storing current search results
        self.current_results = []

        self.main_container = ttk.Frame(self.root, padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.create_header()
        self.create_input_form()
        self.create_search_bar()  # New search bar
        self.create_results_area()
        self.create_status_bar()
        self.populate_exam_types()

        # Bind validation to form inputs
        self.score_var.trace_add('write', self.validate_form)
        self.budget_var.trace_add('write', self.validate_form)

        # Add keyboard shortcuts
        self.root.bind('<Return>', lambda e: self.search_colleges())
        self.root.bind('<Escape>', lambda e: self.clear_form())
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # Initialize search button in disabled state
        self.search_button.configure(state="disabled")

    def create_header(self):
        """Create the application header with improved styling."""
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
        """Create the input form section with improved layout and validation."""
        self.form_frame = ttk.LabelFrame(
            self.main_container,
            text="Enter Your Details",
            padding="20"
        )
        self.form_frame.pack(fill=tk.X, pady=(0, 20))

        # Create grid layout for better alignment
        current_row = 0

        # Exam selection
        ttk.Label(self.form_frame, text="Select Exam:").grid(row=current_row, column=0, sticky='w', pady=5)
        self.exam_var = tk.StringVar()
        self.exam_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.exam_var,
            state="readonly",
            width=30
        )
        self.exam_combobox.grid(row=current_row, column=1, sticky='w', padx=(10, 0), pady=5)
        current_row += 1

        # Score entry with validation
        ttk.Label(self.form_frame, text="Your Score:").grid(row=current_row, column=0, sticky='w', pady=5)
        self.score_var = tk.StringVar()
        self.score_entry = ttk.Entry(
            self.form_frame,
            textvariable=self.score_var,
            width=32
        )
        self.score_entry.grid(row=current_row, column=1, sticky='w', padx=(10, 0), pady=5)
        current_row += 1

        # Category selection
        ttk.Label(self.form_frame, text="Category:").grid(row=current_row, column=0, sticky='w', pady=5)
        self.category_var = tk.StringVar(value="General")
        categories = ["General", "OBC", "SC", "ST"]
        self.category_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=30
        )
        self.category_combobox.grid(row=current_row, column=1, sticky='w', padx=(10, 0), pady=5)
        current_row += 1

        # Field selection
        ttk.Label(self.form_frame, text="Field:").grid(row=current_row, column=0, sticky='w', pady=5)
        self.field_var = tk.StringVar(value="Engineering")
        fields = ["Engineering", "Medicine", "Architecture"]
        self.field_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.field_var,
            values=fields,
            state="readonly",
            width=30
        )
        self.field_combobox.grid(row=current_row, column=1, sticky='w', padx=(10, 0), pady=5)
        current_row += 1

        # Budget entry with validation
        ttk.Label(self.form_frame, text="Max Budget (₹):").grid(row=current_row, column=0, sticky='w', pady=5)
        self.budget_var = tk.StringVar()
        self.budget_entry = ttk.Entry(
            self.form_frame,
            textvariable=self.budget_var,
            width=32
        )
        self.budget_entry.grid(row=current_row, column=1, sticky='w', padx=(10, 0), pady=5)
        current_row += 1

        # Buttons frame
        button_frame = ttk.Frame(self.form_frame)
        button_frame.grid(row=current_row, column=0, columnspan=2, pady=(20, 0))

        self.search_button = ttk.Button(
            button_frame,
            text="Find Colleges",
            command=lambda: self.search_colleges(),  # Wrap in lambda
            style="primary",
            width=20
        )
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            style="secondary",
            width=20
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Add form validation bindings
        self.score_var.trace_add('write', self.validate_form)
        self.budget_var.trace_add('write', self.validate_form)
        self.exam_var.trace_add('write', self.validate_form)

    def create_search_bar(self):
        """Create a search bar for filtering college results."""
        search_frame = ttk.Frame(self.main_container)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        # Search icon and entry field in a single frame
        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(fill=tk.X)

        # Search icon (you can replace this with an actual icon if available)
        search_icon = ttk.Label(search_input_frame, text="🔍")
        search_icon.pack(side=tk.LEFT, padx=(0, 5))

        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            search_input_frame,
            textvariable=self.search_var,
            width=50,
            style="primary"
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Add placeholder text
        self.search_entry.insert(0, "Search colleges by name or location...")
        self.search_entry.bind('<FocusIn>', self._on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_search_focus_out)

        # Bind search functionality
        self.search_var.trace_add('write', self._on_search_change)

    def _on_search_focus_in(self, event):
        """Handle search entry focus in event."""
        if self.search_entry.get() == "Search colleges by name or location...":
            self.search_entry.delete(0, tk.END)

    def _on_search_focus_out(self, event):
        """Handle search entry focus out event."""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search colleges by name or location...")

    def _on_search_change(self, *args):
        """Filter college results based on search text."""
        search_text = self.search_var.get().lower()

        # Skip filtering if it's the placeholder text
        if search_text == "search colleges by name or location...":
            return

        # Clear existing results
        self.clear_results()

        if not self.current_results:
            return

        # Filter and display matching colleges
        for college in self.current_results:
            if (search_text in college.name.lower() or
                    search_text in college.location.lower()):
                self.create_college_card(college)

    def search_colleges(self, event=None):
        self.logger.debug("Search colleges function called")

        # Validate form again just to be safe
        if not self.validate_form():
            self.logger.debug("Form validation failed")
            messagebox.showerror("Input Error", "\n".join(self.validation_errors))
            return

        self.status_var.set("Searching...")
        self.root.update_idletasks()
        self.clear_results()

        try:
            # Get form values
            exam_name = self.exam_var.get()
            field = self.field_var.get()
            category = self.category_var.get()
            score = float(self.score_var.get())
            budget = float(self.budget_var.get()) if self.budget_var.get() else None

            self.logger.debug(f"""Search parameters:
                Exam: {exam_name}
                Field: {field}
                Category: {category}
                Score: {score}
                Budget: {budget}""")

            # Call database search
            colleges = self.db_manager.search_colleges(
                exam_name=exam_name,
                field=field,
                category=category,
                score=score,
                budget=budget
            )

            self.logger.debug(f"Found {len(colleges) if colleges else 0} colleges")

            if not colleges:
                no_results_label = ttk.Label(
                    self.scrolled_frame,
                    text="No colleges found matching your criteria.\nTry adjusting your score or budget criteria.",
                    font=("Helvetica", 12),
                    justify="center"
                )
                no_results_label.pack(pady=20)
                self.status_var.set("No colleges found")
                self.current_results = []  # Clear current results
                return

            # Sort colleges by cutoff score in descending order
            colleges.sort(key=lambda x: x.cutoff_score, reverse=True)

            # Store current results for search filtering
            self.current_results = [c for c in colleges if score >= c.cutoff_score]

            # Display results
            for college in self.current_results:
                self.create_college_card(college)
                self.logger.debug(f"Created card for college: {college.name}")

            self.status_var.set(f"Found {len(self.current_results)} matching colleges")

        except Exception as e:
            self.logger.error(f"Error during college search: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"An error occurred while searching: {str(e)}")
            self.status_var.set("Search failed")
            self.current_results = []  # Clear current results


    def create_results_area(self):
        """Create the results display area with improved styling."""
        self.results_frame = ttk.LabelFrame(
            self.main_container,
            text="Recommended Colleges",
            padding="20"
        )
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        self.scrolled_frame = ScrolledFrame(self.results_frame, autohide=True)
        self.scrolled_frame.pack(fill=tk.BOTH, expand=True)

    def create_status_bar(self):
        """Create a status bar for displaying messages."""
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(10, 5)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def populate_exam_types(self):
        """Populate exam types from database."""
        try:
            exams = self.db_manager.get_exam_types()
            self.exam_combobox['values'] = exams
            if exams:
                self.exam_combobox.set(exams[0])
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def validate_form(self, *args) -> bool:
        """Validate form inputs and update UI accordingly."""
        self.validation_errors = []

        # Validate exam selection
        if not self.exam_var.get():
            self.validation_errors.append("Please select an exam")

        # Validate score
        try:
            if not self.score_var.get():
                self.validation_errors.append("Score is required")
            else:
                score = float(self.score_var.get())
                # Remove the upper limit check since higher scores should be valid
                if score < 0:
                    self.validation_errors.append("Score must be greater than 0")
        except ValueError:
            self.validation_errors.append("Score must be a valid number")

        # Validate budget (optional)
        if self.budget_var.get():
            try:
                budget = float(self.budget_var.get())
                if budget < 0:
                    self.validation_errors.append("Budget cannot be negative")
            except ValueError:
                self.validation_errors.append("Budget must be a valid number")

        # Update UI based on validation
        self.form_valid = len(self.validation_errors) == 0

        # Enable/disable search button
        if self.form_valid:
            self.search_button.configure(state="normal")
            self.status_var.set("Ready to search")
        else:
            self.search_button.configure(state="disabled")
            self.status_var.set(self.validation_errors[0])

        self.logger.debug(f"Form validation: {'Valid' if self.form_valid else 'Invalid'}")
        if self.validation_errors:
            self.logger.debug(f"Validation errors: {self.validation_errors}")

        return self.form_valid


    def clear_form(self):
        """Clear all form inputs."""
        self.score_var.set("")
        self.budget_var.set("")
        self.category_var.set("General")
        self.field_var.set("Engineering")
        self.search_var.set("")  # Clear search field
        self._on_search_focus_out(None)  # Restore placeholder
        self.status_var.set("Form cleared")
        self.clear_results()
        self.current_results = []

    def clear_results(self):
            """Clear the results area."""
            for widget in self.scrolled_frame.winfo_children():
                widget.destroy()
    def create_college_card(self, college: College):
        """Create a card-style display for a college with improved styling."""
        card = ttk.Frame(
            self.scrolled_frame,
            style="Card.TFrame"
        )
        card.pack(fill=tk.X, pady=5, padx=5)

        # College name
        name_frame = ttk.Frame(card)
        name_frame.pack(fill=tk.X, pady=(10, 5), padx=10)

        name_label = ttk.Label(
            name_frame,
            text=college.name,
            font=("Helvetica", 14, "bold")
        )
        name_label.pack(side=tk.LEFT)

        # Details section with grid layout
        details_frame = ttk.Frame(card)
        details_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Using grid for better alignment
        current_row = 0

        # Location
        ttk.Label(
            details_frame,
            text="Location:",
            font=("Helvetica", 10, "bold")
        ).grid(row=current_row, column=0, sticky='w')
        ttk.Label(
            details_frame,
            text=college.location
        ).grid(row=current_row, column=1, sticky='w', padx=(5, 20))

        # Field
        ttk.Label(
            details_frame,
            text="Field:",
            font=("Helvetica", 10, "bold")
        ).grid(row=current_row, column=2, sticky='w')
        ttk.Label(
            details_frame,
            text=college.field
        ).grid(row=current_row, column=3, sticky='w', padx=(5, 0))
        current_row += 1

        # Cutoff Score
        ttk.Label(
            details_frame,
            text="Cutoff Score:",
            font=("Helvetica", 10, "bold")
        ).grid(row=current_row, column=0, sticky='w')
        ttk.Label(
            details_frame,
            text=f"{college.cutoff_score:.2f}"
        ).grid(row=current_row, column=1, sticky='w', padx=(5, 20))

        # Tuition Fee
        ttk.Label(
            details_frame,
            text="Annual Tuition Fee:",
            font=("Helvetica", 10, "bold")
        ).grid(row=current_row, column=2, sticky='w')
        ttk.Label(
            details_frame,
            text=f"₹{college.tuition_fee:,.2f}"
        ).grid(row=current_row, column=3, sticky='w', padx=(5, 0))

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