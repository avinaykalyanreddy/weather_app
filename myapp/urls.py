from django.urls import  path


from . import views



urlpatterns = [

    path("",views.input_func,name="user_input")
]