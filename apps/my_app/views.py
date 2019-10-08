from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
        return render(request, "my_app/login_reg.html")
def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password_hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user= User.objects.create(
            name=request.POST['name'],
            alias=request.POST['alias'],
            email=request.POST['email'],
            password=password_hashed
        )
        request.session['user_id']=user.id
        return redirect('/home')
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user= User.objects.get(email=request.POST['loginemail'])
        if user:
            if bcrypt.checkpw(request.POST['loginpassword'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                # messages.success(request, 'You have successfully logged in.')
                return redirect('/home')
            else: 
                messages.error(request, "Invalid, please try again")
                return redirect('/')
        else: 
            print("Bad info")
            return redirect('/')
            
def homepage(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in first!!")
        return redirect('/')
    else: 
        one_user = User.objects.get(id= request.session['user_id'])

        reviews = Review.objects.all().order_by('-id')[:6]
        # recent three reviews
        context = {
            "this_user": one_user,
            "reviews": reviews,
            "books": Book.objects.all()
        }
        # needs to make three recent books out
        
        return render(request, "my_app/home.html", context)

def add_books_reviews(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in first!!")
        return redirect('/')
    else:
        if request.method=="GET":
            return render(request, "my_app/add.html")

        if request.method=="POST":
            errors = Book.objects.book_validator(request.POST)
            if len(errors) >0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/books/add')
            else:
                user = User.objects.get(id=request.session['user_id'])
                new_book = Book.objects.create(
                    title = request.POST['title'],
                    publish_date = request.POST['date'],
                    author = request.POST['new_author'],
                    creator = user,
                )
                request.session['new_book']= new_book.id

                review_for_new_book = Review.objects.create(
                    content = request.POST['review'],
                    rating = int(request.POST['rating']),
                    books = new_book,
                    reviewer = user,
                )
                return redirect(f'/books/{new_book.id}')


def view_review(request, b_id):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in first!!")
        return redirect('/')
    else:
        book= Book.objects.get(id=b_id)
        context = {
           "book": book,
           "reviews": Review.objects.filter(books=book),
        }
        return render(request, "my_app/view.html", context)

def add_more_review(request, b_id):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in first!!")
        return redirect('/')
    else:
        errors = Book.objects.review_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/books/{b_id}')
        else:
            user = User.objects.get(id=request.session['user_id'])
            book = Book.objects.get(id=b_id)

            new_review = Review.objects.create(
                content = request.POST['review'],
                rating = int(request.POST['rating']),
                reviewer = user,
                books = book,
            )
            return redirect(f'/books/{b_id}')

def user_info(request, u_id):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in first!!")
        return redirect('/')
    else:
        user = User.objects.get(id=u_id)
        all_reviews = user.reviews
        context = {
            "user": user,
            "reviews": user.reviews,
            "books": Book.objects.all(),
        }
        # needs to get only the book titles and no repeated book titles
        return render(request,"my_app/user.html", context)

def delete_reviews(request, b_id, r_id):
    reviews_to_delete= Review.objects.get(id=r_id)
    reviews_to_delete.delete()
    return redirect(f'/books/{b_id}')

def logout(request):
    request.session.clear()
    messages.success(request, 'You have successfully logged out.')
    return redirect('/')


# overall, needs to refactor and clean up codes