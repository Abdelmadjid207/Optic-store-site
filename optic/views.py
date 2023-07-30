from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
from .forms import Signupform, addclientForm, addsellerForm, addproductForm
from .models import Client, Seller, Product, Brand, Category, Cart, ActionCounter, ClientCounter, SaleCounter
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
import matplotlib.pyplot as plt
from datetime import timedelta
from django.utils import timezone
import os
import urllib
import heapq


# Create your views here.

def home(request):
    client_n = Client.objects.count()
    product_n = Product.objects.count()
    product_f = Product.objects.filter(quantity='0')
    n_a_b = Brand.objects.filter(status=Brand.NADMIN).count()
    n_a_c = Category.objects.filter(status=Category.NADMIN).count()
    product_a = Product.objects.filter(status=Product.NADMIN)
    current_user = request.user
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error! Try again")
            return redirect('home')
    else:
        return render(request, 'home.html', {'client_n':client_n, 'product_n':product_n, 'product_f':product_f, 'current_user':current_user, 'n_a_b':n_a_b, 'n_a_c':n_a_c, 'product_a':product_a})

def chart(request):
    products = Product.objects.all()
    today = datetime.date.today() 
    current_month = today.month
    print(current_month)
    i=1
    j=0
    max_tuple = None
    largestsales = None
    stepcount = []
    if request.method == "POST":
        start = request.POST.get("start")
        produits = request.POST.get("produits")
        if produits == "0":
            while i <= 30:
                
                sales = 0
                stats = Cart.objects.filter(updated="{}-{}".format(start, i))
                count = stats.count()
                for j in stats:
                    sales = sales + j.price
                print(stats.first)
                print(sales)
                stepcount.append({
                    "label": "{}-{}".format(start, i),
                    "y": float(sales)
                })
                
                i = i + 1
            print(stepcount)
            saleint = 0
            sold = []
            w = 0
            largestsales = []
            for k in Product.objects.all():
                count = Cart.objects.filter(updated__startswith="{}".format(start), product=k).count()
                sold.append((int(count),str(k)))
                w = w + 1
            max_tuple = heapq.nlargest(5, sold, key=lambda x: x[0])
            for tuple in max_tuple:
                if int(tuple[0]) != 0:
                    largestsales.append(tuple[1])
                else:
                    largestsales.append("No other sold products this month")
        else:
            while i <= 30:
                
                sales = 0
                prod = Product.objects.get(name=produits)
                stats = Cart.objects.filter(updated="{}-{}".format(start, i), product=prod)
                count = stats.count()
                for j in stats:
                    sales = sales + j.price
                print(stats.first)
                print(sales)
                stepcount.append({
                    "label": "{}-{}".format(start, i),
                    "y": float(sales)
                })
                
                i = i + 1
            print(stepcount)
    else :
        produits = "0"
        today = timezone.now().strftime('%Y-%m')
        print(today)
        start = str(today)
        print(start)
        while i <= 30:
            
            sales = 0
            stats = Cart.objects.filter(updated="{}-{}".format(start, i))
            count = stats.count()
            for j in stats:
                sales = sales + j.price
            print(stats.first)
            print(sales)
            stepcount.append({
                "label": "{}-{}".format(start, i),
                "y": float(sales)
            })
            
            i = i + 1
        print(stepcount)
        saleint = 0
        sold = []
        w = 0
        largestsales = []
        for k in Product.objects.all():
            count = Cart.objects.filter(updated__startswith="{}".format(start), product=k).count()
            sold.append((int(count),str(k)))
            w = w + 1
        max_tuple = heapq.nlargest(5, sold, key=lambda x: x[0])
        for tuple in max_tuple:
            if int(tuple[0]) != 0:
                largestsales.append(tuple[1])
            else:
                largestsales.append("No other sold products this month")


    """j, created = ActionCounter.objects.get_or_create(date=timezone.now().date())
    i = j.id if created else j.pk
    ij = j.count
    ii = ActionCounter.objects.get( id = i-1 )
    iij = ii.count
    iii = ActionCounter.objects.get( id = i-2 )
    iiij = iii.count
    iv = ActionCounter.objects.get( id = i-3 )
    ivj = iv.count  
    v = ActionCounter.objects.get( id = i-4 )
    vj = v.count
    vi = ActionCounter.objects.get( id = i-5 )
    vij = vi.count
    vii = ActionCounter.objects.get( id = i-6 )
    viij = vii.count
    stepcount = [
        { "label":str(vii.date), "y": viij },

        { "label":str(vi.date), "y": vij },

        { "label":str(v.date), "y": vj },

        { "label":str(iv.date), "y": ivj },

        { "label":str(iii.date), "y": iiij },

        { "label":str(ii.date), "y": iij },

        { "label":str(j.date), "y": ij }
    ]"""
    u ,created = ClientCounter.objects.get_or_create(date=timezone.now().date())
    u_count = u.count
    u_id = u.id if created else u.pk
    uu = ClientCounter.objects.get( id = u_id-1 )
    uu_count = uu.count
    w ,created = SaleCounter.objects.get_or_create(date=timezone.now().date())
    w_count = w.count
    w_id = w.id if created else w.pk
    ww = SaleCounter.objects.get( id = w_id-1 )
    ww_count = ww.count
    return render(request, 'chart.html', {'stepcount':stepcount, 'w_count':w_count, 'ww_count':ww_count, 'u_count':u_count, 'uu_count':uu_count, 'products':products, 'current_month':current_month, 'max_tuple':max_tuple, 'largestsales':largestsales, 'produits':produits})

def checkadmin(request):
    users = User.objects.all().order_by('-date_joined')
    current_user = request.user
    print(current_user.id)
    if request.method == "POST":
        id_list = request.POST.getlist('box')
        
        users.update(is_superuser=False, is_staff=False)
        
        for user in id_list:
                User.objects.filter(id=int(user)).update(is_superuser=True, is_staff=True)             
        messages.success(request, "Admins updated")
        return redirect('checkadmin')        
    return render(request, 'checkadmin.html', {'users':users, 'current_user':current_user})
    


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = Signupform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered !")
            return redirect('home')
    else:
        form = Signupform()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})

def viewclient(request):
    clients = Client.objects.all().order_by('-added_at')
    return render(request, 'clients.html', {'clients':clients})

def one_client(request, pk):
    one_client = Client.objects.get(id=pk)
    return render(request, 'oneclient.html', {'one_client':one_client})

def delete_client(request, pk):
    delete_client = Client.objects.get(id=pk)
    delete_client.delete()
    today = timezone.now().date()
    tooday = datetime.date.today()
    if delete_client.added_at.day == tooday.day and delete_client.added_at.month == tooday.month and delete_client.added_at.year == tooday.year:
        action_counter, _ = ActionCounter.objects.get_or_create(date=today)
        client_counter, _ = ClientCounter.objects.get_or_create(date=today)
        if action_counter.count > 0:
            action_counter.decrease_count()
        if client_counter.count > 0:
            client_counter.decrease_count()
    messages.success(request, "Client deleted successfully ")
    return redirect('clients')


def add_client (request):
    form = addclientForm(request.POST or None)
    current_user = request.user
    if request.method == "POST":        
        if form.is_valid():
            addaclient = form.save()
            Client.objects.filter(id=addaclient.id).update(added_by=current_user.username)
            today = timezone.now().date()
            action_counter, _ = ActionCounter.objects.get_or_create(date=today)
            action_counter.increase_count()
            client_counter, _ = ClientCounter.objects.get_or_create(date=today)
            client_counter.increase_count()            
            messages.success(request, "Client added successfully ")
            return redirect('clients')
    return render(request, 'add_client.html', {'form':form})

def edit_client(request, pk):
    current_client = Client.objects.get(id=pk)
    current_user = request.user
    form = addclientForm(request.POST or None, instance=current_client)
    Client.last_update = datetime.datetime.now
    if form.is_valid():
        edit = form.save()
        Client.objects.filter(id=edit.id).update(edited_by=current_user.username)
        messages.success(request, "Client's infos are updated successfully ")
        return redirect('clients')
    return render(request, 'edit_client.html', {'form':form, 'current_client':current_client})

def search_client(request):
    if request.method == "POST":
        searchbar = request.POST['searchbar']
        s_resultf = Client.objects.filter(first_name__contains=searchbar)
        s_resultl = Client.objects.filter(last_name__contains=searchbar)
        return render(request, 'search_client.html', {'searchbar':searchbar, 's_resultf':s_resultf, 's_resultl':s_resultl})
    else:
        return render(request, 'search_client.html', {})
    
    
def search_client_date(request):
    if request.method == "POST":
        day = request.POST['day']
        s_add_d = Client.objects.filter(added_at__contains=day)#, added_at__month=month, added_at__year=year)
        return render(request, 'search_client_date.html', {'day':day, 's_add_d':s_add_d})
    else:
        return render(request, 'search_client_date.html', {})

def search_client_date2(request):
    if request.method == "POST":
        dayd = request.POST['dayd']
        s_upd_d = Client.objects.filter(last_update__contains=dayd)#, added_at__month=month, added_at__year=year)
        return render(request, 'search_client_date2.html', {'dayd':dayd, 's_upd_d':s_upd_d})
    else:
        return render(request, 'search_client_date2.html', {})
        

def viewseller(request):
    sellers = Seller.objects.all()
    return render(request, 'sellers.html', {'sellers':sellers})

def one_seller(request, pk):
    one_seller = Seller.objects.get(id=pk)
    return render(request, 'oneseller.html', {'one_seller':one_seller})

def delete_seller(request, pk):
    delete_seller = Seller.objects.get(id=pk)
    today = timezone.now().date()
    tooday = datetime.date.today()
    action_counter, _ = ActionCounter.objects.get_or_create(date=today)
    if delete_seller.added.day == tooday.day and delete_seller.added.month == tooday.month and delete_seller.added.year == tooday.year:
        if action_counter.count > 0:
            action_counter.decrease_count()
    delete_seller.delete()
    messages.success(request, "seller deleted successfully ")
    return redirect('sellers')


def add_seller (request):
    form = addsellerForm(request.POST or None)
    current_user = request.user
    if request.method == "POST":         
        if form.is_valid():
            addaseller = form.save()
            Seller.objects.filter(id=addaseller.id).update(added_by=current_user.username)
            today = timezone.now().date()
            action_counter, _ = ActionCounter.objects.get_or_create(date=today)
            action_counter.increase_count()
            messages.success(request, "seller added successfully ")
            return redirect('sellers')
    return render(request, 'add_seller.html', {'form':form})

def edit_seller(request, pk):
    current_seller = Seller.objects.get(id=pk)
    form = addsellerForm(request.POST or None, instance=current_seller)
    if form.is_valid():
        form.save()
        messages.success(request, "seller's infos are updated successfully ")
        return redirect('sellers')
    return render(request, 'edit_seller.html', {'form':form, 'current_seller':current_seller})

def search_seller(request):
    if request.method == "POST":
        searchbar = request.POST['searchbar']
        ss_resultf = Seller.objects.filter(first_sname__contains=searchbar)
        ss_resultl = Seller.objects.filter(last_sname__contains=searchbar)
        return render(request, 'search_seller.html', {'searchbar':searchbar, 'ss_resultf':ss_resultf, 'ss_resultl':ss_resultl})
    else:
        return render(request, 'search_seller.html', {})
    
    

def viewproduct(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all().order_by('name')
    return render(request, 'products.html', {'products':products, 'brands':brands, 'categories':categories})

def one_product(request, pk):
    one_product = Product.objects.get(id=pk)
    return render(request, 'oneproduct.html', {'one_product':one_product})

def delete_product(request, pk):
    delete_product = Product.objects.get(id=pk)
    today = timezone.now().date()
    tooday = datetime.date.today()
    action_counter, _ = ActionCounter.objects.get_or_create(date=today)
    print(delete_product.seller)
    if delete_product.added.day == tooday.day and delete_product.added.month == tooday.month and delete_product.added.year == tooday.year:
        if action_counter.count > 0:
            action_counter.decrease_count()
    delete_product.delete()
    messages.success(request, "product deleted successfully ")
    return redirect('products')

def approve_product(request, pk):
    approve_product = Product.objects.filter(id=pk).update(status=Product.ADMIN)
    messages.success(request, "product approved successfully ")
    return redirect('products')


def add_product (request):
    form = addproductForm(request.POST or None)
    current_user = request.user
    if request.method == "POST":
        name = request.POST['name'] 
        barcode = request.POST['barcode']       
        if form.is_valid():
            check = Product.objects.filter(name=name).exists() or Product.objects.filter(barcode=barcode).exists()
            if check:
                messages.success(request, "product already exists! use a different name or barcode")
                return redirect('add_product')
            else:
                addaproduct = form.save()
                Product.objects.filter(id=addaproduct.id).update(added_by=current_user.username)
                if current_user.is_superuser:
                    Product.objects.filter(id=addaproduct.id).update(status=Product.ADMIN)
                else:
                    Product.objects.filter(id=addaproduct.id).update(status=Product.NADMIN)
                today = timezone.now().date()
                action_counter, _ = ActionCounter.objects.get_or_create(date=today)
                action_counter.increase_count()
                messages.success(request, "product added successfully ")
                return redirect('products')
    return render(request, 'add_product.html', {'form':form})

def edit_product(request, pk):
    current_product = Product.objects.get(id=pk)
    form = addproductForm(request.POST or None, instance=current_product)
    if form.is_valid():
        form.save()
        messages.success(request, "product's infos are updated successfully ")
        return redirect('products')
    return render(request, 'edit_product.html', {'form':form, 'current_product':current_product})

def search_product(request):
    if request.method == "POST":
        searchbar = request.POST['searchbar']
        s_resultf = Product.objects.filter(name__contains=searchbar)
        return render(request, 'search_product.html', {'searchbar':searchbar, 's_resultf':s_resultf})
    else:
        return render(request, 'search_product.html', {})

def search_product_bc(request):
    if request.method == "POST":
        searchbc = request.POST['searchbc']
        s_result = Product.objects.filter(barcode=searchbc)
        return render(request, 'search_product_bc.html', {'searchbc':searchbc, 's_result':s_result})
    else:
        return render(request, 'search_product_bc.html', {})
    
    
def filter_product_br(request):
    if request.method == "POST":
        filt = request.POST[str('filt')]
        print(filt)
        filt_res = Brand.objects.get(name=filt)
        filt_res = Product.objects.filter(brand=filt_res)
        return render(request, 'filter_product_br.html', {'filt':filt, 'filt_res':filt_res})
    else:
        return render(request, 'filter_product_br.html', {})
    
    
def filter_product_c(request):
    if request.method == "POST":
        categ = request.POST[str('categ')]
        print(categ)
        categ_res = Category.objects.get(name=categ)
        categ_res = Product.objects.filter(category=categ_res)
        return render(request, 'filter_product_c.html', {'categ':categ, 'categ_res':categ_res})
    else:
        return render(request, 'filter_product_c.html', {})
    
    
def cart(request, pk):
    client = Client.objects.get(id=pk)
    products = Product.objects.all()
    tooday = datetime.date.today()
    if request.method == "POST":
        
        if request.POST.get("delete"):
            delete = request.POST.get("delete")
            cart = Cart.objects.get(id=delete)
            pr = Product.objects.get(name=cart.product)
            a = float(pr.quantity) + float(cart.i_quantity)
            Product.objects.filter(name=cart.product).update(quantity=a)
            today = timezone.now().date()
            if cart.updated == tooday:
                action_counter, _ = ActionCounter.objects.get_or_create(date=today)
                i = 0
                if action_counter.count > 0:
                    action_counter.decrease_count()
            cart.delete()
        elif request.POST.get("newcart"):
            prod = request.POST.get("prod")
            prodn = request.POST.get("prodn")
            prodd = request.POST.get("prodd")
            if len(prod) > 1 and prodn == "0":
                try:
                    prodq = request.POST.get("prodq")
                    s_prod = Product.objects.get(barcode=prod)
                    if int(s_prod.quantity) > 0 and int(s_prod.quantity) >= int(prodq):
                        p = float(s_prod.price)*float(prodq)
                        client.cart_set.create(client=client, product=s_prod, desc=prodd, i_quantity=prodq, updated=datetime.date.today(), price=p)
                        a = float(s_prod.quantity) - float(prodq)
                        Product.objects.filter(barcode=prod).update(quantity=a) 
                    else:
                        s_prod = None
                        messages.success(request, "Product ran out! or there isn't enough. Click on previous page arrow")
                        return render(request, 'cart.html', {'client':client}) 
                except:
                    s_prod = None
                    messages.success(request, "Wrong Barcode or Quantity isn't specified. Click on previous page arrow")
                    return render(request, 'cart.html', {'client':client})
            elif prodn != "0":
                try:
                    prodq = request.POST.get("prodq")
                    s_prod = Product.objects.get(name=prodn)
                    if int(s_prod.quantity) > 0 and int(s_prod.quantity) >= int(prodq):
                        p = float(s_prod.price)*float(prodq)
                        client.cart_set.create(client=client, product=s_prod, desc=prodd, i_quantity=prodq, updated=datetime.date.today(), price=p)
                        a = float(s_prod.quantity) - float(prodq)
                        Product.objects.filter(name=prodn).update(quantity=a) 
                        today = timezone.now().date()
                        action_counter, _ = ActionCounter.objects.get_or_create(date=today)
                        action_counter.increase_count()
                        i = 0
                    else:
                        s_prod = None
                        messages.success(request, "Product ran out! or there isn't enough. Click on previous page arrow")
                        return render(request, 'cart.html', {'client':client}) 
                except:
                    s_prod = None
                    messages.success(request, "Wrong Barcode or Quantity isn't specified. Click on previous page arrow")
                    return render(request, 'cart.html', {'client':client})
                #items = Cart.objects.filter(client=client)
    return render(request, 'cart.html', {'client':client, 'products':products})

def checkout(request, pk):
    
    client = Client.objects.get(id=pk)
    c_price=0
    """cart = Cart.objects.get(client=client)
    if request.method == "POST":"""
    for item in client.cart_set.all():
        product = item.product
        c_quantity = int(item.i_quantity)
        c_price =  c_price + (item.product.price * c_quantity)
    sale=0    
    for i in Cart.objects.filter(updated=datetime.date.today()):
        print(i.updated)
        
        sale = sale + float(i.price)
        print(i.price)
    print(sale)
    
    SaleCounter.objects.get_or_create(date=timezone.now().date())
    try:
        SaleCounter.objects.filter(date=timezone.now().date()).update(count=sale)
    except:
        SaleCounter.objects.filter(date=timezone.now().date()).update(count=0)
    return render(request, 'checkout.html', {'cart':cart, 'client':client, 'c_price':c_price})

def checkout_pdf(request, pk):
    client = Client.objects.get(id=pk)
    current_user = request.user
    c_price=0
    for item in client.cart_set.all():
        product = item.product
        c_quantity = int(item.i_quantity)
        c_price =  c_price + (item.product.price * c_quantity)
        """item = CheckoutItems.objects.create(checkout=checkout, product=product, i_price=i_price, i_quantity=i_quantity)"""   
    return render(request, 'checkout_pdf.html', {'cart':cart, 'client':client, 'c_price':c_price, 'current_user':current_user})
        
        
def brand(request):
    brands = Brand.objects.all().order_by('name')
    current_user = request.user
    if request.method == "POST":
        if request.POST.get("delete"):
            delete = request.POST.get("delete")
            brand = Brand.objects.get(id=delete)
            brand.delete()
            messages.success(request, "Brand deleted")
        elif request.POST.get("approve"):
            approved = request.POST.get("approve")
            Brand.objects.filter(id=approved).update(status=Brand.ADMIN)
            messages.success(request, "Brand approved")
        elif request.POST.get("newbrand"):
            b = request.POST.get("brand")
            check = Brand.objects.filter(name=b).exists()
            if check:
                messages.success(request, "Brand already exists")
                return redirect('brand')
            else:
                if current_user.is_superuser == True:
                    Brand.objects.create(name=b, status=Brand.ADMIN)
                else:
                    Brand.objects.create(name=b, status=Brand.NADMIN)
                messages.success(request, "Brand added")
    return render(request, 'brand.html', {'brands':brands})

def category(request):
    categories = Category.objects.all()
    current_user = request.user
    if request.method == "POST":
        
        if request.POST.get("delete"):
            delete = request.POST.get("delete")
            category = Category.objects.get(id=delete)
            category.delete()
            messages.success(request, "Category deleted")
        elif request.POST.get("approve"):
            approved = request.POST.get("approve")
            Category.objects.filter(id=approved).update(status=Category.ADMIN)
            messages.success(request, "Brand approved")
        elif request.POST.get("newcategory"):
            c = request.POST.get("category")
            check = Category.objects.filter(name=c).exists()
            if check:
                messages.success(request, "Category already exists")
                return redirect('category')
            else:
                if len(c) > 2:
                    if current_user.is_superuser == True:
                        Category.objects.create(name=c, status=Category.ADMIN)
                    else:
                        Category.objects.create(name=c, status=Category.NADMIN)
                messages.success(request, "Category added")
    return render(request, 'category.html', {'categories':categories})


def pdf_report_create(request, pk):
    client = Client.objects.get(id=pk)
    client.cart_set.all
    current_user = request.user
    c_price=0
    
    for item in client.cart_set.all():
        product = item.product
        c_quantity = int(item.i_quantity)
        c_price =  c_price + (item.product.price * c_quantity)

    template_path = 'checkout_pdf.html'

    context = {'client': client, 'c_price':c_price, 'current_user':current_user}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="checkout.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response