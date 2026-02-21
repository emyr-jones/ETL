from faker import Faker
import random
import string
import pandas as pd
from google.cloud import storage

fake = Faker()

# -------- SETTINGS --------
NUM_EMPLOYEES = 100
BUCKET_NAME = "nkt-employee-data"   # ✅ removed space
DESTINATION_BLOB_NAME = "employee_data.csv"
# --------------------------

departments = ["Engineering", "HR", "Finance", "Marketing", "Sales", "Operations"]

employee_data = []

password_characters = string.ascii_letters + string.digits

for _ in range(NUM_EMPLOYEES):
    employee = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "job_title": fake.job(),
        "department": random.choice(departments),
        "email": fake.email(),
        "address": fake.address().replace("\n", ", "),
        "phone_number": fake.phone_number(),
        "salary": random.randint(40000, 150000),
        "password": "".join(random.choice(password_characters) for _ in range(8))
    }

    employee_data.append(employee)

# ---------- SAVE TO CSV ----------
df = pd.DataFrame(employee_data)
csv_filename = "employee_data.csv"
df.to_csv(csv_filename, index=False)

print("CSV file created locally.")

# ---------- UPLOAD TO GCP ----------
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)  # slightly stricter than client.bucket()
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to gs://{bucket_name}/{destination_blob_name}")

upload_to_gcs(BUCKET_NAME, csv_filename, DESTINATION_BLOB_NAME)