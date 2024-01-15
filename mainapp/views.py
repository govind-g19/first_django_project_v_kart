from django.shortcuts import render
from adminmanager.models import Category, Product, ProductImage
# from django.shortcuts import get_object_or_404
# from django.db.models import F

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
    return render(request, "main/product_details.html",)

# def product_details(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     variants = ProductVariant.objects.filter(product=product)
#     variant_images = VariantImage.objects.select_related('variant__color').filter(variant__product=product)
#     colors = ProductColor.objects.all()
#     rams = ProductRam.objects.all()

#     selected_color_id = request.GET.get('color')
#     selected_ram_id = request.GET.get('ram')

#     if selected_color_id:
#         variants = variants.filter(color_id=selected_color_id)
#         variant_images = variant_images.filter(variant__color_id=selected_color_id)

#     filtered_variants = variants

#     if selected_ram_id:
#         filtered_variants = variants.filter(ram_id=selected_ram_id)
#         # Retrieve the price attribute from the ProductRam model for the selected RAM
#         ram_price = ProductRam.objects.filter(pk=selected_ram_id).values_list('product_price', flat=True).first()
#         # Update the price of filtered_variants based on the selected RAM price
#         filtered_variants.update(price=ram_price)

#     context = {
#     'product': product,
#     'variants': filtered_variants,
#     'variant_images': variant_images,
#     'colors': colors,
#     'rams': rams,
#     'selected_color_id': int(selected_color_id) if selected_color_id else None,
#     'selected_ram_id': int(selected_ram_id) if selected_ram_id else None,
#     'selected_variant': filtered_variants.first() if filtered_variants.exists() else None,  # Select first variant after filter
# }
#     return render(request, "main/product_details.html", context)