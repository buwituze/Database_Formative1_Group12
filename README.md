# Salary Records API

A fast and async REST API built with **FastAPI** and **MongoDB** to manage salary records with CRUD operations and support for fetching the latest record. Also designed to integrate with a machine learning model for salary prediction.

---

## Features

* Create, read, update, delete salary records
* Fetch the most recent salary record
* MongoDB async connection with Motor
* Auto-generated Swagger UI docs for easy testing
* ML model integration (via separate script)

---

## Setup & Run

1. Clone the repo
2. Create a `.env` file with:

   ```
   MONGO_URI=your_mongo_connection_string
   MONGO_DB=your_db_name
   MONGO_COLLECTION=your_collection_name
   ```
3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```
4. Run the API server

   ```bash
   uvicorn app:app --reload
   ```

---

## API Usage

To test/use the FastAPI, run:

* Access deployed API:
  
  ```bash
  https://loan-api-gvx3.onrender.com/docs
  ```
* Navigate to API path:

  ```bash
  cd API
  ```
* Install required packages:

  ```bash
  pip install -r requirements.txt
  ```
* Run the FastAPI app:

  ```bash
  uvicorn app:app --reload
  ```
* Interact with endpoints via Swagger UI at:
  `http://127.0.0.1:8000/docs`
  (Follow examples for proper request structure)

---

## ML Prediction

Use `predict.py` to fetch latest data from the API and run salary predictions with your trained model.

---


