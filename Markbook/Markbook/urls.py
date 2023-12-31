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
    path('lessoning/',create_lesson,name='lesson_create'),
    path('deleting/',delete_lesson,name='lesson_delete'),
    path('theme/',change_theme,name='change_theme'),
    path('checking_change/',check_change,name='check_change'),
    path('tables/leave/',leave,name='leave'),
    path('adminschedule/leave/',leave,name='leave'),
    path('adding/leave/',leave,name='leave'),
    path('adminschedule/',adminschedule,name='adminschedule'),
    path('adminschedule/get_table/',get_table,name="get_table"),
    path('adminschedule/student_load/',student_load,name='adminschedule'),
    path('adminstatistics/', adminstatistic, name = 'adminstat'),
    path('statistics/',statistics,name='statistics'),
    path('statistics/leave/',leave,name='leave'),
    path('adminstatistics/leave/',leave,name='leave'),
    path('statistic/',statistic,name="statistic"),
    path("adminstat/", adminstat , name = "adminstat"),


]
