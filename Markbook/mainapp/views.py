from django.shortcuts import render
from django.contrib.auth.views import *
from django.shortcuts import redirect
from mainapp.forms import *
from mainapp.models import *
from django.http import HttpResponse
import json
from datetime import datetime
def main_page(request):
    context = {}
    form = StudentLoginForm
    model = Student
    if request.method == "POST":

        if request.session.test_cookie_worked():
            field = form(request.POST)
            if field.is_valid():
                user = Student.objects.get(code = field.data['code'])
                request.session["student_id"] = user.id
                return redirect('/tables')
    else:
        field = form()
        context['field'] = field
    request.session.set_test_cookie()
    return render(request, 'mainpage.html',context)

def tables(request):
    user = Student.objects.get(id = request.session['student_id'])
    context = {}
    context['username'] = user.firstname
    return render(request,'Schedule.html',context)

def is_date_in_range(date_to_check, start_date, end_date):
    date_to_check = datetime.strptime(date_to_check, '%d.%m.%Y')
    start_date = datetime.strptime(start_date, '%d.%m.%Y')
    end_date = datetime.strptime(end_date, '%d.%m.%Y')
    return start_date <= date_to_check <= end_date


def get_table(request):
    r = json.loads(request.body)
    context = {}
    print(r['date'],r['day'])
    arr = Lesson.objects.filter(day_of_Week = r['day'])
    for i in range(len(arr)):
        sub = {}
        sub['name']=arr[i].name
        sub['time']=arr[i].time
        context[str(i+1)]=sub
        context[str(i+1)]=sub
    print(context)
    return HttpResponse(json.dumps(context, ensure_ascii=False),content_type="application/json")

def add_page(request):
    return render(request,"AddTimetable.html")