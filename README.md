# ETL Coinbase API Project
This project is part of the Data Journey and aims to extract data from the Coinbase API, transform it, and load it for analysis.

![Draw of the Pipeline](https://github.com/user-attachments/assets/0b33c1a6-967c-4fc6-93c0-86ed613060ab)

## Important links FYI:
[PostgreSQL DB](https://dashboard-etl-api-coinbase.onrender.com) (yeah, it takes a while to open)
[Dashboard](https://db-etl-api-coinbase.onrender.com) (yeah, it takes a while to open)
[Logs](https://logfire.pydantic.dev/gustavoazreis/etl-api-coinbase)

## Repository Structure
- **app/:** Contains the main scripts for running the Streamlit dashboard.
- **src/:** Contains the main scripts for running the pipeline and loading data into databases.
- **examples/:** Includes sample study cases of API responses and how data is processed.
- **.gitignore:** Specifies which files or folders should be ignored by Git.
- **README.md:** This file, providing an overview of the project and instructions for use.
- **bitcoin.json:** JSON file containing sample Bitcoin data, stored in a TinyDB database.

## Prerequisites
Make sure you have the following tools installed on your machine:

**Python 3.x**
**pip**
**Render account**
**Logfire account**

## Installation
### Clone the repository:
`git clone https://github.com/gustavoazreis/ETLProjetoAPICoinbase.git`

### Navigate to the project directory:
`cd ETLProjetoAPICoinbase
`
### Create a virtual environment (optional, but recommended):
`python -m venv venv source venv\Scripts\activate`

### Install the dependencies:
`pip install -r requirements.txt`

## Configuration
Before running the project, configure the environment variables:

Create a .env file in the project root with the following information:

`postgres_user =
postgres_password =
postgres_host = 
postgres_port =  
postgres_db =  
LOGFIRE_TOKEN = 
PORT =`

## Execution
After configuration, run the main script in the src/ folder to start the ETL process:

`python src/pipeline_main.py`

The script will extract data from the Coinbase API, process it, and store it as defined in the project.

After that, run the main script in the app/ folder to start the dashboard:

`python app/dashboard_main.py`

## Cloud
I used Render to deploy the 3 services because it's open source, but it's up to you.
