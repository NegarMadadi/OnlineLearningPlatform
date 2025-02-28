from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect
from .forms import CourseSelectionForm, LevelSelectionForm
from .models import PersonalizedLearningPath, Level
from CourseApp.models import Course  # Importing Course model from Course app
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


def login_required_message(message='You must be logged in to access this page.'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.info(request, message)
                return redirect('user_login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



@login_required_message('You need to log in to create a personalized learning path.')
def select_course(request):
    if request.method == 'POST':
        form = CourseSelectionForm(request.POST)
        if form.is_valid():
            request.session['course_id'] = form.cleaned_data['course'].id
            return redirect('select_level')
    else:
        form = CourseSelectionForm()
    return render(request, 'personalpath/select_course.html', {'form': form})

def select_level(request):
    from .models import Level   #Import the Level model

@login_required_message('You need to log in to create a personalized learning path.')
def select_level(request):
    if 'course_id' not in request.session:
        return redirect('select_course')
    
    if request.method == 'POST':
        form = LevelSelectionForm(request.POST)
        if form.is_valid():
            level_name = form.cleaned_data['level']  # Get the selected level name
            course_id = request.session['course_id']
            course = Course.objects.get(id=course_id)
            
            # Fetch the corresponding Level object based on the selected level name
            level = Level.objects.get(name=level_name)
            
            #PersonalizedLearningPath.objects.create(user=request.user, course=course, level=level)
            personalized_learning_path = PersonalizedLearningPath.objects.create(user=request.user, course=course, level=level)
            # Print statements for debugging
            print(f'User: {request.user}')
            print(f'Course: {course}')
            print(f'Level: {level}')
            print(f'PersonalizedLearningPath: {personalized_learning_path }')
            return redirect('view_learning_path', path_id=personalized_learning_path.id)
    else:
        form = LevelSelectionForm()
    return render(request, 'personalpath/select_level.html', {'form': form})


@login_required_message('You need to log in to create a personalized learning path.')
def view_learning_path(request,path_id):

    if 'course_id' not in request.session:
        return redirect('select_course')

    course_id = request.session['course_id']
    course = Course.objects.get(id=course_id)
    level_id = request.session.get('level_id')
    level = Level.objects.get(id=level_id) if level_id else None
    path = PersonalizedLearningPath.objects.get(id=path_id)
    #path = PersonalizedLearningPath.objects.filter(user=request.user, course=course, level=level).first()
    # Pass the username to the template context
    username = request.user.username
    print(f"Retrieved path in views is : {path}")
    return render(request, 'personalpath/view_learning_path.html', {'path': path , 'username': username})
