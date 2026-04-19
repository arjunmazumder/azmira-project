import django_filters
from projects.models import Property

class PropertyFilter(django_filters.FilterSet):
    # প্রাইস রেঞ্জ ফিল্টার (Min এবং Max)
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    
    # সাইজ রেঞ্জ ফিল্টার
    min_size = django_filters.NumberFilter(field_name="size_sqft", lookup_expr='gte')
    max_size = django_filters.NumberFilter(field_name="size_sqft", lookup_expr='lte')

    # লোকেশন এবং টাইটেল দিয়ে আংশিক সার্চ
    location = django_filters.CharFilter(field_name="project__location", lookup_expr='icontains')
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Property
        fields = ['bedroom', 'bathroom', 'status', 'is_featured', 'has_parking', 'has_lift']