from rest_framework import serializers
from projects.models import (
    Project, Property,
    BlogPost, ClientReview
)



class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    # এই প্রজেক্টের আন্ডারে থাকা সব প্রপার্টি লিস্ট আকারে দেখাবে
    properties = PropertySerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'

class FeaturedPropertySerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = Property
        fields = ['id', 'title', 'project_name', 'price', 'size_sqft', 'is_featured', 'status']



class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'


class ClientReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientReview
        fields = '__all__'