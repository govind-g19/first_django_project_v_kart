from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout 
from django.contrib.auth.models import User
from .models import Category, Product, ProductImage
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control, never_cache
from django.contrib.auth.decorators import login_required
from django.http import Http404

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# Create your views here.
def admin_loogin(request):
      if request.method == "POST":
        uname = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(username=uname, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, "Logged in successfully as admin")
            return redirect('/adminmanager/admin-index')


      return render(request, 'admin/admin-login.html')

@never_cache
@login_required
def admin_logout(request):
   logout(request)
   messages.success(request,"Log in to enjoy more")
   return redirect('/adminmanager/admin-login')

@login_required
def admin_index(request):
    return render(request,'admin/admin-index.html')


@login_required
def admin_user_list (request):
        user = User.objects.filter(is_superuser=False).order_by('id')
        return render (request, 'admin/admin-user.html',{"user":user})

@login_required
def block_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return redirect('/adminmanager/admin-user')
    user.is_active = False
    user.save()
    return redirect('/adminmanager/admin-user')  

@login_required
def unblock_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return redirect('/adminmanager/admin-user')
    user.is_active = True
    user.save()
    return redirect('/adminmanager/admin-user')

# category
@login_required
def Category_List(request):
    context={
        'cat': Category.objects.all()
    }
    return render(request,'admin/category_list.html',context)

@login_required
def Edit_Cat(request, id):
    cat = get_object_or_404(Category, pk=id)

    if request.method == 'POST':
        cat.category_name = request.POST.get('category_name')
        cat.category_details = request.POST.get('category_details')  # Updated variable name
        
        cat.save()

        return redirect('/adminmanager/category')

    context = {
        'cat': cat
    }
    return render(request, 'admin/edit_category.html', context)


@login_required
def add_category(request):
    if request.method == 'POST':
        name    = request.POST.get('category_name')
        details = request.POST.get('category_details')  # Corrected field name
        
        if not name:
            messages.error(request, "Category name is required.")
            return render(request, 'admin/add_category.html')

        try:
            existing_category = Category.objects.get(category_name=name)
            messages.warning(request, "Category already exists.")
            return render(request, 'admin/add_category.html')
        except Category.DoesNotExist:
            # Category with the same name does not exist; proceed to create
            pass

        try:
            new_cat = Category.objects.create(
                category_name    = name,
                category_details = details,
                is_available     = True
            )
            messages.success(request, "Category added successfully.")
            return redirect('/adminmanager/category')
        except Exception as e:
            messages.error(request, f"Error occurred while adding category: {str(e)}")
            return render(request, 'admin/add_category.html')

    return render(request, 'admin/add_category.html')

@login_required
def soft_delete_category(request, id):
    try:
        cat = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        return redirect('/adminmanager/category')

    # Soft delete logic
    if cat.soft_deleted:  # If already soft deleted, revert the changes
        cat.soft_deleted = False
        cat.is_available = True
    else:  # If not soft deleted, perform soft delete
        cat.soft_deleted = True
        cat.is_available = False

    cat.save()
    return redirect('/adminmanager/category')


@login_required
def undo_soft_delete_category(request, id):
    try:
        cat = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        return redirect('/adminmanager/category')

    # Undo the soft delete by setting soft_deleted to False and availability to True
    cat.soft_deleted = False
    cat.is_available = True

    cat.save()
    return redirect('/adminmanager/category')



#product 
@login_required
def Product_list(request):
    categories = Category.objects.all()
    products   = Product.objects.all()  # Initially fetch all products

    selected_category_id = request.GET.get('category_id')  # Get selected category ID from query parameters

    if selected_category_id:
        # Filter products based on the selected category
        products = Product.objects.filter(category__id=selected_category_id)

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, "admin/product_list.html", context)

@login_required
def Add_Product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_images = request.FILES.getlist('product_images') 
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        # Check if all required fields are provided
        if not all([product_name, category_id, description, price, quantity]):
            messages.error(request, "Please provide all required fields.")
            return redirect('/adminmanager/add_product')

        try:
            price     = float(price)
            quantity  = int(quantity)
            if price <= 0 or quantity <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Price and quantity must be positive numbers.")
            return redirect('/adminmanager/add_product')

        # Check if a product with the same name already exists
        if Product.objects.filter(product_name=product_name).exists():
            messages.error(request, f"A product with the name '{product_name}' already exists.")
            return redirect('/adminmanager/add_product')

        try:
            category = Category.objects.get(pk=category_id)
            product = Product.objects.create(
                product_name=product_name,
                category=category,
                description=description,
                price=price,
                quantity=quantity,
                available=True  # Set the default availability to True when adding a product
            )

            # Save product images
            for image in product_images:
                ProductImage.objects.create(product=product, image=image)

            return redirect('/adminmanager/product_list')
        except Category.DoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('/adminmanager/add_product')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('/adminmanager/add_product')

    categories = Category.objects.all().order_by('id')
    context = {'categories': categories}
    return render(request, 'admin/add_product.html', context)


@login_required
def Edit_Product(request, id):
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return redirect('/adminmanager/product_list')
    categories = Category.objects.all().order_by('id')

    if request.method == 'POST':
        product.product_name  = request.POST.get('product_name')
        category_id           = request.POST.get('category')
        description           = request.POST.get('description')
        price                 = request.POST.get('price')
        quantity              = request.POST.get('quantity')

        if not (product.product_name and category_id and price and quantity):
            messages.error(request, "Please provide all required fields.")
            return redirect(f'/adminmanager/edit_product/{id}/')


        try:
            price     = float(price)
            quantity  = int(quantity)
            if price  <= 0 or quantity <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Price and quantity must be positive numbers.")
            return redirect(f'/adminmanager/edit_product/{id}/')


        if Product.objects.filter(product_name=product.product_name).exclude(pk=id).exists():
            messages.error(request, f"A product with the name '{product.product_name}' already exists.")
            return redirect(f'/adminmanager/edit_product/{id}/')


        category = Category.objects.get(pk=category_id)

        product.category    = category
        product.description = description
        product.price       = price
        product.quantity    = quantity
        product.save()

        images = request.FILES.getlist('product_images')
        if images:
            product.images.all().delete()

            for image in images:
                ProductImage.objects.create(product=product, image=image)

        return redirect('/adminmanager/product_list')

    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'admin/edit_product.html', context)


@login_required
def soft_delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.soft_deleted = True
    product.available    = False
    product.save()
    return redirect('/adminmanager/product_list')

@login_required
def undo_soft_delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.soft_deleted = False
    product.available    = True
    product.save()
    return redirect('/adminmanager/product_list')

