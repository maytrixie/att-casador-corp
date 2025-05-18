import pymysql
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Database connection
conn = pymysql.connect(
    host='localhost', user='root', password='', db='att_db', cursorclass=pymysql.cursors.DictCursor
)

# Load sales data
query = """
    SELECT DATE_FORMAT(sale_date, '%Y-%m') AS month, SUM(quantity_sold) AS sales
    FROM Sales
    GROUP BY month
    ORDER BY month
"""
df = pd.read_sql(query, conn)
conn.close()

df['month_num'] = pd.to_datetime(df['month']).dt.month
# Label: 1 if sales above median, else 0
median_sales = df['sales'].median()
df['label'] = (df['sales'] > median_sales).astype(int)

# Features: month number, previous month's sales
# Shift sales to get previous month's sales as a feature
df['prev_sales'] = df['sales'].shift(1).fillna(df['sales'].mean())
X = df[['month_num', 'prev_sales']]
y = df['label']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

models = {
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Neural Network': MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=1000, random_state=42)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    print(f"{name}: Accuracy={acc:.2f}, Precision={prec:.2f}, Recall={rec:.2f}, F1={f1:.2f}") 