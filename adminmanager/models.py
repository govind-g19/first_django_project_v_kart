from django.db import models

# Create your models here.

# Catagory
class Category(models.Model):
    category_name   = models.CharField( max_length=150,unique= True)
    soft_deleted    = models.BooleanField(default= False)
    category_details = models.TextField(null = True,blank = True)
    is_available   = models.BooleanField(default=True, blank=True,null=True)
    def __str__(self):
        return self.category_name
    

# Product
class Product(models.Model):
    product_name   = models.CharField(max_length=200, unique=True)
    product_images = models.ImageField(upload_to='images/products')
    category       = models.ForeignKey(Category, on_delete=models.CASCADE)
    description    = models.TextField(max_length=500, blank=True)
    price          = models.IntegerField()
    quantity       = models.IntegerField()
    create_date    = models.DateField(auto_now_add=True)
    modified_date  = models.DateField(auto_now=True)
    available      = models.BooleanField(default=True)
    soft_deleted   = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='photos/product', default='default_image.jpg')

    def __str__(self):
        return f"Image of {self.product.product_name}"
    

# class ProductColor(models.Model):
#     product_color   = models.CharField(max_length=50)

#     def __str__(self):
#         return self.product_color
    


# class ProductRam(models.Model):
#     product_ram   = models.CharField(max_length=50)
#     product_price = models.IntegerField(blank = True, null = True )
    
#     def __str__(self):
#         return self.product_ram
    


# class ProductRom(models.Model):
#     product_rom   = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.product_rom

# class ProductVariant(models.Model):
#     product   = models.ForeignKey(Product, on_delete=models.CASCADE)
#     color     = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
#     ram       = models.ForeignKey(ProductRam, on_delete=models.CASCADE)
#     rom       = models.ForeignKey(ProductRom, on_delete=models.CASCADE)

#     def __str__(self):
#        return f"{self.product.product_name} - Color: {self.color.product_color}, RAM: {self.ram.product_ram}, ROM: {self.rom.product_rom}"

# class VariantImage(models.Model):
#     variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='variant_images/')

#     def __str__(self):
#         return f"Image for {self.variant.product.product_name} ram: {self.variant.ram.product_ram}, color: {self.variant.color.product_color} Variant"
