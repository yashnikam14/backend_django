import random
import threading
from datetime import datetime

from django.core.management.base import BaseCommand
from utils.loggers import log_into_file
import pandas as pd
import os
import json
from backend_app.models import MarkSheet, StudDetails, Cities, States
from django.utils import timezone
import traceback
from threading import Thread

folder_path = os.path.join(os.getcwd(), 'data_files')

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

cities = [
    "New York", "London", "Tokyo", "Paris", "Sydney",
    "Berlin", "Toronto", "Mumbai", "Dubai", "Rome",
    "Los Angeles", "Cape Town", "Amsterdam", "Barcelona",
    "Singapore", "Melbourne", "Rio de Janeiro", "Seoul",
    "Moscow", "Istanbul", "Lagos", "Mexico City",
    "Kuala Lumpur", "Buenos Aires", "Lagos", "Cairo",
    "Bangkok", "São Paulo", "Hong Kong", "San Francisco",
    "Mexico City", "Chicago", "Vienna", "Madrid"
]

states = [
    "California", "Texas", "Florida", "New York", "Illinois",
    "Pennsylvania", "Ohio", "Georgia", "North Carolina", "Michigan"
]


class Command(BaseCommand):
    args = ''
    help = 'Export data to remote server'

    def handle(self, *args, **options):
        try:
            log_into_file({"function": "handle", "started": True})
            DataValidator().handle_data()
            # StudentDetails().handle_cities()
            # stud = StudentDetails()
            # th = []
            # for i in cities:
            #     t = threading.Thread(target=stud.create_city, args=(i,))
            #     t.start()
            #     th.append(t)
            # for i in states:
            #     t = threading.Thread(target=stud.create_state, args=(i,))
            #     t.start()
            #     th.append(t)
            # for t in th:
            #     t.join()
            log_into_file({"function": "handle", "completed": True})

        except Exception as e:
            log_into_file({"function": "handle", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})


class DataValidator:
    def handle_data(self):
        try:
            log_into_file({"function": "handle_data", "started": True})
            for file_name in csv_files:
                file_path = os.path.join(folder_path, file_name)

                df = pd.read_csv(file_path, usecols=['Name', 'Gender', 'Age', 'Section', 'Science', 'English', 'History', 'Maths'])
                naive_datetime = datetime.now()

                aware_datetime = timezone.make_aware(naive_datetime)
                for index, row in df.iterrows():
                    entry = MarkSheet(name=row['Name'], gender=row['Gender'], age=row['Age'], section=row['Section'], marks=json.dumps({
                            'science': row['Science'],
                            'english': row['English'],
                            'history': row['History'],
                            'maths': row['Maths']
                        }), creation_time=aware_datetime)
                    entry.save()
                log_into_file({"function": "handle_data", "file": file_name, "data_inserted": True})
                print(file_name)
                os.remove(file_path)

            log_into_file({"function": "handle_data", "completed": True})

        except Exception as e:
            log_into_file({"function": "handle_data", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})



class StudentDetails:
    def handle_cities(self):
        try:
            log_into_file({"function": "handle_cities", "started": True})
            get_all_records = StudDetails.objects.filter(city=None).all()
            thread_lst = []
            for record in get_all_records:
                city_thread = threading.Thread(target=self.add_cities, args=(record,))
                city_thread.start()
                thread_lst.append(city_thread)

            for th in thread_lst:
                th.join()
            log_into_file({"function": "handle_cities", "completed": True})

        except Exception as e:
            log_into_file({"function": "handle_cities_cities", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})

    def add_cities(self, record):
        try:
            log_into_file({"function": "add_cities", "started": True})
            city_id = int(random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]))
            record.city = city_id
            record.save(update_fields=['city'])
            log_into_file({"function": "add_cities", "completed": True})

        except Exception as e:
            log_into_file({"function": "add_cities", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})

    def create_city(self, city):
        try:
            log_into_file({"function": "create_city", "started": True})
            state = int(random.choice([1,2,3,4,5,6,7,8,9,10]))
            new_city = Cities(name=city, state_id=state)
            new_city.save()
            log_into_file({"function": "create_city", "completed": True})

        except Exception as e:
            log_into_file({"function": "create_city", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})

    def create_state(self, state):
        try:
            log_into_file({"function": "create_state", "started": True})
            new_state = States(name=state)
            new_state.save()
            log_into_file({"function": "create_state", "completed": True})

        except Exception as e:
            log_into_file({"function": "create_state", "exception": str(e),
                           "exception_type": type(e).__name__, "exception_at": traceback.format_exc()})