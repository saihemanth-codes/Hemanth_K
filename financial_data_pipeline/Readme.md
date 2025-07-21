# 💸 Financial Data Pipeline Project

A complete data pipeline designed to simulate real-time financial transaction processing, transformation, and storage using modern data engineering tools and practices.

This project is part of the `Hemanth_K` portfolio repository and showcases integration of **Kafka**, **Apache Airflow**, **SQLite**, **DBT**, and **Python**.

---

## 📂 Dataset Source

- **Website:** [https://relational-data.org/dataset/Financial](https://relational-data.org/dataset/Financial)
- **Format:** CSV
- **File Used:** `trans.csv`
- **Description:** Simulated financial transactions across multiple accounts and customers.

---

## 🧰 Tech Stack

| Tool             | Purpose                                   |
|------------------|-------------------------------------------|
| **Python**       | Scripting and data processing             |
| **Apache Kafka** | Real-time data streaming (ingesting CSV)  |
| **Apache Airflow** | Workflow orchestration & automation     |
| **SQLite**       | Lightweight local storage (data lakehouse)|
| **DBT (Data Build Tool)** | Data modeling (dim/fact tables) |
| **Docker (optional)** | Containerized deployment             |

---

## 📈 Project Architecture

```
                     ┌───────────────────┐
                     │    trans.csv      │
                     └────────┬──────────┘
                              │
                         [Kafka Producer]
                              │
                     ┌────────▼────────┐
                     │    Kafka Topic  │
                     └────────┬────────┘
                              │
                 ┌────────────▼────────────┐
                 │ Airflow DAG - Consumer  │
                 │  (data transformation)  │
                 └────────────┬────────────┘
                              │
                        ┌─────▼─────┐
                        │  SQLite   │
                        └─────┬─────┘
                              │
                        ┌────▼────┐
                        │  DBT    │
                        │  Models │
                        └─────────┘
```

---

## ⚙️ How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/saihemanth-codes/Hemanth_K.git
cd Hemanth_K/financial_data_pipeline
```

### 2. Prepare the Environment

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Optional: Set up a virtual environment using `venv` or `conda`

---

### 3. Start Kafka and Zookeeper

You can use Docker Compose or a local install:

```bash
# If using Docker
docker-compose up -d
```

Kafka will stream data from `trans.csv` line-by-line to simulate real-time ingestion.

---

### 4. Run Airflow DAG

- Start Airflow:

```bash
airflow db init
airflow webserver -p 8080
airflow scheduler
```

- Visit: [http://localhost:8080](http://localhost:8080)
- Login:
  - **Username:** `airflow`
  - **Password:** `airflow`
- Enable and trigger the DAG (`transaction_pipeline_dag`)

---

### 5. Run DBT Models

Once data is loaded into SQLite:

```bash
cd dbt/
dbt run
```

DBT will generate cleaned and modeled tables like:

- `dim_customer`
- `dim_account`
- `fact_transactions`

---

## 🗂️ Example Schema

### 🔹 `dim_customer`

| customer_id | name        | region     |
|-------------|-------------|------------|
| 101         | John Smith  | East       |
| 102         | Jane Doe    | West       |

### 🔹 `fact_transactions`

| trans_id | customer_id | amount | timestamp           |
|----------|-------------|--------|---------------------|
| 9001     | 101         | 250.75 | 2023-01-10 08:15:00 |

---

## 💡 Learning Objectives

- Build **real-time pipelines** using Apache Kafka
- Orchestrate ETL jobs with **Apache Airflow**
- Model data using **dimensional schemas with DBT**
- Handle local lightweight storage using **SQLite**
- Apply clean data engineering practices for portfolio use

---

## 🚀 Future Enhancements

- Add monitoring with Prometheus + Grafana
- Switch to PostgreSQL or Snowflake as the data warehouse
- Deploy everything using Docker Compose or Kubernetes
- Add a Streamlit dashboard or Power BI visualization

---

## 🙌 Credits

- Dataset from [Relational Data](https://relational-data.org/)
- Inspired by real-world financial data architecture
- Developed by **Hemanth Korrapati**

---

## 📄 License

This project is licensed under the MIT License — feel free to use and adapt!

