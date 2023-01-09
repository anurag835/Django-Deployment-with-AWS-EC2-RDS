from import_export import resources
from .models import *


class UserDataResource(resources.ModelResource):
    class meta:
        model = UserData


class UserInputResource(resources.ModelResource):
    class meta:
        model = UserInput
