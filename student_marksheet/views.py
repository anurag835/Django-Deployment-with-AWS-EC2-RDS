from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserData, UserInput
from .resources import UserDataResource, UserInputResource
from django.contrib import messages
from tablib import Dataset
from django.utils.datastructures import MultiValueDictKeyError
from .helpers import render_to_pdf
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.db import IntegrityError
# Create your views here.

# View for uploading data.xlsx file

@csrf_exempt
def file_upload(request):
    if request.method == "POST":
        user_data_resource = UserDataResource()
        dataset = Dataset()
        try:
            excel_file = request.FILES["myfile"]
            if not excel_file.name.endswith('.xlsx'):
                messages.info(request, "Invalid file format. Please upload a valid Excel file.")
                return render(request, 'student_marksheet/upload.html')

            imported_data = dataset.load(excel_file.read(), format='xlsx')
            result = user_data_resource.import_data(dataset, dry_run=True)
            if not result.has_errors():
                try:
                    user_data_resource.import_data(dataset, dry_run=False)
                except IntegrityError as e:
                    messages.error(request, "Error uploading data: Integrity constraint violation.")
                    return render(request, 'student_marksheet/upload.html')

            for data in imported_data:
                value = UserData(
                    data[0], data[1], data[2], data[3], data[4]
                )
                value.save()
        except MultiValueDictKeyError as e:
            messages.error(request, "No file uploaded.")
            print(e)
    return render(request, 'student_marksheet/upload.html')


# View for uploading user_input.xlsx file
@csrf_exempt
def simple_file_upload(request):
    if request.method == "POST":
        user_input_resource = UserInputResource()
        dataset2 = Dataset()
        try:
            excel_file = request.FILES["myfile"]
            if not excel_file.name.endswith('.xlsx'):
                messages.info(request, "Invalid file format. Please upload a valid Excel file.")
                return render(request, 'student_marksheet/upload.html')

            imported_data2 = dataset2.load(excel_file.read(), format='xlsx')
            # Check if all userdata_id values exist in the database
            userdata_ids = [data2[0] for data2 in imported_data2]
            missing_userdata_ids = set(userdata_ids) - set(UserData.objects.values_list('roll', flat=True))
            
            if missing_userdata_ids:
                messages.error(request, f"Error uploading data: Userdata IDs not found - {', '.join(missing_userdata_ids)}")
                return render(request, 'student_marksheet/upload.html')

            result2 = user_input_resource.import_data(dataset2, dry_run=True)
            if not result2.has_errors():
                try:
                    user_input_resource.import_data(dataset2, dry_run=False)
                except IntegrityError as e:
                   messages.error(request, "Error uploading data: Integrity constraint violation.")
                   return render(request, 'student_marksheet/upload.html')

            for data2 in imported_data2:
                value2 = UserInput(
                    data2[0], data2[1], data2[2], data2[3], data2[4],
                    data2[5], data2[6], data2[7], data2[8], data2[9],
                    data2[10], data2[11], data2[12], data2[13], data2[14],
                    data2[15], data2[16], data2[17], data2[18], data2[0]
                )
                value2.save()

        except MultiValueDictKeyError as e:
            messages.error(request, "No file uploaded.")
            print(e)

    return render(request, 'student_marksheet/upload.html')


# Create a utility function to calculate total_sum, max_marks, and percentage
def calculate_marks(data):
    total_sum = data.markObSub1 + data.markObSub2 + data.markObSub3 + data.markObSub4 + data.markObSub5 + data.markObSub6
    max_marks = data.maxMarkSub1 + data.maxMarkSub2 + data.maxMarkSub3 + data.maxMarkSub4 + data.maxMarkSub5 + data.maxMarkSub6
    percentage = (total_sum / max_marks) * 100 if max_marks != 0 else 0
    return total_sum, max_marks, percentage


# View for getting data from database model
def get_data(request, roll):
    context = {}
    try:
        data = UserInput.objects.get(roll=roll)
    except UserInput.DoesNotExist:
        messages.error(request, f"User with roll number {roll} does not exist.")
        return redirect('input_roll')

    total_sum, max_marks, percentage = calculate_marks(data)

    context['data'] = data
    context['total_sum'] = total_sum
    context['max_marks'] = max_marks

    if percentage >= 90:
        context['grade'] = "A"
    else:
        context['grade'] = "F"
    return render(request, 'student_marksheet/index.html', context)


# View for user enter roll number
def input_roll(request):
    if request.method == "POST":
        roll = request.POST.get('roll')
        return redirect(f"/get-data/{roll}")
    return render(request, 'student_marksheet/inputform.html')


class GeneratePDFView(View):
    def get(self, request, roll, * args, **kwargs):
        context = {}
        try:
            data = UserInput.objects.get(roll=roll)
        except UserInput.DoesNotExist:
            # Handle the case where the user with the specified roll number doesn't exist
            messages.error(request, f"User with roll number {roll} does not exist.")
            return redirect('input_roll')
        
        total_sum, max_marks, percentage = calculate_marks(data)

        context['data'] = data
        context['total_sum'] = total_sum
        context['max_marks'] = max_marks

        if percentage >= 90:
            context['grade'] = "A"
        else:
            context['grade'] = "F"

        template = get_template('student_marksheet/marksheet.html')
        context['data'] = data
        html = template.render(context)
        pdf = render_to_pdf('student_marksheet/marksheet.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"{data.userdata.name} {data.userdata.roll}.pdf"
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
