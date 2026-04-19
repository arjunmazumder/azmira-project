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

# আপনার কাস্টম রেসপন্স ফাংশনগুলো (যদি অন্য ফাইল থেকে ইম্পোর্ট করেন তবে এটি লাগবে না)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response("Projects retrieved successfully", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response("Project details retrieved successfully", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Project created successfully", serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response("Project creation failed", serializer.errors)

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


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response("Properties retrieved successfully", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response("Property details retrieved successfully", serializer.data)

    # কাস্টম ফিচার্ড এপিআই এন্ডপয়েন্ট
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_list = Property.objects.filter(is_featured=True)
        serializer = FeaturedPropertySerializer(featured_list, many=True)
        return success_response("Featured properties retrieved successfully", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Property created successfully", serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response("Property creation failed", serializer.errors)
    
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
    # সব প্রজেক্ট নেওয়ার সময় select_related বা prefetch_related ব্যবহার করা ভালো পারফরম্যান্সের জন্য
    queryset = Project.objects.all().prefetch_related('properties').order_by('-created_at')
    serializer_class = ProjectSerializer
    
    # ফিল্টার ব্যাকএন্ডস
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # সার্চ ফিল্ডস: এখানে প্রজেক্ট এবং প্রপার্টি উভয় মডেলের ফিল্ড আছে
    search_fields = [
        # Project মডেলের ফিল্ড
        'name', 
        'location', 
        'developer_name', 
        'project_type', 
        'status',
        
        # Property (Related) মডেলের ফিল্ড (Double Underscore ব্যবহার করে)
        'properties__title', 
        'properties__unit_number',
        'properties__road',
        'properties__price',
        'properties__description'
    ]
    
    # অর্ডারিং ফিল্ডস
    ordering_fields = ['created_at', 'name']

    def list(self, request, *args, **kwargs):
        # সার্চ এবং ফিল্টার অনুযায়ী কুয়েরিসেট ফিল্টার করা
        queryset = self.filter_queryset(self.get_queryset())
        
        # ফিল্টার করার পর মোট কয়টি প্রজেক্ট পাওয়া গেল
        total_count = queryset.count()
        
        # ডাটা সিরিয়ালাইজ করা
        serializer = self.get_serializer(queryset, many=True)
        
        # আপনার ডিমান্ড অনুযায়ী স্ট্যান্ডার্ড রেসপন্স ফরম্যাট
        response_data = {
            "total_count": total_count,
            "projects": serializer.data
        }
        
        return success_response("Projects retrieved successfully", response_data)
    
#-----------------property searching-----------------------

class PropertyViewSet(viewsets.ModelViewSet):
    # ডাটাবেজ অপ্টিমাইজেশনের জন্য select_related ব্যবহার করা হয়েছে
    queryset = Property.objects.all().select_related('project').order_by('-created_at')
    serializer_class = PropertySerializer
    
    # ব্যাকএন্ডস: ফিল্টার, সার্চ এবং অর্ডারিং (সর্টিং)
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # কাস্টম ফিল্টার ক্লাস
    filterset_class = PropertyFilter
    
    # সার্চ ফিল্ডস (গ্লোবাল সার্চের জন্য)
    search_fields = [
        'title', 'unit_number', 'road', 'description', 
        'project__name', 'project__location'
    ]
    
    # সর্টিং বা অর্ডারিং ফিল্ডস (ইউজার যা দিয়ে সর্ট করতে পারবে)
    ordering_fields = ['price', 'size_sqft', 'created_at', 'floor_level']
    # ডিফল্টভাবে নতুনগুলো আগে দেখাবে
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        # সার্চ এবং ফিল্টার অ্যাপ্লাই করা
        queryset = self.filter_queryset(self.get_queryset())
        
        # ফিল্টার করার পর মোট রেজাল্ট সংখ্যা
        total_count = queryset.count()
        
        # ডাটা সিরিয়ালাইজ করা
        serializer = self.get_serializer(queryset, many=True)
        
        # স্ট্যান্ডার্ড রেসপন্স ডাটা
        response_data = {
            "total_count": total_count,
            "properties": serializer.data
        }
        
        return success_response(f"Successfully retrieved {total_count} properties", response_data)