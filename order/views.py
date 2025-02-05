from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

# Create your views here.

from  order.models import ShopCartForm, ShopCart
from product.models import Category

def index(request):
    return HttpResponse("Order App")


@login_required(login_url='/login')
def addtocart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request,  "Ürün başarı ile sepete eklenmiştir. Teşekkür ederiz.")
        return HttpResponseRedirect(url)

    messages.warning(request, "Ürün Sepete eklemede hata oluştu!. Lütfen kontrol ediniz ")
    return HttpResponseRedirect(url)



@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in schopcart:
        total += rs.product.price * rs.quantity

    context = {'schopcart': schopcart,
               'category': category,
               'total': total,
               }
    return render(request, 'Shopcart_products.html', context)

@login_required(login_url='/login')
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Ürün Sepetten Silinmiştir.")
    return HttpResponseRedirect("/shopcart")