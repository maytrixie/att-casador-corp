# ATT Casador Corp - Inventory Management System

A comprehensive inventory management system with sales tracking, forecasting, and analytics capabilities.

## Features

- User Authentication and Authorization
- Inventory Management
- Sales Tracking
- Data Analytics and Visualization
- Sales Forecasting
- Customer Management
- Order Processing
- Delivery Tracking

## Tech Stack

- Python 3.9
- Flask
- MySQL
- SQLAlchemy
- Pandas
- Scikit-learn
- Statsmodels
- Bootstrap
- Chart.js

## Setup Instructions

1. Clone the repository:
```bash
git clone [your-repository-url]
cd att_casador_corp
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with the following variables:
```
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=att_db
SECRET_KEY=your_secret_key
```

5. Initialize the database:
```bash
python create_db.py
```

6. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Database Schema

The system uses the following main tables:
- User
- Product
- Customer
- Sales
- Inventory
- Orders
- Location
- Delivery
- Forecast

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 