import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

query = """
SELECT
    c.customer_id,
    COUNT(DISTINCT f.order_id) AS frequency,
    SUM(f.price) AS monetary
FROM fact_order_items f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_id;
"""

df = pd.read_sql(query, engine)
print(df.head())
print(f"Total customers: {len(df)}")


features = df[['frequency', 'monetary']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(scaled_features)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['frequency'], df['monetary'], c=df['cluster'], cmap='viridis', alpha=0.6)
plt.xlabel('Order Frequency')
plt.ylabel('Total Spend (Monetary)')
plt.title('Customer Segments (KMeans Clustering)')
plt.colorbar(scatter, label='Cluster')
plt.savefig('customer_clusters.png')
plt.show()

print("\nCluster summary:")
print(df.groupby('cluster')[['frequency', 'monetary']].mean())