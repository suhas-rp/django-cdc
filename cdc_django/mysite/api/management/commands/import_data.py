import csv
from django.core.management.base import BaseCommand
from api.models import student, placement, placementApplication

class Command(BaseCommand):
    #class command to import data into the required class types ex: student
    def handle(self, *args, **kwargs):
        # Import Students
        with open('students.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                student.objects.get_or_create(
                    id=row['id'],
                    rollno=row['rollno'],
                    batch=row['batch'],
                    branch=row['branch']
                )
        
        # Import Placements
        with open('placements.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                placement.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    role=row['role'],
                    ctc=float(row['ctc'])
                )
        
        # Import Placement Applications
        with open('placement_applications.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                placementApplication.objects.get_or_create(
                    id=row['id'],
                    placement_id=row['placementid'],
                    student_id=row['studentid'],
                    selected=(row['selected'].strip().lower() == 'true')
                )

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))