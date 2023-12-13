from django.contrib import admin
from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='Main'),
    path('tables/', tables, name = "tables"),
    path('tables/get_table/',get_table,name="get_table"),
    path('adding/', add_page, name="add_page"),
    path('checking/',create_check,name='check_create'),
    path('lessoning/',create_lesson,name='check_create'),

    path('checking_change/',check_change,name='check_change'),
    path('tables/leave/',leave,name='leave'),

]
