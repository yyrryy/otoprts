
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Brand, Category, Client, Order, Orderitem, Produit, Coupon, Model, Mark
import pandas as pd
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.
def home(request):
    ctx={
        'categories': Category.objects.all(),
        'brands':Brand.objects.all(),
        'models':Model.objects.all(),
        'clients':Client.objects.all()
    }
    
    return render(request, 'home.html', ctx)


def about(request):
    return render(request, 'about.html')



def loginpage(request):
    if request.method == 'POST':
        print('login proccess')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            group=user.groups.all().first().name
            if group == 'salsemen':
                return redirect(catalog)
            elif group=='client':
                return redirect(catalog)
            elif group == 'accounting':
                return redirect(orders)
        else:
            return redirect(loginpage)
    print('not post')
    return render(request, 'login.html')


def byref(request):
    
    ref=request.POST.get('ref')
    pds=Produit.objects.filter(ref=ref).first()
    if not(pds):
        return JsonResponse({
            'valid':False
        })
    pd={
        'valid':True,
        'id':pds.id,
        'name':pds.nom,
        'ref':pds.ref,
        'price':pds.prix,
        'stock':pds.stock,
        'mark':pds.marque,
        'country':pds.pays,
        'img':pds.image.url
    }

    return JsonResponse(pd, safe=False)


def bysach(request):
    
    chas=request.POST.get('chas')
    catg=request.POST.get('catg')
    pds=Produit.objects.filter(n_chasis=chas, Categorie=int(catg))
    res={'valid':True, 'pdcts':[]}
    if not(pds):
        res['valid']=False
        return JsonResponse(
            res, safe=False
        )
    artcls=[]
    for i in pds:
        pd={
            'id':i.id,
            'name':i.nom,
            'ref':i.ref,
            'price':i.prix,
            'stock':i.stock,
            'mark':i.marque,
            'country':i.pays,
            'img':i.image.url
        }
        artcls.append(pd)
    res['pdcts']=artcls
    return JsonResponse(res, safe=False)


def coupon(request):
    # get cupon from the request
    coupon=request.POST.get('coupon')
    print('coupon', coupon)
    # check if cupon exist in db
    cpn=Coupon.objects.filter(code=coupon).first()
    if not(cpn):
        # return a json response with value False
        return JsonResponse({
            'valid':False
        })
    # return a json response with value True
    return JsonResponse({
        'valid':True,
        'amount':cpn.amount
    })


# users groups
# chack if user's group in accounting
def isaccounting(user):
    return user.groups.filter(name='accounting').exists()

# chack if user's group in salsemen
def issalsemen(user):
    return user.groups.filter(name='salsemen').exists()










def filters(request):
    # calls.html will handle the data
    # get call from the request
    category=request.POST.get('category') or None
    brand=request.POST.get('brand') or None
    model=request.POST.get('model') or None
    mark=request.POST.get('mark') or None
    products=''
    # filter logic


    print(category, brand, model, mark)

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
    brands=Brand.objects.all()
    marks=Mark.objects.all()
    return render(request, 'create.html', {'categories':categories, 'brands':brands, 'marks':marks})


# add category ajax route
def addcategory(request):
    # get category from request
    category=request.POST.get('category')
    print(category)
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

def addbulkfltrair(request):
    myfile = request.FILES['file']
    df = pd.read_excel(myfile)
    df = df.fillna('')
    for d in df.itertuples():
        Produit.objects.create(name=d.n,category=Category.objects.get(pk=1), price=round(d.pr, 2), brand=d.b, model=d.mo, mark=d.ma, ref=d.ref)
    return redirect(create)

def addbulkfltrhuile(request):
    myfile = request.FILES['file']
    df = pd.read_excel(myfile)
    df = df.fillna('')
    for d in df.itertuples():
        Produit.objects.create(name=d.n,category=Category.objects.get(pk=2), price=round(d.pr, 2), brand=d.b, model=d.mo, mark=d.ma, ref=d.ref)
    return redirect(create)

def addbulkrlmnt(request):
    myfile = request.FILES['file']
    df = pd.read_excel(myfile)
    df = df.fillna('')
    for d in df.itertuples():
        Produit.objects.create(name=d.n,category=Category.objects.get(pk=3), price=round(d.pr, 2), brand=d.b, model=d.mo, mark=d.ma, ref=d.ref)
    return redirect(create)

def addbulkcroi(request):
    myfile = request.FILES['file']
    df = pd.read_excel(myfile)
    df = df.fillna('')
    for d in df.itertuples():
        Produit.objects.create(name=d.n,category=Category.objects.get(pk=4), price=round(d.pr, 2), brand=d.b, model=d.mo, mark=d.ma, ref=d.ref)
    return redirect(create)

def addbulkah(request):
    myfile = request.FILES['file']
    df = pd.read_excel(myfile)
    df = df.fillna('')
    for d in df.itertuples():
        Produit.objects.create(name=d.n,category=Category.objects.get(pk=5), price=round(d.pr, 2), brand=d.b, model=d.mo, mark=d.ma, ref=d.ref)
    return redirect(create)

@login_required(login_url='loginpage')
def addbulk(request, ctg):
    myfile = request.FILES['file']
    df = pd.read_excel(myfile)
    df = df.fillna('')
    for d in df.itertuples():
        Produit.objects.create(name=d.n.lower(),category=Category.objects.get(pk=ctg), price=round(d.pr, 2), brand=d.b, model=d.mo, mark=d.ma.lower(), ref=d.ref)
    return redirect(create)

@user_passes_test(issalsemen, login_url='loginpage')
@login_required(login_url='loginpage')
def commande(request):
    client=request.POST.get('client')
    total=request.POST.get('total')
    order=Order.objects.create(client=Client.objects.get(pk=client), salseman=request.user.username, total=total)
    commande=request.POST.getlist('commande[]')
    print(commande)
    for i in commande:
        ref, name, qty=i.split(':')
        Orderitem.objects.create(order=order, ref=ref, name=name, qty=int(qty))
    # return a json res
    return JsonResponse({
        'valid':True,
        'message':'Commande enregistrée avec succès'
    })



@user_passes_test(isaccounting, login_url='loginpage')
@login_required(login_url='loginpage')
def orders(request):
    # get orders from db and order them by date ascendant
    orders=Order.objects.all().filter(isdelivered=False).order_by('id')
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

@login_required(login_url='loginpage')
def dashboard(request):
    user=request.user
    print(user.groups.all().first())
    return render(request, 'dashboard.html')

@user_passes_test(issalsemen, login_url='loginpage')
@login_required(login_url='loginpage')
def catalog(request):
    ctx={
            'categories': Category.objects.all(),
            'brands':Brand.objects.all(),
            'models':Model.objects.all(),
            'clients':Client.objects.all(),
            'title':'Catalog'
        }
    return render(request, 'catalog.html', ctx)



@user_passes_test(issalsemen, login_url='loginpage')
@login_required(login_url='loginpage')
def salsemanorders(request):
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