from django.shortcuts import render, get_object_or_404, redirect
from django.http import request
from .models import Book, Category, Profile
from .forms import BookForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, ProfileForm
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


def index(request):
    book_list = Book.objects.all()
    cat_list = Category.objects.all()
    return render(request, 'store/index.html', {'book_list': book_list, 'cat_list': cat_list})


def signup(request):
    error = ""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').lower()
            email = form.cleaned_data.get('email').lower()
            if not username_is_exist(username) and not email_is_exist(email):
                form.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                profile = Profile(user=user)
                profile.save()
                login(request, user)
                return redirect('home')
            elif username_is_exist(username) and email_is_exist(email):
                error = "نام کاربری و ایمیل قبلا استفاده شده است."
            elif not username_is_exist(username) and email_is_exist(email):
                error = "ایمیل وارد شده قبلا استفاده شده است."
            elif username_is_exist(username) and not email_is_exist(email):
                error = "نام کاربری وارد شده قبلا استفاده شده است."
    else:
        form = SignupForm()
    return render(request, 'store/signup.html', {'form': form, 'error': error})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'store/book_detail.html', {'book': book})


@login_required
def new_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.publish_date = timezone.now()
            book.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'store/edit_book.html', {'form': form, 'title': 'افزودن کتاب'})


@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.publish_date = timezone.now()
            book.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'store/edit_book.html', {'form': form, 'title': 'ویرایش کتاب'})


@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return render(request, 'store/delete_book.html', {})


def profile(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    return render(request, 'store/profile.html', {'profile': user_profile})


@login_required
def settings(request):
    user = get_object_or_404(User, username=request.user)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'store/settings.html', {'form': form})


def search(request):
    query = request.GET.get('q')
    return render(request, 'store/index.html', {'q': query})


class BookList(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'store/book_List.html'
    paginate_by = 30


def username_is_exist(username):
    if User.objects.filter(username=username).exists():
        return True
    else:
        return False


def email_is_exist(email):
    if User.objects.filter(email=email).exists():
        return True
    else:
        return False
