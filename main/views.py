
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import Brand, Category, Client, Order, Orderitem, Produit, Coupon, Model, Mark
import pandas as pd
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
import json
from django.db.models import OuterRef, Exists, Count
import uuid
# import csrf_exampt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.db.models import Q

def product(request, id):
    product=Produit.objects.get(pk=id)
    return render(request, 'product.html', {'product':product})


def searchref(request):
    ref=request.POST.get('ref')
    print(ref)
    products = Produit.objects.filter(Q(ref__icontains=ref) | Q(name__icontains=ref))
    for i in products:
        print(i.ref)
        print(i.name)
        print(i.price)
    return JsonResponse({
        'data':render(request, 'searchref.html', {'products':products}).content.decode('utf-8')
    })

# users groups
# chack if user's group in accounting
def isaccounting(user):
    return (user.groups.filter(name='accounting').exists() or user.groups.filter(name='admin').exists() )

# chack if user's group in salsemen
def issalsemen(user):
    return user.groups.filter(name='salsemen').exists()

def isclient(user):
    return user.groups.filter(name='clients').exists()

def tocatalog(user):
    return (user.groups.filter(name='salsemen').exists() or user.groups.filter(name='clients').exists() or user.groups.filter(name='admin').exists() )

def bothsalseaccount(user):
    return (user.groups.filter(name='salsemen').exists() or user.groups.filter(name='accounting').exists() or user.groups.filter(name='admin').exists() )

def isadmin(user):
    return user.groups.filter(name='admin').exists()


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

@user_passes_test(isadmin, login_url='loginpage')
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
        Produit.objects.create(ref=str(d.ref).lower(), name=d.n.lower(),category_id=ctg, price=round(d.pr, 2), isoffer=d.isoffer, min=d.min, offre=d.offer, image=d.image, mark_id=d.mark)
    return redirect(create)

@user_passes_test(tocatalog, login_url='loginpage')
@login_required(login_url='loginpage')
def commande(request):
    clientname=request.POST.get('clientname')
    clientaddress=request.POST.get('clientaddress')
    clientphone=request.POST.get('clientphone')
    total=request.POST.get('total') 
    modpymnt=request.POST.get('modpymnt')
    modlvrsn=request.POST.get('modlvrsn')
    totalremise=request.POST.get('totalremise', 0)
    order=Order.objects.create(clientname=clientname, clientaddress=clientaddress, clientphone=clientphone, salseman=request.user.username, total=total, modpymnt=modpymnt, modlvrsn=modlvrsn, totalremise=totalremise, code=str(uuid.uuid4()))
    commande=request.POST.getlist('commande[]')
    for i in commande:
        ref, name, qty=i.split(':')
        Orderitem.objects.create(order=order, ref=ref, name=name, qty=int(qty))
    # return a json res
    
    # send_mail(message='Nouveau commande.', subject=f'Nouveau commande. #{order.id}')
    #threading.Thread(target=send_mail, args=('Nouveau commande.', f'Nouveau commande. #{order.id}', 'abdelwahedaitali@gmail.com', ['aitaliabdelwahed@gmail.com'], False)).start()
    return JsonResponse({
        'valid':True,
        'message':'Commande enregistrée avec succès',
        'id':order.code
    })





@user_passes_test(isaccounting, login_url='loginpage')
@login_required(login_url='loginpage')
def orders(request):
    # get orders from db and order them by date ascendant
    orders=Order.objects.all()
    delivered=len(Order.objects.all().filter(isdelivered=True))

    return render(request, 'orders.html', {'orders':orders, 'delivered':delivered, 'title':'Commandes', 'notdel':len(orders)-delivered})


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
@user_passes_test(tocatalog, login_url='loginpage')
@login_required(login_url='loginpage')
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



@user_passes_test(bothsalseaccount, login_url='loginpage')
@login_required(login_url='loginpage')
def salsemanorders(request, str_id):
    orders=Order.objects.get(code=str_id)
    items=Orderitem.objects.filter(order=orders.id)
    return render(request, 'salsemanorders.html', {'order':orders, 'items':items, 'title':'Commande #'+str(orders.id)})




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

# def signup(request):
#     if request.method == 'POST':
#         name=request.POST.get('name')
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         usename=request.POST.get('usename')
        
#         return redirect('loginpage')


def sitemap(request):
    # Get the base URL for the sitemap
    host_base = request.build_absolute_uri(reverse("home"))

    # Static routes with static content
    static_urls = []
    for url in ["aboutus", "#contactus", "partners", "catalog"]:
        static_urls.append({"loc": f"{host_base}{url}"})

    # Render the sitemap template
    context = {"static_urls": static_urls}
    sitemap_xml = render(request, "sitemap.xml", context, content_type="application/xml")

    # Return the sitemap as an HTTP response with the appropriate content type
    return HttpResponse(sitemap_xml, content_type="application/xml")