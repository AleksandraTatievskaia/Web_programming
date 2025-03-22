from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import RegistrationForm
from .models import User
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Cart
from .models import Order
from .models import CartItem
from .models import OrderItem



# Функция для проверки роли администратора
def is_admin(user):
    return user.role == 'admin'


# Главная страница - просмотр книг
def book_list(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 5)  # отображаемые книги на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из URL
    page_obj = paginator.get_page(page_number)  # Берем объекты для текущей страницы
    return render(request, 'echo/book_list.html', {'page_obj': page_obj})


# Добавление книги - только для авторизованных пользователей
@login_required
def add_book(request):
    if request.method == 'POST':  # Когда форма отправлена
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем в БД
            return redirect('echo/book_list')
    else:
        form = BookForm()
    return render(request, 'echo/book_form.html', {'form': form})


# Редактирование книги - только для администраторов
@login_required
@user_passes_test(is_admin)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('echo/book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'echo/book_form.html', {'form': form})


# Удаление книги - только для администраторов
@login_required
@user_passes_test(is_admin)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('echo/book_list')


# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Хэшируем пароль перед сохранением
            user.set_password(form.cleaned_data['password'])
            user.save()  # Сохраняем пользователя в БД
            messages.success(request, "Вы успешно зарегистрированы!")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'echo/register.html', {'form': form})


# Авторизация пользователя
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # messages.success(request, "Вы успешно вошли!")
                return redirect('book_list')  # Перенаправляем на страницу списка книг
            else:
                messages.error(request, "Неверный логин или пароль.")
    else:
        form = LoginForm()
    return render(request, 'echo/login.html', {'form': form})

# Выход пользователя
def logout_view(request):
    logout(request)
    return redirect('book_list')  # Переадресуем на главную страницу

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'echo/profile.html', {'form': form})


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Если товар уже в корзине, увеличиваем количество, иначе создаём новый элемент
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)

    if not created:  # Если элемент уже существует, увеличиваем количество
        cart_item.quantity += 1
        cart_item.save()

    return HttpResponseRedirect(reverse('book_list'))


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('book')

    # Проверяем, есть ли товары в корзине
    if not cart_items.exists():
        total_price = 0
    else:
        total_price = sum(item.total_price() for item in cart_items)  # Вычисляем общую цену

    return render(request, 'echo/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        return redirect('cart')  # Перенаправляем, если корзина пуста

    total_price = sum(item.total_price() for item in cart_items)

    # Если форма отправлена (пользователь подтверждает заказ)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=total_price)
        order.save()

        for item in cart_items:
            OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity)

        # После оформления заказа очищаем корзину
        cart_items.delete()

        return redirect('orders')  # Перенаправляем на страницу с заказами

    return render(request, 'echo/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'echo/orders.html', {'orders': orders})


@login_required
def profile(request):
    """
    Личный кабинет пользователя, где отображаются его данные.
    """
    return render(request, 'echo/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваши данные успешно обновлены!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'echo/edit_profile.html', {'form': form})