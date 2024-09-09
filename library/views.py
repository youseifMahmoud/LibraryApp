from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author
from .forms import BookForm, AuthorForm , CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q  


def home(request):
    # Redirect to login if not authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Forms for adding books and authors
    if request.method == 'POST':
        book_form = BookForm(request.POST)
        author_form = AuthorForm(request.POST)
        
        if book_form.is_valid():
            book_form.save()
            return redirect('home')
        
        if author_form.is_valid():
            author_form.save()
            return redirect('home')
    else:
        book_form = BookForm()
        author_form = AuthorForm()

    # Handle search queries for books
    query_books = request.GET.get('q_books', '')
    if query_books:
        books = Book.objects.filter(Q(title__icontains=query_books))
    else:
        books = Book.objects.all()

    # Handle search queries for authors
    query_authors = request.GET.get('q_authors', '')
    if query_authors:
        authors = Author.objects.filter(Q(name__icontains=query_authors))
    else:
        authors = Author.objects.all()

    # Pass the required data to the template
    return render(request, 'library/home.html', {
        'username': request.user.username,  
        'book_form': book_form,
        'author_form': author_form,
        'books': books,
        'authors': authors,
        'query_books': query_books,
        'query_authors': query_authors,
    })

def client_page(request):
    # Check if the user is authenticated and not an admin
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')  # Redirect to login if not authenticated or an admin

    # Handle the search query for books
    query_books = request.GET.get('q_books', '')  

    if query_books:
        books = Book.objects.filter(Q(title__icontains=query_books))
    else:
        books = Book.objects.none()  # No books found if no query

    # Pass the username and other data to the template
    return render(request, 'library/client.html', {
        'username': request.user.username,  # Pass the user's username to the template
        'books': books,
        'query_books': query_books,  
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Set session to expire in 7 days
            request.session.set_expiry(7 * 24 * 60 * 60)  

            if user.is_staff:
                return redirect('home')  # Redirect to admin home
            else:
                return redirect('client_page')  # Redirect to client page
    else:
        form = AuthenticationForm()
    
    return render(request, 'library/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'admin':
                user.is_staff = True
            else:
                user.is_staff = False
            user.save()
            return redirect('login')  # Redirect to login after signup
    else:
        form = CustomUserCreationForm()  # Create a new form instance for GET requests

    return render(request, 'library/signup.html', {'form': form}) 

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('home')  # Redirect to admin home
            else:
                return redirect('client_page')  # Redirect to client page
    else:
        form = AuthenticationForm()
    return render(request, 'library/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to login after logout
    
def book_list(request):
    """
    Retrieves all books from the database and renders the book list page.

    Returns:
        book list page with a list of books.
    """
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def author_list(request):
    """
    Retrieves all authors from the database and renders the author list page.

    Returns:
        HttpResponse: The rendered author list page with a list of authors.
    """
    authors = Author.objects.all()
    return render(request, 'library/author_list.html', {'authors': authors})

def edit_book(request, pk):
    """
    To edit book and redirect to home after editing.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after successful edit
    else:
        form = BookForm(instance=book)
    return render(request, 'library/edit_book.html', {'form': form})

def delete_book(request, pk):
    """
    To deleting book and redirect to home after deleting.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('home')  # Redirect to the home page after deletion

    return render(request, 'library/delete_book.html', {'book': book})

def edit_author(request, pk):
    """
    To edit author and redirect to home after editing.
    """
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after saving changes
    else:
        form = AuthorForm(instance=author)
    return render(request, 'library/edit_author.html', {'form': form})

def delete_author(request, pk):
    """
    To deleting author and redirect to home after deleting.
    """
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        author.delete()
        return redirect('home')  # Redirect to the home page after deletion

    return render(request, 'library/delete_author.html', {'author': author})
