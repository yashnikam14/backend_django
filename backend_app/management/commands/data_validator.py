from datetime import datetime

from django.core.management.base import BaseCommand
from utils.loggers import log_into_file
import pandas as pd
import os
import json
from backend_app.models import MarkSheet
from django.utils import timezone
import traceback

folder_path = os.path.join(os.getcwd(), 'data_files')

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]


class Command(BaseCommand):
    args = ''
    help = 'Export data to remote server'

    def handle(self, *args, **options):
        try:
            log_into_file({"function": "handle", "started": True})
            DataValidator().handle_data()

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

