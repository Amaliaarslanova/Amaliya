from django.shortcuts import render, redirect
from . import models
import requests

# Create your views here.
def index_page(request):
    #Если отправляет отзыв
    if request.method == 'POST':
        mail = request.POST.get('mail')
        feedback = request.POST.get('message')

        models.Feedback.objects.create(user_mail=mail, feedback_message=feedback)

    connect = requests.get(url='https://cbu.uz/ru/arkhiv-kursov-valyut/json/').json()
    products = models.Product.objects.all()
    categories = models.Category.objects.all()
    sales = models.Sale.objects.all()
    currency_rate = connect[0]['Rate']
    weather = '+32 C'

    return render(request, 'index.html',{'products': products,
                                         'categories': categories,
                                         'sales': sales})



# Функция поиска
def search_product(request):
    if request.method == 'POST':
        user_search_product = request.POST.get('search')
        try:
            result_product = models.Product.objecs.get(product_name=user_search_product)

            return render(request, 'current_product.html',{'result_product': result_product})

        except:
            return redirect('/')

#Получить определенный продукт
def current_product(request, name, pk):
    product = models.Product.objects.get(product_name=name, id=pk)

    return render (request, 'current_product.html', {'result_product': product})

#Получить все товары из конкретной категории
def get_current_category(request, pk):
    current_category = models.Category.objects.get(id=pk)

    products_from_category = models.Product.objects.filter(product_category=current_category)

    return render(request, 'current_category.html',
                  {'products_from_category': products_from_category})



#Добавление в корзину
def add_product_to_user_cart(request, pk):
    if request.method == 'POST':
        product = models.Product.objects.get(id=pk)
        product_count = float(request.POST.get('count'))

        user = models.Cart(user_id=request.user.id,
                           user_product=product,
                           product_quantity=product_count,
                           total_for_current_product=product_count*product.product_price)
        product.product_quantity -= product_count
        product.save()
        user.save()

        return redirect(f'/product/{product.product_name}/{pk}')
def show_cart(request):
    cart= models.Cart.objects.filter(user_id=request.user.id)
    return render(request,'cart.html',{'cart':cart})

#Удаление товара из корзины
def delete_product_from_cart(request,pk):
    if request.method == 'POST':
        product_to_delete = models.Cart.objects.get(id=pk,user_id=request.user.id)
        product = models.Product.objects.get(product_name=product_to_delete.user_product)
        product.product_quantity += product_to_delete.product_quantity



        product.save()
        product_to_delete.delete()

        return redirect('/cart')