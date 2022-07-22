from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs.models import Blog
from blogs.serializers import BlogSerializer
from rest_framework.decorators import api_view

# Create your views here.
# def index(request):
#     return render(request, "tutorials/index.html")


def index(request):
    print("------------------------- I AM HERE")
    queryset = Blog.objects.all()
    return render(request, "blogs/index.html", {'blogs': queryset})


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blogs/index.html'

    def get(self, request):
        queryset = Blog.objects.all()
        return Response({'Blog': queryset})


class list_all_blogs(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blogs/blog_list.html'

    def get(self, request):
        queryset = Blog.objects.all()
        return Response({'blogs': queryset})


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def blog_list(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            blogs = blogs.filter(title__icontains=title)

        blogs_serializer = BlogSerializer(blogs, many=True)
        return JsonResponse(blogs_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        blog_data = JSONParser().parse(request)
        blog_serializer = BlogSerializer(data=blog_data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            return JsonResponse(blog_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(blog_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Blog.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Blogs were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return JsonResponse({'message': 'This blog does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        blog_serializer = BlogSerializer(blog)
        return JsonResponse(blog_serializer.data)

    elif request.method == 'PUT':
        blog_data = JSONParser().parse(request)
        blog_serializer = BlogSerializer(blog, data=blog_data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            return JsonResponse(blog_serializer.data)
        return JsonResponse(blog_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        blog.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def blog_list_published(request):
    blogs = Blog.objects.filter(published=True)

    if request.method == 'GET':
        blogs_serializer = BlogSerializer(blogs, many=True)
        return JsonResponse(blogs_serializer.data, safe=False)