
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Brand, Category, Client, Order, Orderitem, Produit, Coupon, Model, Mark
import pandas as pd
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
import json
from django.db.models import OuterRef, Exists, Count
import threading
# import csrf_exampt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# users groups
# chack if user's group in accounting
def isaccounting(user):
    return user.groups.filter(name='accounting').exists()

# chack if user's group in salsemen
def issalsemen(user):
    return user.groups.filter(name='salsemen').exists()

def isclient(user):
    return user.groups.filter(name='clients').exists()

def tocatalog(user):
    return (user.groups.filter(name='salsemen').exists() or user.groups.filter(name='clients').exists())
# Create your views here.
def home(request):
    # print(request.user)
    # print(request.user.groups.first())
    # if request.user.groups.first():
    #     if (request.user.groups.first().name=='salsemen'):
    #         return redirect(catalog)
    #     if (request.user.groups.first().name=='accounting'):
    #         return redirect(orders)
    #     if (request.user.groups.first().name=='admin'):
    #         return redirect(orders)
    # return redirect(loginpage)
    return render(request, 'main.html')


def about(request):
    return render(request, 'about.html')
def partners(request):
    return render(request, 'marques.html')

def profile(request):
    return render(request, 'profile.html')

def loginpage(request):
    print(request.user.groups.all())
    if request.user.groups.all():
        if (request.user.groups.first().name=='salsemen'):
            return redirect(catalog)
        if (request.user.groups.first().name=='accounting'):
            return redirect(orders)
        if (request.user.groups.first().name=='admin'):
            return redirect(orders)
        if (request.user.groups.first().name=='clients'):
            return redirect(catalog)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print('user', user)
        if user is not None:
            login(request, user)
            group=user.groups.all().first().name
            if group == 'salsemen':
                return redirect(catalog)
            elif group=='clients':
                return redirect(catalog)
            elif group == 'accounting':
                return redirect(orders)
        else:
            return redirect(loginpage)
    return render(request, 'login.html')


@csrf_exempt
def editinfoclient(request):
    client=Client.objects.get(user_id=request.user.id)
    print(client.name)
    client.name=request.POST.get('name').strip()
    client.phone=request.POST.get('phone').strip()
    client.address=request.POST.get('address').strip()
    client.city=request.POST.get('city').strip()
    client.save()
    return redirect(profile)

@login_required(login_url='/login')
@csrf_exempt
def updatepassword(request):
    user=User.objects.get(pk=request.user.id)
    print(request.user.id)
    user.set_password(request.POST.get('cpass'))
    user.save()
    login(request, user)
    return redirect(profile)






def filters(request):
    # calls.html will handle the data
    # get call from the request
    category=request.POST.get('category') or None
    brand=request.POST.get('brand') or None
    model=request.POST.get('model') or None
    mark=request.POST.get('mark') or None
    products=''
    # filter logic



    if category and brand and model and mark:
        # get the products from the db
        products=Produit.objects.filter(category=category, brand=brand, model=model, mark=mark)
    elif category and brand:
        # get the products from the db
        products=Produit.objects.filter(category=category, brand=brand)
    elif category and model:
        # get the products from the db
        products=Produit.objects.filter(category=category, model=model)
    elif category and mark:
        products=Produit.objects.filter(category=category, mark=mark)

    elif brand and model:
        # get the products from the db
        products=Produit.objects.filter(brand=brand, model=model)
    elif brand and mark:
        products=Produit.objects.filter(brand=brand, mark=mark)
    elif model and mark:
        products=Produit.objects.filter(model=model, mark=mark)
    elif category:
        # get the products from the db
        products=Produit.objects.filter(category=category)
    elif brand:
        # get the products from the db
        products=Produit.objects.filter(brand=brand)
    elif model:
        # get the products from the db
        products=Produit.objects.filter(model=model)
    elif mark:
        products=Produit.objects.filter(mark=mark)
    return JsonResponse({
        'data':render(request, 'calls.html', {'products':products}).content.decode('utf-8')
    })

@user_passes_test(isaccounting, login_url='loginpage')
@login_required(login_url='loginpage')
def create(request):
    # get category from db
    categories=Category.objects.all()
    # get brand from db
    return render(request, 'create.html', {'categories':categories, })


# add category ajax route
def addcategory(request):
    # get category from request
    category=request.POST.get('category')
    Category(title=category).save()
    return redirect(create)

def addbrand(request):
    # get category from request
    brand=request.POST.get('brand')
    print(brand)
    Brand(name=brand).save()
    return redirect(create)

def addmark(request):
    # get category from request
    mark=request.POST.get('mark')
    print(mark)
    Mark(name=mark).save()
    return redirect(create)

@login_required(login_url='loginpage')
def addbulk(request, ctg):
    myfile = request.FILES['file']
    df = pd.read_excel(myfile)
    df = df.fillna('')
    for d in df.itertuples():
        print(d)
        Produit.objects.create(name=d.n.lower(),category=Category.objects.get(pk=ctg), price=round(d.pr, 2), ref=str(d.ref).lower(), min=d.min, offre=d.offre, image=d.image)
    return redirect(create)

@user_passes_test(tocatalog, login_url='loginpage')
@login_required(login_url='loginpage')
def commande(request):
    client=request.POST.get('client')
    total=request.POST.get('total') 
    modpymnt=request.POST.get('modpymnt')
    modlvrsn=request.POST.get('modlvrsn')
    order=Order.objects.create(client=Client.objects.get(pk=client), salseman=request.user.username, total=total, modpymnt=modpymnt, modlvrsn=modlvrsn)
    commande=request.POST.getlist('commande[]')
    for i in commande:
        ref, name, qty=i.split(':')
        Orderitem.objects.create(order=order, ref=ref, name=name, qty=int(qty))
    # return a json res
    
    # send_mail(message='Nouveau commande.', subject=f'Nouveau commande. #{order.id}')
    #threading.Thread(target=send_mail, args=('Nouveau commande.', f'Nouveau commande. #{order.id}', 'abdelwahedaitali@gmail.com', ['aitaliabdelwahed@gmail.com'], False)).start()
    return JsonResponse({
        'valid':True,
        'message':'Commande enregistrée avec succès'
    })





@user_passes_test(isaccounting, login_url='loginpage')
@login_required(login_url='loginpage')
def orders(request):
    # get orders from db and order them by date ascendant
    orders=Order.objects.all().filter(isdelivered=False).order_by('date')
    delivered=Order.objects.all().filter(isdelivered=True)

    return render(request, 'orders.html', {'orders':orders, 'delivered':delivered, 'title':'Commandes'})


def orderitems(request, id):
    orderitems=Orderitem.objects.filter(order=id)
    order=Order.objects.get(pk=id)
    return JsonResponse({
        'data':render(request, 'orderitems.html', {'orderitems':orderitems, 'order':order}).content.decode('utf-8')
    })


def dilevered(request, id):
    order=Order.objects.get(pk=id)
    order.isdelivered=True
    order.save()
    return redirect(orders)


# gets products after clicking on a category
def products(request, id):
    # get the products from the db
    c=Category.objects.get(pk=id)
    products=Produit.objects.filter(category=id)
    return render(request, 'products.html', {'products':products, 'title':'Produits de '+str(c), 'category':c})


@login_required(login_url='loginpage')
def dashboard(request):
    user=request.user
    print(user.groups.all().first())
    return render(request, 'dashboard.html')

@user_passes_test(tocatalog, login_url='loginpage')
@login_required(login_url='loginpage')
def catalog(request):
    categories = Category.objects.annotate(
        has_promotion=Exists(Produit.objects.filter(category_id=OuterRef('pk'), offre__istartswith='|')),
        total_products=Count('produit')
    )
    ctx={
            'categories': Category.objects.all(),
            'brands':Brand.objects.all(),
            'models':Model.objects.all(),
            'clients':Client.objects.all(),
            'title':'Catalog',
            'cc':categories,
        }
    return render(request, 'catalog.html', ctx)



@user_passes_test(tocatalog, login_url='loginpage')
@login_required(login_url='loginpage')
def salsemanorders(request):
    print(request.user)
    orders=Order.objects.filter(salseman=request.user.username)
    return render(request, 'salsemanorders.html', {'orders':orders})




def clients(request):
    clients=Client.objects.all()
    # Convert the QuerySet to a list of dictionaries
    data = list(clients.values())

    # Serialize the list as JSON
    json_data = json.dumps(data)
    # return a json response with clients as clients
    return JsonResponse({
        'clients':json_data
    })


def addclient(request):
    name=request.POST.get('name')
    phone=request.POST.get('phone')
    address=request.POST.get('address')
    city=request.POST.get('city')
    Client.objects.create(name=name, phone=phone, address=address, city=city)
    return JsonResponse({
        'valid':True,
        'message':'Client ajouté avec succès'
    })

def logoutuser(request):
    logout(request)
    return redirect(loginpage)


def aboutus(request):
    return render(request, 'aboutus.html', {'title':'A propos de nous'})

def create_product(request):
    name = request.POST.get('name')
    price = request.POST.get('price')
    offre=request.POST.get('offre')
    min=request.POST.get('min')
    ref=request.POST.get('ref')
    category=request.POST.get('category')
    print(name, price, offre, min, ref, category)
    # Create the product object
    product = Produit(name=name, price=price
    , offre=offre, min=min, ref=ref, category=Category.objects.get(pk=category))


    product.save()
    return redirect('create')

@user_passes_test(tocatalog, login_url='loginpage')
def cart(request):
    return render(request, 'cart.html', {'title':'Panier'})

def me(request):
    return render(request, 'me.html', {'title':'Develper - abdelwahed ait ali'})


