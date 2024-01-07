from django.shortcuts import render
from adminmanager.models import Category, Product, ProductImage, ProductVariant,VariantImage,ProductColor, ProductRam
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request): 

    context={
        'product':Product.objects.all(),
        'category': Category.objects.all(),
        'product_img':ProductImage.objects.all(),
    }
    return render(request,'index.html',context)


def shop(request):  
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
    return render(request,'main/shop.html',context)



def base(request):
    return render(request, 'base.html')


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    variants = ProductVariant.objects.filter(product=product)
    variant_images = VariantImage.objects.filter(variant__product=product)
    colors = ProductColor.objects.all()
    rams = ProductRam.objects.all()

    selected_color_id = request.GET.get('color')
    selected_ram_id = request.GET.get('ram')

    if selected_color_id:
        variants = variants.filter(color_id=selected_color_id)
        variant_images = variant_images.filter(variant__color_id=selected_color_id)

    if selected_ram_id:
        variants = variants.filter(ram_id=selected_ram_id)
        variant_images = variant_images.filter(variant__ram_id=selected_ram_id)

    context = {
        'product': product,
        'variants': variants,
        'variant_images': variant_images,
        'colors': colors,
        'rams': rams,
        'selected_color_id': int(selected_color_id) if selected_color_id else None,
        'selected_ram_id': int(selected_ram_id) if selected_ram_id else None,
    }
    return render(request, "main/product_details.html", context)