# SuadeReport
📖 About

Suade Report is a web application that generates reports based on data from CSV files. It provides insights and analytics for a specific date, including information about customers, items sold, discounts, commissions, and more.

## 🛠️ Setup


1. Clone the repository:

```
git clone https://github.com/your-username/suade-report.git
```

2. Set up virtual environment:

```
pip3 install virtualenv
```

3. Then activate it with:

```
virtualenv ./venv  # Windows
source venv/bin/activate  # Linux
```

4. Install python dependencies:

```
python3 -m pip install -r requirements.txt
```

## ⚙️ Run the API

1. Start the web application by running the following command:

```
cd api
uvicorn main:app 
```
2. Open your browser and navigate to http://localhost:8000 to access the application.

3. The API provides a /get_report endpoint that accepts a date parameter in the format of YYYY-MM-DD. It returns a report for the specified date.

## 🧑‍💻 Development
The Suade Report project is built using the following technologies:

- Python: The core programming language used for development.
- FastAPI: A modern, fast (high-performance), web framework for building APIs.
- Pandas: A powerful library for data manipulation and analysis.
- uvicorn: A lightning-fast ASGI server implementation.
