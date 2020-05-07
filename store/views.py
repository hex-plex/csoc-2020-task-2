from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from datetime import date
# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': None, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE

    context['book']=get_object_or_404(Book,pk=bid)
    context['num_available']=len(BookCopy.objects.filter(book=context['book'],status=True))
    if request.user.is_authenticated:
        messages.info(request,context['book'].myRateing(str(request.user.username)))
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    # START YOUR CODE HERE
    q=Q()
    if 'title' in get_data.keys():
        if get_data['title']!='':
            q |=Q(title__iexact=get_data['title'])
        if get_data['author']!='':
            q |=Q(author__iexact=get_data['author'])
        if get_data['genre']!='':
            q |=Q(genre__iexact=get_data['genre'])
        context['books']=Book.objects.filter(q)
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    context['books']=BookCopy.objects.filter(borrower__exact=request.user)

    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    response_data = {
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    book_id = request.POST['bid'] # get the book id from post data
    if not request.user.is_authenticated:
        response_data['message']='Login to continue'
        return JsonResponse(response_data)
    book = BookCopy.objects.filter(book_id__exact=book_id,status__exact=True).first()
    if book:
        book.borrow_date=date.today()
        book.status=False
        book.borrower=request.user
        book.save()
        response_data['message']='success'
    else:
        response_data['message']='failure'

    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
'''
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def returnBookView(request):
    response_data = {
        'message': None,
    }
    book_id=request.POST['bid']
    try:
        book=BookCopy.objects.get(pk=book_id)
        book.status=True
        book.borrower=None
        book.borrow_date=None
        book.save()
        response_data['message']='Successfully Book returned.'
        return JsonResponse(response_data)

    except:
        response_data['message']='No such book_id found'
        return JsonResponse(response_data)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def ratingItView(request,bid):
    response_data = {
        'message': None,
    }
    book=Book.objects.get(pk=bid)
    ratinginp = request.POST["rating"]
    ind = book.checkUser(str(request.user))
    if ind==-1:
        book.updateRate(ratinginp,str(request.user))
    else:
        res=book.editRate(ratinginp,str(request.user),ind)
        if res==1:
            response_data['message']="Successfully updated Rating"
        else:
            response_data['message']="Something went wrong"
    return JsonResponse(response_data)
