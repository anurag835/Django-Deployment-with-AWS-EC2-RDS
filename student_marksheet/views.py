from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .resources import *
from django.contrib import messages
from tablib import Dataset
from django.utils.datastructures import MultiValueDictKeyError
from .helpers import render_to_pdf
from django.template.loader import get_template

from django.views.generic import View
# Create your views here.

# View for uploading data.xlsx file


def file_upload(request):
    if request.method == "POST":
        user_data_resource = UserDataResource()
        dataset = Dataset()
        try:
            excel_file = request.FILES["myfile"]
            if not excel_file.name.endswith('.xlsx'):
                messages.info(request, "Wrong format")
                return render(request, 'student_marksheet/upload.html')

            imported_data = dataset.load(excel_file.read(), format='xlsx')
            result = user_data_resource.import_data(dataset, dry_run=True)
            if not result.has_errors():
                user_data_resource.import_data(dataset, dry_run=False)
            for data in imported_data:
                value = UserData(
                    data[0], data[1], data[2], data[3], data[4]
                )
                value.save()
        except MultiValueDictKeyError as e:
            print(e)
    return render(request, 'student_marksheet/upload.html')

# View for uploading user_input.xlsx file


def simple_file_upload(request):
    if request.method == "POST":
        user_input_resource = UserInputResource()
        dataset2 = Dataset()
        try:
            excel_file = request.FILES["myfile"]
            if not excel_file.name.endswith('.xlsx'):
                messages.info(request, "Wrong format")
                return render(request, 'student_marksheet/upload.html')

            imported_data2 = dataset2.load(excel_file.read(), format='xlsx')
            result2 = user_input_resource.import_data(dataset2, dry_run=True)
            if not result2.has_errors():
                user_input_resource.import_data(dataset2, dry_run=False)

            for data2 in imported_data2:
                user_data = UserData.objects.get(roll=data2[0])
                value2 = UserInput(
                    data2[0], data2[1], data2[2], data2[3], data2[4],
                    data2[5], data2[6], data2[7], data2[8], data2[9],
                    data2[10], data2[11], data2[12], data2[13], data2[14],
                    data2[15], data2[16], data2[17], data2[18], user_data
                )
                value2.save()

        except MultiValueDictKeyError as e:
            print(e)

    return render(request, 'student_marksheet/upload.html')

# View for getting data from database model


def get_data(request, roll):
    context = {}
    pi = UserInput.objects.get(roll=roll)
    context['data'] = pi

    total_sum = pi.markObSub1+pi.markObSub2+pi.markObSub3 + \
        pi.markObSub4+pi.markObSub5+pi.markObSub6
    context['total_sum'] = total_sum
    max_marks = pi.maxMarkSub1+pi.maxMarkSub2+pi.maxMarkSub3 + \
        pi.maxMarkSub4+pi.maxMarkSub5+pi.maxMarkSub6

    context['max_marks'] = max_marks

    percentage = total_sum/max_marks*100
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
        print(roll)
        context = {}
        data = UserInput.objects.get(roll=roll)
        context['data'] = data

        total_sum = data.markObSub1+data.markObSub2+data.markObSub3 + \
            data.markObSub4+data.markObSub5+data.markObSub6
        context['total_sum'] = total_sum
        max_marks = data.maxMarkSub1+data.maxMarkSub2+data.maxMarkSub3 + \
            data.maxMarkSub4+data.maxMarkSub5+data.maxMarkSub6

        context['max_marks'] = max_marks

        percentage = total_sum/max_marks*100
        if percentage >= 90:
            context['grade'] = "A"
        else:
            context['grade'] = "F"

        print(data)
        template = get_template('student_marksheet/marksheet.html')
        context['data'] = data
        html = template.render(context)
        # print("html#########", html)
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
