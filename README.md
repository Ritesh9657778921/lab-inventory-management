# Lab Inventory Management System

This project is a Lab Inventory Management System built using Python with Flask, HTML/CSS, and SQLite/MySQL. It provides a web-based interface for managing chemical stocks, tracking expiry dates, monitoring hazard levels, and managing storage locations. The system also includes alerts for low stock and expired chemicals.

## Features

- Manage chemical inventory with details such as name, quantity, unit, expiry date, hazard level, and storage location.
- Add, edit, and delete chemical entries.
- View a comprehensive list of all chemicals in the inventory.
- Dashboard displaying total chemicals, low stock items, and expired chemicals.
- Alerts for low stock and expired chemicals.
- Login / registration with admin and user roles.
- Role-based access: admins can add, edit, delete, and export inventory.
- Inventory export to CSV for reports.
- User-friendly interface with forms for adding and editing chemicals.

## Technologies Used

- Python
- Flask
- SQLAlchemy (for database management)
- SQLite or MySQL (for data storage)
- HTML/CSS (for front-end)
- JavaScript (for client-side functionality)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd lab-inventory-management
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Configure the database in `instance/config.py`:
   ```python
   SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'  # or your MySQL URI
   SECRET_KEY = 'your_secret_key'
   ```

5. Run the application:
   ```
   python run.py
   ```

6. Open your web browser and go to `http://127.0.0.1:5000`.

7. Register a new account or log in with an existing one. Admin users can manage chemicals and export inventory reports.

## Usage

- Navigate to the dashboard to view an overview of the inventory.
- Use the "Add Chemical" form to add new chemicals to the inventory.
- Edit existing chemicals or delete them as needed.
- Check the alerts page for any low stock or expired chemicals.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.