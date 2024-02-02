import csv
import random
from faker import Faker
import hashlib

def generate_fake_data(num_records=10):
    fake = Faker()

    data = []
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        address = fake.address()
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=65)

        data.append([first_name, last_name, address, date_of_birth])

    return data

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['first_name', 'last_name', 'address', 'date_of_birth'])
        csv_writer.writerows(data)

def anonymize_data(input_filename='generated_data.csv', output_filename='anonymized_data.csv'):
    with open(input_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        header = reader.fieldnames

        anonymized_data = []
        for row in reader:
            anonymized_row = {
                'first_name': hashlib.sha256(row['first_name'].encode()).hexdigest(),
                'last_name': hashlib.sha256(row['last_name'].encode()).hexdigest(),
                'address': hashlib.sha256(row['address'].encode()).hexdigest(),
                'date_of_birth': row['date_of_birth']
            }
            anonymized_data.append(anonymized_row)

    with open(output_filename, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=header)
        csv_writer.writeheader()
        csv_writer.writerows(anonymized_data)

if __name__ == "__main__":
    num_records = 10  # You can adjust the number of records as needed
    fake_data = generate_fake_data(num_records)
    write_to_csv(fake_data,'generated_data.csv')

    input_filename = 'generated_data.csv'
    output_filename = 'anonymized_data.csv'
    anonymize_data(input_filename, output_filename)