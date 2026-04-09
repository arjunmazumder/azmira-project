from django.apps import AppConfig

class ProductsConfig(AppConfig): # এখানে 'ProductdConfig' থাকলে 'ProductsConfig' করুন
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'  # এই লাইনটি খুব ভালো করে দেখুন, এখানে 'productd' আছে কি না। থাকলে 'products' করে দিন।