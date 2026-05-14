from django.shortcuts import render
from django.db.models import Q
from services.models import ServiceCategory
from users.models import ProfessionalProfile


def index(request):
    categories = ServiceCategory.objects.filter(is_active=True, parent__isnull=True).order_by('order')[:8]
    professionals = ProfessionalProfile.objects.filter(status='active').select_related('user').order_by('-rating')[:6]

    context = {
        'categories': categories,
        'professionals': professionals,
    }
    return render(request, 'core/index.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    categories = ServiceCategory.objects.filter(is_active=True)
    professionals = ProfessionalProfile.objects.filter(status='active').select_related('user').order_by('-rating')

    if query:
        categories = categories.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        professionals = professionals.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(bio__icontains=query) |
            Q(city__icontains=query)
        )

    if category:
        categories = categories.filter(slug=category)
        professionals = professionals.filter(
            services__category__slug=category
        ).distinct()

    context = {
        'query': query,
        'categories': categories,
        'professionals': professionals,
        'total_results': categories.count() + professionals.count(),
    }
    return render(request, 'core/search_results.html', context)


def login_view(request):
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login, get_user_model
        from django.shortcuts import redirect

        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'core/login.html', {'error': 'E-mail ou senha incorretos.'})

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:index')
        else:
            return render(request, 'core/login.html', {'error': 'E-mail ou senha incorretos.'})

    return render(request, 'core/login.html')


def register_view(request):
    if request.method == 'POST':
        from django.contrib.auth import get_user_model
        User = get_user_model()

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        whatsapp = request.POST.get('whatsapp', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = []
        if not first_name or not last_name:
            errors.append('Nome e sobrenome são obrigatórios.')
        if not email:
            errors.append('E-mail é obrigatório.')
        if not whatsapp:
            errors.append('Telefone é obrigatório.')
        if password1 != password2:
            errors.append('As senhas não coincidem.')
        if len(password1) < 6:
            errors.append('A senha deve ter pelo menos 6 caracteres.')
        if User.objects.filter(email=email).exists():
            errors.append('Este e-mail já está cadastrado.')

        if errors:
            return render(request, 'core/register.html', {'errors': errors})

        username = email.split('@')[0] + '_' + str(User.objects.count() + 1)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            whatsapp=whatsapp,
            user_type='client'
        )

        from django.contrib.auth import login
        login(request, user)

        from django.shortcuts import redirect
        return redirect('core:index')

    return render(request, 'core/register.html')


def logout_view(request):
    from django.contrib.auth import logout
    from django.shortcuts import redirect
    logout(request)
    return redirect('core:index')


def custom_service_view(request):
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('core:login')

    if request.method == 'POST':
        from services.models import ServiceRequest

        service_type = request.POST.get('type', '')
        service_name = request.POST.get('service_name', '').strip()
        description = request.POST.get('description', '').strip()
        category_name = request.POST.get('category_name', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        budget = request.POST.get('budget', '').strip()

        errors = []
        if not service_type:
            errors.append('Selecione se você quer contratar ou oferecer o serviço.')
        if not service_name:
            errors.append('Nome do serviço é obrigatório.')
        if not description:
            errors.append('Descrição é obrigatória.')

        if errors:
            return render(request, 'core/custom_service.html', {'errors': errors})

        ServiceRequest.objects.create(
            client=request.user,
            title=service_name,
            description=f"{description}\n\nCategoria: {category_name or 'Não especificada'}\nOrçamento: {budget or 'Não informado'}",
            city=city,
            state=state,
            is_custom=True,
            status='pending'
        )

        return render(request, 'core/custom_service.html', {
            'success': True,
            'service_type': service_type
        })

    return render(request, 'core/custom_service.html')
