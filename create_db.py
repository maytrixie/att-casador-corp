import pymysql
import os
import shutil

# First, try to remove the database directory if it exists
db_path = os.path.join(os.getcwd(), 'att_db')
if os.path.exists(db_path):
    try:
        shutil.rmtree(db_path)
    except Exception as e:
        print(f"Warning: Could not remove database directory: {str(e)}")

# Create database connection without specifying database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cursor:
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS att_db")
        cursor.execute("USE att_db")
        
        # Create tables
        # Location table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Location (
            location_id INT AUTO_INCREMENT PRIMARY KEY,
            delivery_id INT,
            customer_id INT,
            latitude DECIMAL(10,6),
            longitude DECIMAL(10,6),
            time_stamp DATETIME
        )''')
        
        # Customer table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Customer (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            contact_number VARCHAR(20),
            email VARCHAR(100),
            location_id INT,
            FOREIGN KEY (location_id) REFERENCES Location(location_id)
        )''')
        
        # User table
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(50),
            username VARCHAR(10),
            password VARCHAR(50),
            role ENUM('admin','user'),
            email VARCHAR(50)
        )''')
        
        # Product table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(50),
            price DECIMAL(10,2),
            category VARCHAR(50)
        )''')
        
        # Sales table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Sales (
            sales_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            quantity_sold INT,
            sale_date DATE,
            total_amount DECIMAL(10,2),
            FOREIGN KEY (product_id) REFERENCES Product(product_id)
        )''')
        
        # Orders table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            order_date DATE,
            payment_status ENUM('paid','unpaid'),
            status ENUM('pending','completed','cancelled'),
            amount_paid DECIMAL(10,2),
            payment_date DATE,
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
        )''')
        
        # Order Details table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Order_Details (
            order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            product_id INT,
            quantity INT,
            price DECIMAL(10,2),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (product_id) REFERENCES Product(product_id)
        )''')
        
        # Forecast table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Forecast (
            forecast_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            forecast_date DATE,
            predicted_quantity DECIMAL(10,2),
            confidence_level DECIMAL(5,2),
            FOREIGN KEY (product_id) REFERENCES Product(product_id)
        )''')
        
        # Restock table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Restock (
            restock_id INT AUTO_INCREMENT PRIMARY KEY,
            quantity VARCHAR(100),
            restock_date DATE,
            product_id INT,
            FOREIGN KEY (product_id) REFERENCES Product(product_id)
        )''')
        
        # Inventory table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Inventory (
            inventory_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            quantity INT,
            stock_status VARCHAR(50),
            updated_at DATETIME,
            FOREIGN KEY (product_id) REFERENCES Product(product_id)
        )''')
        
        # Delivery table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Delivery (
            delivery_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            delivery_personnel_id INT,
            destination_address VARCHAR(255),
            status ENUM('pending','delivered','cancelled'),
            delivery_date DATE,
            FOREIGN KEY (product_id) REFERENCES Product(product_id)
        )''')
        
        # DeliveryTracking table
        cursor.execute('''CREATE TABLE IF NOT EXISTS DeliveryTracking (
            tracking_id INT AUTO_INCREMENT PRIMARY KEY,
            delivery_id INT,
            latitude DECIMAL(10,8),
            longitude DECIMAL(11,8),
            timestamp TIMESTAMP,
            FOREIGN KEY (delivery_id) REFERENCES Delivery(delivery_id)
        )''')
        
        # DeliveryRoutes table
        cursor.execute('''CREATE TABLE IF NOT EXISTS DeliveryRoutes (
            route_id INT AUTO_INCREMENT PRIMARY KEY,
            delivery_id INT,
            origin_location_id INT,
            destination_location_id INT,
            estimated_time TIME,
            FOREIGN KEY (delivery_id) REFERENCES Delivery(delivery_id)
        )''')
        
        # Activity Log table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Activity_Log (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            action VARCHAR(100),
            time_stamp DATETIME,
            FOREIGN KEY (user_id) REFERENCES user(user_id)
        )''')
        
        # Insert default admin user
        cursor.execute("""
            INSERT INTO user (username, password, email, role, full_name) 
            VALUES ('admin', 'admin123', 'admin@casador.com', 'admin', 'Admin User')
        """)
        
        conn.commit()
        print("Database and tables created successfully!")
        
except Exception as e:
    print(f"Error: {str(e)}")
    conn.rollback()
finally:
    conn.close() 