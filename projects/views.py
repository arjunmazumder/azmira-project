from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from projects.filters import PropertyFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from core.response import success_response, error_response
from projects.models import (
    Project, Property, ClientReview,
    Message,
    
)

from projects.serializers import(
    ProjectSerializer, PropertySerializer, FeaturedPropertySerializer,
    BlogPostSerializer, ClientReviewSerializer,MessageSerializer
) 

#-----------list, retrieve and create all project-------------------

# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all().order_by('-created_at')
#     serializer_class = ProjectSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return success_response("Projects retrieved successfully", serializer.data)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return success_response("Project details retrieved successfully", serializer.data)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return success_response("Project created successfully", serializer.data, status_code=status.HTTP_201_CREATED)
#         return error_response("Project creation failed", serializer.errors)


# ১. সব প্রজেক্টের লিস্ট পাওয়ার জন্য আলাদা ভিউ
class ProjectListView(APIView):
    def get(self, request):
        projects = Project.objects.all().order_by('-created_at')
        total_count = projects.count()  # মোট প্রজেক্টের সংখ্যা বের করা
        serializer = ProjectSerializer(projects, many=True)
        
        # ডাটা এবং টোটাল কাউন্টকে একটি ডিকশনারিতে সাজানো
        response_data = {
            "total_projects": total_count,
            "projects": serializer.data
        }
        
        return success_response("All projects retrieved successfully", response_data)

#get all properties
class PropertyListView(APIView):
    def get(self, request):
        # ডাটাবেজ থেকে সব প্রপার্টি নেওয়া
        properties = Property.objects.all().order_by('-id')
        total_count = properties.count() # মোট প্রপার্টির সংখ্যা
        
        serializer = PropertySerializer(properties, many=True)
        
        # রেসপন্স ডেটা সাজানো
        response_data = {
            "total_properties": total_count,
            "properties": serializer.data
        }
        
        return success_response("All properties retrieved successfully", response_data)
    
# ২. টাইপ অনুযায়ী প্রজেক্ট পাওয়ার জন্য আলাদা ভিউ
class ProjectByTypeView(APIView):
    def get(self, request):
        project_type = request.query_params.get('project_type')

        if project_type:
            projects = Project.objects.filter(project_type=project_type)
        else:
            projects = Project.objects.all()

        serializer = ProjectSerializer(projects, many=True)
        return success_response("Projects fetched", serializer.data)

# Name base search

class ProjectSearchByNameView(APIView):
    def get(self, request):
        # query param থেকে project_name নেওয়া
        project_name = request.query_params.get('project_name', '').strip()

        # নামের আংশিক মিল চেক
        if project_name:
            projects = Project.objects.filter(name__icontains=project_name).order_by('-created_at')
        else:
            projects = Project.objects.all().order_by('-created_at')

        if projects.exists():
            serializer = ProjectSerializer(projects, many=True)
            return  success_response("successful !!", serializer.data)

        return success_response("No projects found", serializer.data)

class ProjectByLocationView(APIView):
    def get(self, request):
        location_param = request.query_params.get('location', '')
        location_text = location_param.replace('-', ' ')

        projects = Project.objects.filter(location__icontains=location_text)
        total_count = projects.count()

        serializer = ProjectSerializer(projects, many=True)

        return success_response(
            "Projects by location",
            {
                "count": total_count,
                "results": serializer.data
            }
        )


# class PropertyViewSet(viewsets.ModelViewSet):
#     queryset = Property.objects.all().order_by('-created_at')
#     serializer_class = PropertySerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return success_response("Properties retrieved successfully", serializer.data)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return success_response("Property details retrieved successfully", serializer.data)

#     # কাস্টম ফিচার্ড এপিআই এন্ডপয়েন্ট
#     @action(detail=False, methods=['get'])
#     def featured(self, request):
#         featured_list = Property.objects.filter(is_featured=True)
#         serializer = FeaturedPropertySerializer(featured_list, many=True)
#         return success_response("Featured properties retrieved successfully", serializer.data)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return success_response("Property created successfully", serializer.data, status_code=status.HTTP_201_CREATED)
#         return error_response("Property creation failed", serializer.errors)
    
class FeaturedPropertyListView(APIView):
    def get(self, request):
        featured_properties = Property.objects.filter(is_featured=True).order_by('-created_at')
        serializer = FeaturedPropertySerializer(featured_properties, many=True)
        return success_response("Featured properties retrieved successfully", serializer.data)
    
class LatestBlogPostCreateView(APIView):
    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                "Blog post created successfully",
                serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return error_response("Failed to create blog post", serializer.errors)
    
class ClientReviewCreateView(APIView):
    # permission_classes = [IsAdminUser]  # Only admin can post reviews

    def post(self, request):
        serializer = ClientReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Client review created successfully", serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response("Failed to create review", serializer.errors)

class ClientReviewListView(APIView):
    # Anyone can view published reviews
    def get(self, request):
        reviews = ClientReview.objects.filter(is_published=True).order_by('-created_at')
        serializer = ClientReviewSerializer(reviews, many=True)
        return success_response("Client reviews retrieved successfully", serializer.data)
    
class MessageCreateView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                "Message sent successfully",
                serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return error_response("Failed to send message", serializer.errors)
    
# GET: admin-only endpoint to view all messages
class MessageListAdminView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        messages = Message.objects.all().order_by('-created_at')
        serializer = MessageSerializer(messages, many=True)
        return success_response("All messages retrieved successfully", serializer.data)
    


class ProjectViewSet(viewsets.ModelViewSet):
    # ডাটাবেজ অপ্টিমাইজেশন: এক কোয়েরিতেই সব প্রপার্টি ডাটা নিয়ে আসবে (N+1 Problem Fix)
    queryset = Project.objects.all().prefetch_related('properties').order_by('-created_at')
    serializer_class = ProjectSerializer
    
    # ফিল্টার, সার্চ এবং অর্ডারিং কনফিগারেশন
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    search_fields = [
        'name', 'location', 'developer_name', 'project_type', 'status',
        'properties__title', 'properties__unit_number', 'properties__road'
    ]

    # ১. লিস্ট ভিউ (সব প্রজেক্ট)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # প্যাগিনেশন চেক
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(f"Successfully retrieved {queryset.count()} projects", serializer.data)

    # ২. নির্দিষ্ট প্রজেক্ট ডিটেইলস
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response("Project details retrieved successfully", serializer.data)

    # ৩. নতুন প্রজেক্ট তৈরি (POST)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Project created successfully", serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response("Project creation failed", serializer.errors)

    # ৪. প্রজেক্ট আপডেট (PUT/PATCH)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return success_response("Project updated successfully", serializer.data)
        return error_response("Project update failed", serializer.errors)

    # ৫. আংশিক আপডেট (PATCH)
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # ৬. প্রজেক্ট ডিলিট (DELETE)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response("Project deleted successfully", None, status_code=status.HTTP_204_NO_CONTENT)
    

#-----------------property searching-----------------------


class PropertyViewSet(viewsets.ModelViewSet):
    # ডাটাবেজ অপ্টিমাইজেশনের জন্য select_related ব্যবহার করা হয়েছে
    queryset = Property.objects.all().select_related('project').order_by('-created_at')
    serializer_class = PropertySerializer
    
    # ফিল্টার, সার্চ এবং অর্ডারিং ব্যাকএন্ডস
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # কাস্টম ফিল্টার ক্লাস এবং সার্চ ফিল্ডস
    filterset_class = PropertyFilter
    search_fields = [
        'title', 'unit_number', 'road', 'description', 
        'project__name', 'project__location'
    ]
    
    # সর্টিং বা অর্ডারিং ফিল্ডস
    ordering_fields = ['price', 'size_sqft', 'created_at', 'floor_level']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        # সার্চ এবং ফিল্টার অ্যাপ্লাই করা
        queryset = self.filter_queryset(self.get_queryset())
        
        # প্যাগিনেশন চেক (যদি প্যাগিনেশন সেটআপ করা থাকে)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "total_count": queryset.count(),
            "properties": serializer.data
        }
        return success_response("Successfully retrieved properties", response_data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response("Property details retrieved successfully", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                "Property created successfully", 
                serializer.data, 
                status_code=status.HTTP_201_CREATED
            )
        return error_response("Property creation failed", serializer.errors)
    
    def update(self, request, *args, **kwargs):
        """
        সম্পূর্ণ প্রপার্টি আপডেট করার জন্য (PUT)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return success_response("Property updated successfully", serializer.data)
        
        return error_response("Property update failed", serializer.errors)

    def partial_update(self, request, *args, **kwargs):
        """
        আংশিক আপডেট করার জন্য (PATCH) - যেমন শুধু দাম বা স্ট্যাটাস পরিবর্তন
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # কাস্টম ফিচার্ড এপিআই এন্ডপয়েন্ট
    @action(detail=False, methods=['get'])
    def featured(self, request):
        # এখানেও অপ্টিমাইজেশন ব্যবহার করা হয়েছে
        featured_list = Property.objects.filter(is_featured=True).select_related('project')
        serializer = FeaturedPropertySerializer(featured_list, many=True)
        return success_response("Featured properties retrieved successfully", serializer.data)