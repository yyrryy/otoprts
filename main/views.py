from unicodedata import name
from django.http import JsonResponse, response
from django.shortcuts import render
from .models import Categories, Produit, Coupon, Ordersguest
import json


# Create your views here.
def home(request):
    cts= Categories.objects.all()   
    return render(request, 'main/main.html', {'cc':cts})


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