from django.shortcuts import render
from django.contrib.auth.views import *
from django.shortcuts import redirect
from mainapp.forms import *
from mainapp.models import *

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

def tables(request):
    return render(request,'AddTimetable.html')