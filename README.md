<img width="1000" height="600" alt="cluster graph" src="https://github.com/user-attachments/assets/02238ce7-ba56-4a89-803e-e0e939acda65" /><img width="1979" height="1580" alt="star_schema_diagram" src="https://github.com/user-attachments/assets/efba8910-735e-4d3b-8c04-c09e346ddced" />

# Ecommerce-Data-Warehouse
# E-commerce Data Warehouse & Customer Segmentation

Raw CSVs → clean star schema → SQL analytics → customer segmentation ML. A hands-on data warehousing project built from the ground up for anyone who loves exploring how data actually works.

Built using the [Olist Brazilian E-commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (100k+ real orders).

## What this project covers

- *Dimensional modeling* — designing a star schema from scratch (fact + dimension tables)
- *ETL with SQL* — staging raw data, then transforming it into a clean, query-ready warehouse
- *SQL analytics* — extracting real business insights from the warehouse
- *Machine learning* — customer segmentation using KMeans clustering, with features pulled directly from the warehouse

## Architecture

Raw CSVs are loaded as-is into *staging tables* (no transformation, just a landing zone). SQL then transforms and loads that data into a *star schema* — one central fact table surrounded by dimension tables.


CSV files → staging tables → star schema (fact + dimension tables) → SQL analysis → ML features


## Star schema

The warehouse follows a classic Kimball-style star schema. fact_order_items sits at the center — one row per order item (the "grain") — with customer_key, product_key, and date_key linking out to the three dimension tables.

| Table | Type | Description |
|---|---|---|
| fact_order_items | Fact | One row per order item — price, freight cost, and foreign keys to each dimension |
| dim_customer | Dimension | Customer ID, city, state |
| dim_product | Dimension | Product ID, category |
| dim_date | Dimension | Date, year, month, day, weekday |

*Why one row per order item?* An order can contain multiple products, so modeling at the item level (rather than the order level) keeps the schema flexible — no cramming multiple products into one row, and revenue can be sliced by product, category, or order with simple aggregations.

(Schema diagram included in this repo — see /assets)

## ETL process

1. *Staging* — raw CSVs (orders, customers, order_items, products) loaded untouched into staging tables.
2. *Dimension load* — dim_customer, dim_product, and dim_date populated from staging, with DISTINCT used to avoid duplicates and Postgres auto-generating surrogate keys.
3. *Fact load* — fact_order_items populated by joining staging_order_items → staging_orders → each dimension table, resolving surrogate keys along the way.

Full SQL scripts are in /sql.

## SQL analysis

With the star schema in place, business questions become simple, fast queries instead of multi-join scans over raw flat data:

- Total revenue by customer state
- Top 10 product categories by revenue
- Monthly order volume trend
- Top customers by total spend

Queries are in /sql/analysis_queries.sql.

## Customer segmentation (ML)

Customer-level features — order frequency and total spend — were pulled directly from the warehouse via SQL, scaled, and clustered using *KMeans* (scikit-learn) to segment customers into behavioral groups.

*Note on this dataset:* Olist's customer base is dominated by one-time buyers — most customers place a single order, so "frequency" clusters heavily around 1, and the segmentation here separates mainly by *spend* (a handful of high-value single-purchase customers vs. the long tail of typical orders). This is a genuine, real-world characteristic of the dataset rather than a modeling artifact, and it's a useful reminder that repeat-purchase analysis needs a dataset with real repeat behavior to be meaningful.

(Cluster chart included in this repo — see /assets)

## Tech stack

- *PostgreSQL* — data warehouse
- *SQL* — DDL, staging, ETL, analytical queries (CTEs, joins, aggregations, window functions)
- *Python* — pandas, scikit-learn, matplotlib
- *Dimensional modeling* — Kimball-style star schema design

## Repo structure


├── sql/
│   ├── create_tables.sql          # star schema + staging table DDL
│   ├── load_staging_to_schema.sql # ETL: staging → star schema
│   └── analysis_queries.sql       # business insight queries
├── cluster_customers.py           # feature extraction + KMeans clustering
├── assets/
│   ├── star_schema_diagram.png
│   └── customer_clusters.png
└── README.md


## Key takeaway

The schema you design before touching your data matters more than any query you write after it. Getting the grain and the fact/dimension split right made every downstream query and every ML feature simpler to build.

## Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — 100k+ orders made between 2016-2018 across multiple marketplaces in Brazil.
