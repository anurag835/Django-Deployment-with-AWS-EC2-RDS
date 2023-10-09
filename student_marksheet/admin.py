from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(UserData)
class UserDataAdmin(ImportExportModelAdmin):
    list_display = ('roll', 'name', 'parentName', 'course', 'branch', 'logo')


@admin.register(UserInput)
class UserInputAdmin(ImportExportModelAdmin):
    list_display = ('roll', 'subject1', 'maxMarkSub1', 'markObSub1', 'subject2', 'maxMarkSub2', 'markObSub2', 'subject3',
                    'maxMarkSub3', 'markObSub3', 'subject4', 'maxMarkSub4', 'markObSub4', 'subject5', 'maxMarkSub5', 'markObSub5', 'subject6', 'maxMarkSub6', 'markObSub6')
