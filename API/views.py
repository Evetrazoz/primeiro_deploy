
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from . import models
from .serializer import LivroSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

@swagger_auto_schema(
    methods=["POST"],
    request_body=UserSerializer,
    tags=["token"],
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"username": serializer.data["username"]}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
@swagger_auto_schema(
    methods=["POST"],
    request_body=LivroSerializer,
    tags=["Livroo"],
)
@swagger_auto_schema(
    methods=["GET"],
    tags=["Livroo"],
    manual_parameters=[
        openapi.Parameter("pageSize", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter("page", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
)
@api_view(["GET", "POST"])
def Livro(request):
    if request.method == "GET":
        paginator = PageNumberPagination()
        #http://127.0.0.1:8000/api/livro/?pageSize=10
        paginator.page_size = request.query_params.get("pageSize", 1)
        livros = models.Livro.objects.all()
        paginated_livros = paginator.paginate_queryset(livros, request)
        serializer = LivroSerializer(paginated_livros, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == "POST":
        serializer = LivroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def livroById(request, pk):
    try:
        livro = models.Livro.objects.get(pk=pk)
        if not request.user.groups.filter(name="admin").exists():
            return Response({"error": "acesso negado"},status=status.HTTP_403_FORBIDDEN)
    except models.Livro.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = LivroSerializer(livro)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = LivroSerializer(livro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        livro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)