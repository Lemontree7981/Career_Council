Career Council--

Helping students find their best college options.

Table of Contents:

Overview
Features
Getting Started
Usage
Database Structure
Future Enhancements
Contributing
License
Overview



Career Council is a career counseling app that simplifies the college recommendation process for high school students.
It uses Python and SQLite3 to store college data and provides customized recommendations based on the student's test scores.
This project aims to make career counseling more accessible and tailored to individual student profiles.
Features
College Recommendations: Receive college suggestions based on test score cut-off values.
Database Storage: Easily stores and retrieves data using SQLite3.
User-Friendly Interface: Built with simplicity in mind, providing a straightforward experience for users.
Scalability: The app can be expanded to include more fields, data points, and customization options.

Getting Started
Clone the repository:

bash
Copy code
git clone https://github.com/Lemontree7981/Career_Council.git
cd Career_Council
Install Requirements:
Ensure you have Python installed (3.x is recommended).
Run the following to install any required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the App:
Start the app by running:

bash
Copy code
python main.py
Usage
Enter your test scores when prompted.
The app will analyze your scores and provide a list of suitable colleges based on their cut-off scores.
Review the recommendations to make informed decisions about your college applications.
Database Structure
The SQLite database contains the following main tables:

Colleges: Stores college names and cut-off scores.
Students: Stores student IDs, names, and test scores.
Recommendations: Links student IDs with recommended colleges.
Future Enhancements
Additional Filters: Sort colleges by location, ranking, and cost.
Score History: Track student score changes over time.
Custom Cut-off Updates: Allow administrators to update college cut-off scores annually.
Contributing
We welcome contributions! Please fork the repository, make your changes, and submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for more information.

