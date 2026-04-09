from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from projects.models import Project, Property, ClientReview
from core.response import success_response, error_response
from projects.serializers import(
    ProjectSerializer, PropertySerializer, FeaturedPropertySerializer,
    BlogPostSerializer, ClientReviewSerializer
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
        serializer = ProjectSerializer(projects, many=True)
        return success_response("All projects retrieved successfully", serializer.data)

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
    def get(self, request, location=None):
        location_param = location or request.query_params.get('location', '')
        location_text = location_param.replace('-', ' ')

        projects = Project.objects.filter(location__icontains=location_text)

        serializer = ProjectSerializer(projects, many=True)
        return success_response("Projects by location", serializer.data)


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