from django.core.management.base import BaseCommand
from utils.loggers import log_into_file
import os
import random
import csv
from datetime import datetime


folder_path = os.path.join(os.getcwd(), 'data_files')

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

genders = ['Male', 'Female']
sections = ['A', 'B', 'C', 'D']
subjects = ['Science', 'English', 'History', 'Maths']
name = [
    'John', 'Alice', 'Emma', 'James', 'Olivia', 'Lucas', 'Sophia', 'Liam', 'Isabella', 'Mason',
    'Ava', 'Ethan', 'Mia', 'Jackson', 'Charlotte', 'Logan', 'Amelia', 'Aiden', 'Harper', 'Henry',
    'Ella', 'Daniel', 'Grace', 'Samuel', 'Zoe', 'Isaac', 'Nora', 'Wyatt', 'Emily', 'Owen', 'Scarlett',
    'Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin',
    'Thompson', 'Garcia', 'Martinez', 'Roberts', 'Clark', 'Rodriguez', 'Lewis', 'Walker', 'Allen', 'Young',
    'King', 'Scott', 'Green', 'Baker', 'Adams', 'Nelson', 'Hill', 'Davis', 'Carter', 'Mitchell', 'Perez'
]

class Command(BaseCommand):
    args = ''
    help = 'Export data to remote server'

    def handle(self, *args, **options):
        try:
            log_into_file({"function": "handle", "started": True})
            new_students = DataGenerator().generate_student_data(1, 5000)
            if not os.path.exists('data_files'):
                os.makedirs('data_files')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"students_data_{timestamp}.csv"
            file_path = os.path.join('data_files', file_name)

            with open(file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file,
                                        fieldnames=["id", "Name", "Gender", "Age", "Section", "Science", "English",
                                                    "History", "Maths"])
                writer.writeheader()
                writer.writerows(new_students)

            print("generated file name: ", file_name)
            log_into_file({"function": "handle", "file_created": file_name})
            log_into_file({"function": "handle", "completed": True})

        except Exception as e:
            log_into_file({"function": "handle", "exception": str(e)})


class DataGenerator:

    def generate_student_data(self, start_id, num_students):
        try:
            students = []
            log_into_file({"function": "generate_student_data", "started": True})
            for student_id in range(start_id, start_id + num_students):
                student = {
                    "id": student_id,
                    "Name": "{} {}".format(random.choice(name), random.choice(name)),
                    "Gender": random.choice(genders),
                    "Age": int(random.choice([15, 16, 17, 18, 19, 20, 21, 22])),
                    "Section": random.choice(sections),
                    "Science": random.randint(1, 100),
                    "English": random.randint(1, 100),
                    "History": random.randint(1, 100),
                    "Maths": random.randint(1, 100)
                }
                students.append(student)
            log_into_file({"function": "generate_student_data", "completed": True})
            return students

        except Exception as e:
            log_into_file({"function": "generate_student_data", "exception": str(e)})

