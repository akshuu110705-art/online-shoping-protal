from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Avg
from django.core.paginator import Paginator
from .models import Product, Cart, CartItem, Order, OrderItem, Review, Wishlist

admin_required = user_passes_test(lambda u: u.is_staff, login_url='/login/')


def home(request):
    featured_products = Product.objects.all()[:6]
    return render(request, 'store/home.html', {'featured_products': featured_products})


def products(request):
    items = Product.objects.all()
    q = request.GET.get('q')
    category = request.GET.get('category')
    gender = request.GET.get('gender')
    if q:
        items = items.filter(name__icontains=q)
    if category:
        items = items.filter(category__icontains=category)
    if gender:
        items = items.filter(gender=gender)
    paginator = Paginator(items, 24)
    page = request.GET.get('page', 1)
    products_page = paginator.get_page(page)
    return render(request, 'store/products.html', {'products': products_page, 'total': items.count()})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    reviews = product.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    user_review = reviews.filter(user=request.user).first() if request.user.is_authenticated else None
    in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists() if request.user.is_authenticated else False
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'user_review': user_review,
        'in_wishlist': in_wishlist,
    })


# AUTH
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('home')
    return render(request, 'store/register.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# CART
@login_required(login_url='/login/')
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': cart.get_total()})


@login_required(login_url='/login/')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()
    return redirect('cart')


@login_required(login_url='/login/')
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    return redirect('cart')


@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')


# CHECKOUT
@login_required(login_url='/login/')
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    if not cart_items:
        return redirect('cart')
    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total': cart.get_total()})


@login_required(login_url='/login/')
def place_order(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        if not cart_items:
            return redirect('cart')
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode'],
            phone=request.POST['phone'],
            payment_method=request.POST['payment'],
            total=cart.get_total(),
        )
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            item.product.stock -= item.quantity
            item.product.save()
        cart_items.delete()
        return redirect('order_success', pk=order.id)
    return redirect('checkout')


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


@login_required(login_url='/login/')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required(login_url='/login/')
def buy_now(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity = quantity
        else:
            item.quantity = quantity
        item.save()
        return redirect('checkout')
    return redirect('products')


@login_required(login_url='/login/')
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'items': items})


@login_required(login_url='/login/')
def wishlist_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))


@login_required(login_url='/login/')
def order_tracking(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    steps = ['pending', 'processing', 'shipped', 'delivered']
    current = steps.index(order.status) if order.status in steps else 0
    return render(request, 'store/order_tracking.html', {'order': order, 'steps': steps, 'current': current})


@login_required(login_url='/login/')
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        if comment:
            Review.objects.update_or_create(
                product=product, user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
    return redirect('product_detail', pk=pk)


@login_required(login_url='/login/')
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        for item in order.orderitem_set.all():
            item.product.stock += item.quantity
            item.product.save()
    return redirect('order_history')


# ADMIN DASHBOARD
@admin_required
@login_required(login_url='/login/')
def admin_dashboard(request):
    context = {
        'total_orders': Order.objects.count(),
        'total_users': User.objects.count(),
        'total_products': Product.objects.count(),
        'total_sales': Order.objects.aggregate(s=Sum('total'))['s'] or 0,
        'recent_orders': Order.objects.order_by('-created_at')[:5],
    }
    return render(request, 'store/admin/dashboard.html', context)


@admin_required
@login_required(login_url='/login/')
def admin_products(request):
    products = Product.objects.all()
    return render(request, 'store/admin/products.html', {'products': products})


@admin_required
@login_required(login_url='/login/')
def admin_product_add(request):
    if request.method == 'POST':
        product = Product.objects.create(
            name=request.POST['name'],
            category=request.POST['category'],
            price=request.POST['price'],
            description=request.POST['description'],
            stock=request.POST['stock'],
        )
        if request.FILES.get('image'):
            product.image = request.FILES['image']
            product.save()
        return redirect('admin_products')
    return render(request, 'store/admin/product_form.html', {'action': 'Add'})


@admin_required
@login_required(login_url='/login/')
def admin_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.category = request.POST['category']
        product.price = request.POST['price']
        product.description = request.POST['description']
        product.stock = request.POST['stock']
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        return redirect('admin_products')
    return render(request, 'store/admin/product_form.html', {'action': 'Edit', 'product': product})


@admin_required
@login_required(login_url='/login/')
def admin_product_delete(request, pk):
    get_object_or_404(Product, pk=pk).delete()
    return redirect('admin_products')


@admin_required
@login_required(login_url='/login/')
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'store/admin/orders.html', {'orders': orders})


@admin_required
@login_required(login_url='/login/')
def admin_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/admin/order_detail.html', {'order': order})


@admin_required
@login_required(login_url='/login/')
def admin_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = request.POST['status']
        order.save()
    return redirect('admin_order_detail', pk=pk)


@admin_required
@login_required(login_url='/login/')
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'store/admin/users.html', {'users': users})


@admin_required
@login_required(login_url='/login/')
def admin_user_toggle(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        user.is_active = not user.is_active
        user.save()
    return redirect('admin_users')
