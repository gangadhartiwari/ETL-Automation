import json
import pyodbc
from datetime import datetime

# ===================== SETTINGS =====================
json_file = r'C:/Users/synchem/Desktop/MargtoSQL/decrypted_output.json'  # JSON file path
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=edp;"      # SQL Server address
    "DATABASE=MargLiveData;"  # Your database name
    "UID=sa;"      # Your username
    "PWD=sfa;"  # Your password
)

# ===================== HELPER FUNCTIONS =====================

# Load JSON data
def load_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

# Establish SQL connection
def create_connection():
    return pyodbc.connect(conn_str)

# Get records for a given table from JSON
def get_records(table, data):
    root = data.get('Details', {})
    table_data = root.get(table, [])
    return table_data if isinstance(table_data, list) else []

# Normalize and prepare records (simple example, you can expand as needed)
def prepare_record(record):
    # Here you can add any custom normalization logic
    return record

# Insert records into database
def upsert_records(cursor, table, records):
    if not records:
        return

    key_columns = ['ID', 'CompanyID']
    all_columns = list(records[0].keys())
    non_key_columns = [c for c in all_columns if c not in key_columns]

    source_cols = ', '.join(all_columns)
    source_vals = ', '.join(['?'] * len(all_columns))

    on_clause = ' AND '.join([f"target.{k} = source.{k}" for k in key_columns])

    update_clause = ', '.join([f"target.{c} = source.{c}" for c in non_key_columns])

    insert_cols = ', '.join(all_columns)
    insert_vals = ', '.join([f"source.{c}" for c in all_columns])

    sql = f"""
    MERGE {table} AS target
    USING (SELECT {source_vals}) AS source ({source_cols})
    ON {on_clause}
    WHEN MATCHED THEN
        UPDATE SET {update_clause}
    WHEN NOT MATCHED THEN
        INSERT ({insert_cols})
        VALUES ({insert_vals});
    """

    for record in records:
        values = tuple(record[col] for col in all_columns)
        cursor.execute(sql, values)

    cursor.commit()
    print(f"Upserted {len(records)} records into {table}")


# ===================== MAIN SCRIPT =====================

def main():
    try:
        # Load data from JSON
        data = load_json(json_file)

        # Create SQL connection
        conn = create_connection()
        cursor = conn.cursor()
        print("Connected to SQL Server")

        # Tables to process
        tables = ['Dis', 'Masters', 'MDis', 'Party', 'Product', 'SaleType', 'Stock', 'Account', 'AcBal', 'Outstanding', 'PBal', 'ACgroup', 'MComp']

        for table in tables:
            # Get records for the table
            records = get_records(table, data)
            if not records:
                print(f"No data found for table {table}. Skipping...")
                continue
            
            # Prepare records (optional normalization)
            records = [prepare_record(record) for record in records]

            for record in records:
                if 'Group' in record:
                    record['Group1'] = record.pop('Group')

            # Insert records into the corresponding table
            upsert_records(cursor, table, records)

        print("Data insertion complete!")

    except pyodbc.Error as e:
        print(f"Error: {e}")
    
    finally:
        # Close the cursor and connection
        try:
            cursor.close()
            conn.close()
            print("Connection closed")
        except Exception as e:
            print(f"Error closing connection: {e}")

# Run the script
if __name__ == "__main__":
    main()
