from django.http import JsonResponse
from django.contrib.auth import authenticate, login, 
from ratelimit.decorators import ratelimit

@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)
def login_view(request):
    if request.user.is_anonymous:
        view = ratelimit(key='ip', rate='5/m', method='POST', block=True)(_login_inner)
        return view(request)
    else:
        return _login_inner(request)

def _login_inner(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'detail': 'Only POST allowed'}, status=405)
