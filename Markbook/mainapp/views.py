from django.shortcuts import render
from django.contrib.auth.views import *
from django.shortcuts import redirect
from mainapp.forms import *
from mainapp.models import *
from django.http import HttpResponse
import json
from datetime import datetime
import math

def isadmin(func):
    def wrapper(request, *args, **kwargs):
        student_id = request.session.get("student_id")
        if student_id == 2:
            return func(request, *args, **kwargs)
        else:
            return redirect('Main')
    return wrapper

def main_page(request):
    context = {}
    if request.session.get("student_id") is None:
        request.session.set_test_cookie()
        
        if request.method == "POST":
            form = StudentLoginForm(request.POST)
            context['form'] = form

            if form.is_valid():
                try:
                    user = Student.objects.get(code=form.cleaned_data['code'])
                    request.session["student_id"] = user.id
                    if request.session.get("student_id") == 2:
                        return redirect('/adminschedule')
                    else:
                        print(request.session.get("student_id"))
                        return redirect('/tables')
                except Student.DoesNotExist:
                    form.add_error('code', 'Неверный код')
        else:
            form = StudentLoginForm()
            context['form'] = form

        return render(request, 'mainpage.html', context)
    else:
        if request.session.get("student_id") == 2:
            return redirect("/adminschedule")
        else:
            return redirect('/tables')


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


@isadmin
def adminschedule(request):
    context = {'username':Student.objects.get(id=request.session.get('student_id')).firstname}
    return render(request,'MashaClient.html',context)

@isadmin
def adminstatistic(request):
    context = {'username':Student.objects.get(id=request.session.get('student_id')).firstname}
    return render(request,'adminstatistic.html',context)

def statistics(request):
    if request.session.get("student_id") is not None:
        student = Student.objects.get(id=request.session.get('student_id'))
        context = {'username': student.firstname, 'student_id': student.id}
        return render(request,'statisctics.html',context)
    else:
        return redirect("Main")

def difference(date1, date2):
    format = "%d.%m.%Y"
    date1 = datetime.strptime(date1, format)
    date2 = datetime.strptime(date2, format)
    difference = date2 - date1
    return difference.days

def statistic(request):
    context={}
    student = Student.objects.get(id = request.session.get('student_id'))
    checks = Check.objects.filter(student = student)
    lessons = Lesson.objects.filter()
    sub = {}
    today = datetime.today().strftime('%d.%m.%Y')
    
    for i in range(len(lessons)):
        sub[lessons[i].name]['all'] = math.ceil(difference(today,lessons[i].end_time)/7)
    print(sub)
    return HttpResponse(json.dumps(context, ensure_ascii=False),content_type="application/json")


def is_date_in_range(date_to_check, start_date, end_date):
    date_to_check = datetime.strptime(date_to_check, '%d.%m.%Y')
    start_date = datetime.strptime(start_date, '%d.%m.%Y')
    end_date = datetime.strptime(end_date, '%d.%m.%Y')
    return start_date <= date_to_check <= end_date

def create_check(request):
    data = json.loads(request.body.decode('utf-8'))
    student = Student.objects.get(id = data['student_id'])
    lesson = Lesson.objects.get(id = int(data['lesson_id']))
    check = Check(student=student, lesson=lesson, date=data['date'], ison=data['ison'])
    check.save()
    return HttpResponse()

def check_change(request):
    data = json.loads(request.body.decode('utf-8'))
    student = Student.objects.get(id = data['student_id'])
    lesson = Lesson.objects.get(id = int(data['lesson_id']))
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
            else:
                sub['check'] = '-1'
            context[str(i+1)]=sub
            context[str(i+1)]=sub
    return HttpResponse(json.dumps(context, ensure_ascii=False),content_type="application/json")

@isadmin
def add_page(request):
    context = {'username':Student.objects.get(id=request.session.get('student_id')).firstname}
    lessons = Lesson.objects.filter()
    context['lessons'] = lessons
    return render(request,"AddTimetable.html",context)


def create_lesson(request):
    data = json.loads(request.body.decode('utf-8'))
    lesson = Lesson(name = data['name'], start_time = data['start'], end_time =['end'], day_of_Week = data['day'],time=data['time'], group = Group.objects.get())
    lesson.save()
    return HttpResponse()

def delete_lesson(request):
    data = json.loads(request.body.decode('utf-8'))
    Lesson.objects.get(id=int(data['id'])).delete()
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
            else:
                sub['check'] = '-1'
            context[str(i+1)]=sub
            context[str(i+1)]=sub
    return HttpResponse(json.dumps(context, ensure_ascii=False),content_type="application/json")

def student_load(request):
    data = json.loads(request.body.decode('utf-8'))
    context = {}
    print(data)
    lesson = Lesson.objects.get(id = data['lesson'])
    date = data['date']
    count = 0
    for i in Student.objects.filter():
        print(lesson)
        print(date)
        print(i)
        try:
            ison = Check.objects.get(lesson = lesson, date=date,student = i).ison
        except:
            ison = 0
        context[str(count)] = {'name' :i.firstname + " " + i.secondname,'ison':ison}
        count+=1

    

    return HttpResponse(json.dumps(context, ensure_ascii=False),content_type="application/json")
