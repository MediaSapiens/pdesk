from django.shortcuts import render



def index(request):
    return render(request, 'index.html')


def shop_productlist(request):
    return render(request, 'shop_productlist.html')


def shop_productlist2(request):
    return render(request, 'shop_productlist2.html')
    
    
def shop_productpage(request):
    return render(request, 'shop_productpage.html')
