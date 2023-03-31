from django.shortcuts import render

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Username: {username}")
        print(f"Password: {password}")
    return render(request, 'login.html')
