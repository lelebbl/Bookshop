from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product, Category
from cart.forms import CartAddProductForm
from .forms import ReviewForm, CategoryForm, ProductForm
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
import calendar


def popular_list(request):
    products = Product.objects.filter(available=True)[:3]
    return render(request,
                  'main/index/index.html',
                  {'products':products})


def product_detail(request, slug):
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm
    reviews = product.reviews.all()
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                return redirect('main:product_detail', slug=slug)
        else:
            return redirect('users:login')
    else:
        review_form = ReviewForm()

    return render(request,
                  'main/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                    'reviews': reviews,
                    'review_form': review_form,
                   })


def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    paginator = Paginator(products, 10)
    current_page = paginator.page(int(page))
    if category_slug:
        category = get_object_or_404(Category,
                                     slug = category_slug)
        paginator = Paginator(products.filter(category=category), 10)
        current_page = paginator.page(int(page))
    return render(request,
                  'main/product/list.html',
                  {'category': category,
                  'categories': categories,
                  'products': current_page,
                  'slug_url': category_slug})


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@user_passes_test(is_admin)
def admin_panel(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    now_local = timezone.localtime()
    formatted_date_local = now_local.strftime("%d/%m/%Y")
    cal = calendar.TextCalendar().formatmonth(now_local.year, now_local.month)

    return render(request, 'main/admin_panel.html', {
        'categories': categories,
        'products': products,
        'current_date': formatted_date_local,
        'calendar_text': cal,
    })

def staff_dashboard(request):
    if request.user.role != 'staff':
        return render(request, '403.html') 
    return render(request, 'users/staff_dashboard.html')

# CATEGORY CRUD
@user_passes_test(is_admin)
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('main:admin_panel')
    return render(request, 'main/form.html', {'form': form, 'title': 'Создать категорию'})

@user_passes_test(is_admin)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('main:admin_panel')
    return render(request, 'main/form.html', {'form': form, 'title': 'Редактировать категорию'})

@user_passes_test(is_admin)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('main:admin_panel')

# PRODUCT CRUD
@user_passes_test(is_admin)
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('main:admin_panel')
    return render(request, 'main/form.html', {'form': form, 'title': 'Создать товар'})

@user_passes_test(is_admin)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('main:admin_panel')
    return render(request, 'main/form.html', {'form': form, 'title': 'Редактировать товар'})

@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('main:admin_panel')



