from _threading_local import local

from django.shortcuts import render,get_object_or_404,redirect
from django.http import request
from .models import Book,Category
from .forms import BookForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import generic
def index(request):
    book_list = Book.objects.all()
    cat_list = Category.objects.all()
    return render(request,'store/index.html',{'book_list':book_list,'cat_list':cat_list})

def book_detail(request,pk):
    book = get_object_or_404(Book,pk=pk)
    return render(request,'store/book_detail.html',{'book':book})

@login_required
def new_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.publish_date = timezone.now()
            book.save()
            return redirect('book_detail',pk=book.pk)
    else:
        form = BookForm()
    return render(request,'store/edit_book.html',{'form':form})

@login_required
def edit_book(request,pk):
    book = get_object_or_404(Book,pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST,instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.publish_date = timezone.now()
            book.save()
            return redirect('book_detail',pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request,'store/edit_book.html',{'form':form})
@login_required
def delete_book(request,pk):
    book = get_object_or_404(Book,pk=pk)
    book.delete()
    return render(request,'store/delete_book.html',{})

class BookList(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'store/book_List.html'
    paginate_by = 30
