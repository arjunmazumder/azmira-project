from rest_framework import serializers
from projects.models import (
    Project, Property,
    BlogPost, ClientReview,
    Message
)


# ১. লুপ এড়ানোর জন্য একটি বেসিক প্রজেক্ট সিরিয়ালাইজার
class SimpleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'location', 'status']


# ২. প্রপার্টি সিরিয়ালাইজার
class PropertySerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    # এখানে ProjectSerializer এর বদলে SimpleProjectSerializer ব্যবহার করুন
    project = SimpleProjectSerializer(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'unit_number', 'size_sqft', 
            'floor_level', 'price', 'status', 'is_featured', 'road', 
            'bedroom', 'bathroom', 'balcony', 'has_drawing_room', 
            'has_dining_room', 'has_kitchen', 'has_garden', 'has_hall', 
            'has_lift', 'has_parking', 'has_electricity_backup', 
            'image', 'created_at', 'project'
        ]

# ৩. মেইন প্রজেক্ট সিরিয়ালাইজার
class ProjectSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField()
    # এখানে আমরা PropertySerializer ব্যবহার করছি
    properties = PropertySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'developer_name', 'location', 'project_type', 
            'status', 'building_type', 'total_share', 'unit_per_floor', 
            'has_lift', 'has_rooftop_access', 'has_convention_hall', 
            'has_electricity_backup', 'total_units', 'land_area', 
            'handover_date', 'cover_image', 'created_at', 'properties'
        ]


class FeaturedPropertySerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField(source='project.name')
    class Meta:
        model = Property
        fields = ['id', 'title', 'project_name', 'price', 'size_sqft', 'is_featured', 'status']



class BlogPostSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField()

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'description',
            'comments',
            'cover_image',
            'is_published',
            'created_at'
        ]


class ClientReviewSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField()
    class Meta:
        model = ClientReview
        fields = [
            'id',
            'client_name',
            'review_text',
            'rating',
            'video',
            'cover_image',
            'is_published',
            'created_at'
        ]



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id',
            'name',
            'email',
            'phone_number',
            'subject',
            'message',
            'created_at'
        ]