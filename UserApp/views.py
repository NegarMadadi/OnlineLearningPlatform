from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

from CourseApp.models import Course, Enrollment

 
# Create your views here.

def home(request):
    return render (request , 'home.html')

def user_login(request):
    pass

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def user_register(request):
    pass



def search_courses(request):
    pass

@login_required
def course_detail(request):
    pass

def course_list(request):
    pass


@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'UserApp/dashboard.html', {'enrollments': enrollments})

@login_required
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        # Enrollment was created
        return redirect('user_dashboard')
    else:
        # User was already enrolled
        return redirect('user_dashboard')






