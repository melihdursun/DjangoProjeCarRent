from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from home.models import UserProfile
from product.models import CommentForm, Comment, ReservationForm, Reservation, Product, Category


# Create your views here.
def index(request):
    return HttpResponse('Product Page')

@login_required(login_url='/login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user

            data = Comment()
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz")

            return HttpResponseRedirect(url)

    messages.warning(request, "Yorumunuz kaydedilmedi. Lütfen kontrol ediniz")
    return HttpResponse(url)


@login_required(login_url='/login')
def addreservation(request, id):
    current_user = request.user
    product = Product.objects.get(pk=id)
    form = ReservationForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    category = Category.objects.all()
    reservations = Reservation.objects.filter(user_id=current_user.id)
    context = {'product': product, 'form': form, 'profile': profile, 'category': category,
               'reservations': reservations}
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            current_user = request.user

            data = Reservation()
            data.user_id = current_user.id
            data.product_id = id
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.location = form.cleaned_data['location']
            data.address = form.cleaned_data['address']
            data.days = form.cleaned_data['days']
            data.checkin = form.cleaned_data['checkin']
            data.checkout = form.cleaned_data['checkout']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Rezervasyonunuz Başarıyla Alındı. Yetkililerimiz En Kısa Sürede Sizinle İletişime Geçecektir...')
            return HttpResponseRedirect('/user/bookings/')

    return render(request, 'myreservation.html',context)





