import sqlite3
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class College:
    name: str
    location: str
    cutoff_score: float
    field: str
    tuition_fee: float

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Initialize the database with required tables and sample data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS Exams (
                ExamID INTEGER PRIMARY KEY AUTOINCREMENT,
                ExamName TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Colleges (
                CollegeID INTEGER PRIMARY KEY AUTOINCREMENT,
                CollegeName TEXT NOT NULL,
                Location TEXT NOT NULL,
                Field TEXT NOT NULL,
                TuitionFee REAL NOT NULL,
                UNIQUE(CollegeName, Location)
            );

            CREATE TABLE IF NOT EXISTS Cutoffs (
                CollegeID INTEGER,
                ExamID INTEGER,
                Category TEXT NOT NULL,
                CutoffScore REAL NOT NULL,
                FOREIGN KEY (CollegeID) REFERENCES Colleges(CollegeID),
                FOREIGN KEY (ExamID) REFERENCES Exams(ExamID),
                UNIQUE(CollegeID, ExamID, Category)
            );
        """)
        cursor.execute("SELECT COUNT(*) FROM Exams")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                    INSERT INTO Exams (ExamName) VALUES 
                        ('JEE Main'),
                        ('JEE Advanced'),
                        ('NEET'),
                        ('BITSAT');""")

        conn.commit()
        conn.close()

    def get_exam_types(self) -> List[str]:
        """Retrieve all exam types from database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT ExamName FROM Exams ORDER BY ExamName")
            exams = [row[0] for row in cursor.fetchall()]
            conn.close()
            return exams
        except sqlite3.Error as e:
            raise Exception(f"Error loading exam types: {e}")

    def search_colleges(self, exam_name: str, field: str, category: str,
            score: float, budget: Optional[float] = None) -> List[College]:
        """Search for colleges based on given criteria."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = """
                SELECT 
                    c.CollegeName,
                    c.Location,
                    ct.CutoffScore,
                    c.Field,
                    c.TuitionFee
                FROM Colleges c
                JOIN Cutoffs ct ON c.CollegeID = ct.CollegeID
                JOIN Exams e ON ct.ExamID = e.ExamID
                WHERE e.ExamName = ?
                AND c.Field = ?
                AND ct.Category = ?
                AND ct.CutoffScore <= ?
            """
            params = [exam_name, field, category, score]

            if budget:
                query += " AND c.TuitionFee <= ?"
                params.append(budget)

            query += " ORDER BY ct.CutoffScore DESC"

            cursor.execute(query, params)
            results = cursor.fetchall()

            colleges = [
                College(
                    name=row[0],
                    location=row[1],
                    cutoff_score=row[2],
                    field=row[3],
                    tuition_fee=row[4]
                )
                for row in results
            ]

            conn.close()
            return colleges

        except sqlite3.Error as e:
            raise Exception(f"Error searching colleges: {e}")


