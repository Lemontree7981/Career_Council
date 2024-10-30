# Career Council 🎓

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![SQLite](https://img.shields.io/badge/sqlite-3-green.svg)](https://www.sqlite.org/index.html)

> Helping students find their best college options through data-driven recommendations 🚀

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Database Structure](#database-structure)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Career Council is a powerful career counseling application designed to simplify the college recommendation process for high school students. Built with Python and SQLite3, it provides personalized college suggestions based on student test scores, making career counseling more accessible and tailored to individual profiles.

## ✨ Features

- **Smart Recommendations** - Get college suggestions based on test score cut-off values
- **Reliable Storage** - Secure data management using SQLite3
- **User-Friendly** - Clean and intuitive interface for seamless experience
- **Scalable Architecture** - Easily expandable to include more features and data points

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Lemontree7981/Career_Council.git
   cd Career_Council
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application:
   ```bash
   python launcher.py
   ```

## 💡 Usage

1. Launch the application
2. Enter your test scores when prompted
3. Review the personalized college recommendations
4. Make informed decisions about your college applications

## 🗄️ Database Structure

The application uses SQLite3 with the following main tables:

| Table | Description |
|-------|-------------|
| Colleges | Stores college names and cut-off scores |
| Students | Contains student IDs, names, and test scores |
| Recommendations | Maps student IDs to recommended colleges |

## 🔮 Future Enhancements

- [ ] Enhanced filtering by location, ranking, and cost
- [ ] Student score history tracking
- [ ] Annual college cut-off score updates
- [ ] Mobile application development
- [ ] Integration with college application platforms

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <b>Ready to transform your college search? Start using Career Council today!</b>
</div>
