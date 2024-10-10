# Run file once to get clinical trials description
import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine

# Create SQLAlchemy Engine
from urllib.parse import quote

with open('password.txt', 'r') as file:
    password = file.read().strip()

username = 'andai'

quoted_username = quote(username)
quoted_password = quote(password)


url = f"postgresql://{quoted_username}:{quoted_password}@aact-db.ctti-clinicaltrials.org:5432/aact"
engine = create_engine(url)

# Execute SQL Query
query = """

SELECT DISTINCT
	countries.nct_id AS nct_id,
	studies.study_first_submitted_date AS first_date,
	detailed_descriptions AS description
	
	FROM countries
	INNER JOIN studies USING (nct_id)
	INNER JOIN detailed_descriptions USING (nct_id)
	WHERE countries.name = 'Kenya'
		AND studies.study_first_submitted_date BETWEEN '2020-01-01' AND '2023-12-31'
		ORDER BY first_date DESC;
"""

data = pd.read_sql_query(query, engine)
engine.dispose()

# Save  Data
trial_data_path = "data/raw"

def save_data(data, data_path):
    #create a dir if it does not exist
    path = os.path.join(trial_data_path, data_path.split('/')[0])
    if not os.path.exists(path):
        os.makedirs(path)
    saved_path = os.path.join(trial_data_path, f'{data_path}.csv')
    data.to_csv(saved_path, index=False)
    
    # Get the absolute path
    abs_path = os.path.abspath(saved_path)

    print("Saved to ✅:", abs_path)

save_data(data, 'trial_data/study_descriptions')