from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Task
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
#from .models import
# Create your views here.
def home(request, *args, **kwargs):
	return render(request, 'home/index.html')

def login(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        check_email = User.objects.filter(email=email).exists()
        user = authenticate(request, username=email, password=password)
        
        if email =="":
            return render(request, 'home/login.html',{"msg1":"Fill the Email field"})

        if password =="":
            return render(request, 'home/login.html',{"msg1":"Fill the password field"})

        if check_email == False:
            return render(request, 'home/login.html',{"msg1":"The email does not exist in our database!"})

        if user is  None:
            return render(request, 'home/login.html',{"msg1":"Invalid Password!"})

        else:
            auth.login(request, user)			
            request.session['semail'] = email  
            return redirect('profile')
            
    else:
        return render(request, 'home/login.html')


def createAccount(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        middle_name = request.POST['middle_name']
        password = request.POST['password']
        rpt_password = request.POST['rpt_password']

        email_confirm = User.objects.filter(email=email).exists()

        if email =="" or first_name=="" or last_name=="" or email=="":
            messages.info(request, " All the fields are required")	
            return redirect('create-account')

        if rpt_password != password:
            messages.info(request, "The passwords did not match!")	
            return redirect('create-account')			

        if email_confirm :
            messages.info(request, "A user with that email aready exists")	
            return redirect('create-account')

        if len(password) < 4 or len(password) > 15:
            messages.info(request, "A Password should have 4-15 characters!")	
            return redirect('create-account')	

        else:
            user =User.objects.create_user(username=email,first_name=first_name,last_name=last_name,middle_name=middle_name,email=email, password=password)
            user.save()		
            messages.info(request, "Account created successfully, please login!")	
            return redirect('login')
    
    else:
        return render(request, 'home/create_account.html')


def profile(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']       
        id_number = request.POST['id_number']
        phone = request.POST['phone']

        if email =="" or first_name=="" or last_name=="" or email=="":
            messages.info(request, " All the fields are required")	
            return redirect('profile')	

        if len(id_number) != 8:
            messages.info(request, " A valid Id number should have 8 digits!")	
            return redirect('profile')	

        if len(phone) < 9 or len(phone) >13:
            messages.info(request, " A valid phone number should have 10 - 13 digits!")	
            return redirect('profile')	        

        else:
            entry = User.objects.get(email=request.user.email)
            entry.first_name = first_name
            entry.last_name = last_name	
            entry.middle_name = middle_name
            entry.email =email
            entry.phone = phone
            entry.id_number = id_number

            
            entry.save()
            messages.info(request, "Profile updated successfully.")	
            return redirect('profile')		
    
    else:
        user = User.objects.get(id=request.user.id)
        context = {
            'user':user,
        }
        return render(request, 'home/profile.html', context)


def tasks(request, *args, **kwargs):
    user = User.objects.get(email=request.user.email)
    tasks = Task.objects.filter(owner=user).order_by('-id')
    context = {
        'tasks':tasks,
    }
    return render(request, 'home/tasks.html', context)

def addTask(request, *args, **kwargs):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        status = request.POST['status']
        due_date = request.POST['due_date']       

        if title =="" or description=="" or status=="" or due_date=="":
            messages.info(request, " All the fields are required")	
            return redirect('add-task')	        

        else:
            user = User.objects.get(email=request.user.email)
            task =Task.objects.create(owner=user, title=title,description=description,status=status,due_date=due_date)
            task.save()	
            	
            messages.info(request, "Task added successfully")	
            return redirect('add-task')
    else:
        user = User.objects.get(email=request.user.email)
        tasks = Task.objects.order_by('-id').filter(owner=user)[:1]
        context = {
            'tasks':tasks,
        }
        return render(request, 'home/add_task.html', context)

def updateTask(request, str):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        status = request.POST['status']
        due_date = request.POST['due_date']       

        if title =="" or description=="" or status=="" or due_date=="":
            messages.info(request, " All the fields are required")	
            return redirect('tasks')	        

        else:
            user = User.objects.get(email=request.user.email)
            task =Task.objects.get(owner=user, id=str)
            task.title = title
            task.description = description
            task.status = status
            task.due_date = due_date
            task.save()	
            	
            messages.info(request, "Task added successfully")	
            return redirect('tasks')
    else:
        user = User.objects.get(email=request.user.email)
        task = Task.objects.get(owner=user, id=str)
        context = {
            'task':task,
        }
        return render(request, 'home/update_task.html', context)

def viewTask(request, str):
    user = User.objects.get(email=request.user.email)
    task = Task.objects.get(owner=user, id=str) 
    context = {
        'task':task,
    }  
    
    return render(request, 'home/view_task.html', context)

def deleteTask(request, str):
    user = User.objects.get(email=request.user.email)
    task = Task.objects.get(owner=user, id=str)   
    task.delete()
            	
    messages.info(request, "Task deleted successfully")	
    return redirect('tasks')
    