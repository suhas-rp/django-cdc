from django.http import JsonResponse
from rest_framework.views import APIView
from .models import student, placementApplication
from django.db.models import Max, Min, Avg, Count, Q
import numpy as np

class statistics(APIView):
    def get(self, request, *args, **kwargs):
        # Get branch-wise statistics
        branch_data = self.get_branch_statistics()

        # Calculate median CTC for each branch
        median_ctc = self.calculate_median_ctc()

        # Fetch student data with placement details
        students_with_companies = self.get_students_with_companies()

        # Format the data for JSON response
        stats = self.format_statistics(branch_data, median_ctc, students_with_companies)

        return JsonResponse(stats)

    def get_branch_statistics(self):
        
        #Get branch-wise statistics for total students, placed students,
        #highest CTC, lowest CTC, and average CTC.
        
        # Get total students in each branch
        total_students = student.objects.values('branch').annotate(total=Count('id'))

        # Get placed students in each branch (count unique students)
        placed_students = placementApplication.objects.filter(selected=True).values(
            'student__branch'
        ).annotate(
            placed=Count('student', distinct=True),
            highest_ctc=Max('placement__ctc'),
            lowest_ctc=Min('placement__ctc'),
            average_ctc=Avg('placement__ctc')
        ).order_by('student__branch')

        # Merge the two queries
        branch_data = []
        for total in total_students:
            branch = total['branch']
            placed = placed_students.filter(student__branch=branch).order_by('student__branch').first()
            placed_count = placed['placed'] if placed else 0
            highest_ctc = placed['highest_ctc'] if placed and placed['highest_ctc'] is not None else None
            lowest_ctc = placed['lowest_ctc'] if placed and placed['lowest_ctc'] is not None else None
            average_ctc = placed['average_ctc'] if placed and placed['average_ctc'] is not None else None
            
            #appending data
            branch_data.append({
                'branch': branch,
                'total': total['total'],
                'placed': placed_count,
                'highest_ctc': highest_ctc,
                'lowest_ctc': lowest_ctc,
                'average_ctc': average_ctc
            })

        return branch_data

    def calculate_median_ctc(self):
        
        #Calculate the median CTC for each branch.
        
        median_ctc = {}
        branches = student.objects.values_list('branch', flat=True).distinct()
        for branch in branches:
            ctc_values = list(
                placementApplication.objects.filter(
                    student__branch=branch, selected=True
                ).values_list('placement__ctc', flat=True)
            )
            #assigning ctc values as per branch selected student's ctc
            if ctc_values:
                median_ctc[branch] = round(float(np.median(ctc_values)), 2)
            #using numpy to compute median
            else:
                median_ctc[branch] = None

        return median_ctc

    def get_students_with_companies(self):
        
        #Fetch student data with their placement details (companies selected and CTC).
        
        students_data = student.objects.annotate(
            highest_ctc=Max('placementapplication__placement__ctc', filter=Q(placementapplication__selected=True))
        ).values('rollno', 'branch', 'batch', 'highest_ctc')

        students_with_companies = []
        for student_data in students_data:
            companies_selected = list(
                placementApplication.objects.filter(
                    student_id=student_data['rollno'], selected=True
                ).values_list('placement__name', flat=True)
            )
            if companies_selected:
                companies_selected_value = companies_selected
            else:
                companies_selected_value = None

            if student_data['highest_ctc'] is not None:
                ctc_value = student_data['highest_ctc']
            else:
                ctc_value = None

            students_with_companies.append({
                "rollno": student_data['rollno'],
                "branch": student_data['branch'],
                "batch": student_data['batch'],
                "companies_selected": companies_selected_value,
                "ctc": ctc_value
            })

        return students_with_companies

    def format_statistics(self, branch_data, median_ctc, students_with_companies):
        
        #Format the statistics into a JSON-friendly structure.
        
        stats = {
            "highest_ctc": {},
            "lowest_ctc": {},
            "average_ctc": {},
            "median_ctc": {},
            "percentage_placed": {},
            "students": students_with_companies
        }

        # branch-wise statistics
        for data in branch_data:
            branch = data['branch']

            # assigning highest_ctc, lowest_ctc, percentage_placed and average_ctc
            if data['highest_ctc'] is not None:
                stats["highest_ctc"][branch] = data['highest_ctc']
            else:
                stats["highest_ctc"][branch] = None

            if data['lowest_ctc'] is not None:
                stats["lowest_ctc"][branch] = data['lowest_ctc']
            else:
                stats["lowest_ctc"][branch] = None

            if data['average_ctc'] is not None:
                stats["average_ctc"][branch] = round(data['average_ctc'], 2)
            else:
                stats["average_ctc"][branch] = None

            if data['total'] > 0:
                stats["percentage_placed"][branch] = round((data['placed'] / data['total']) * 100, 2)
            else:
                stats["percentage_placed"][branch] = None

        # Populate median_ctc
        for branch, median_value in median_ctc.items():
            if median_value is not None:
                stats["median_ctc"][branch] = median_value
            else:
                stats["median_ctc"][branch] = None

        return stats