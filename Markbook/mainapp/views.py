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
    if(request.session["student_id"]==None):
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
    else:
        return redirect(tables)


def leave(request):
    request.session["student_id"]=None
    return redirect(main_page)

def tables(request):
    if(request.session["student_id"]!=None):
        user = Student.objects.get(id = request.session['student_id'])
        context = {}
        context['username'] = user.firstname
        context['student_id'] = user.id
        return render(request,'Schedule.html',context)
    else:
        return redirect(main_page)

def is_date_in_range(date_to_check, start_date, end_date):
    date_to_check = datetime.strptime(date_to_check, '%d.%m.%Y')
    start_date = datetime.strptime(start_date, '%d.%m.%Y')
    end_date = datetime.strptime(end_date, '%d.%m.%Y')
    return start_date <= date_to_check <= end_date

def create_check(request):
    data = json.loads(request.body.decode('utf-8'))
    student = Student.objects.get(id = data['student_id'])
    lesson = Lesson.objects.get(id = int(data['lesson_id']))
    print(lesson.id)
    check = Check(student=student, lesson=lesson, date=data['date'], ison=data['ison'])
    check.save()
    return HttpResponse()

def check_change(request):
    data = json.loads(request.body.decode('utf-8'))
    student = Student.objects.get(id = data['student_id'])
    lesson = Lesson.objects.get(id = int(data['lesson_id']))
    print(lesson.id)
    check = Check.objects.get(student=student, lesson=lesson, date=data['date'])
    check.ison = data['ison']
    check.save()
    return HttpResponse()

def get_table(request):
    r = json.loads(request.body)
    context = {}
    student = Student.objects.get(id = int(request.session['student_id']))
    arr = Lesson.objects.filter(day_of_Week = r['day'])
    for i in range(len(arr)):
        if(is_date_in_range(r['date'],arr[i].start_time,arr[i].end_time)):
            sub = {}
            checks = Check.objects.filter(lesson = arr[i], date = r['date'],student = student)
            sub['name']=arr[i].name
            sub['time']=arr[i].time
            sub['id']  =arr[i].id
            if(len(checks)!=0):
                sub['check'] = checks[0].ison
                print(sub['check'])
            else:
                sub['check'] = '-1'
            print(sub)
            context[str(i+1)]=sub
            context[str(i+1)]=sub
    return HttpResponse(json.dumps(context, ensure_ascii=False),content_type="application/json")

def add_page(request):
    context = {}
    lessons = Lesson.objects.filter()
    context['lessons'] = lessons
    return render(request,"AddTimetable.html",context)

def create_lesson(request):
    data = json.loads(request.body.decode('utf-8'))
    lesson = Lesson(name = data['name'], start_time = data['start'], end_time =['end'], day_of_Week = data['day'],time=data['time'], group = Group.objects.get())
    print(lesson)
    lesson.save()
    return HttpResponse()

def delete_lesson(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data['id'])
    Lesson.objects.get(id=int(data['id'])).delete()
    return HttpResponse()