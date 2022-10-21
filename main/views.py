from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Brand, Category, Produit, Coupon, Ordersguest, Model, Mark
import json
import pandas as pd
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    categories= Category.objects.all()
    # brands=Brand.objects.all()
    # models=Model.objects.all()
    return render(request, 'main/home.html', {'categories':categories})


def about(request):
    return render(request, 'main/about.html')






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

# process the order
def guestorder(request):
    # get the data from the request
    data=request.POST.get('data')
    # convert the data to json
    data=json.loads(data)
    # create a new order
    order=Ordersguest(data['name'], data['phone'], data['email'], data['address'], data['city'])
    # save the order
    order.save()
    # get the products from the data
    products=data['products']
    # loop through the products
    for i in products:
        # get the product from the db
        pd=Produit.objects.filter(id=i['id']).first()
        # check if the product exist
        if pd:
            # check if the product is in stock
            if pd.stock>=i['quantity']:
                # add the product to the order
                order.products.add(pd)
                # update the stock
                pd.stock-=i['quantity']
                # save the product
                pd.save()
            else:
                # return a json response with value False
                return JsonResponse({
                    'valid':False
                })
        else:
            # return a json response with value False
            return JsonResponse({
                'valid':False
            })
    # return a json response with value True
    return JsonResponse({
        'valid':True
    })



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
        'data':render(request, 'main/calls.html', {'products':products}).content.decode('utf-8')
    })

@login_required
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

def addbulk(request, ctg):
    myfile = request.FILES['file']
    df = pd.read_excel(myfile)
    df = df.fillna('')
    for d in df.itertuples():
        Produit.objects.create(name=d.n,category=Category.objects.get(pk=ctg), price=round(d.pr, 2), brand=d.b, model=d.mo, mark=d.ma.lower(), ref=d.ref)
    return redirect(create)

