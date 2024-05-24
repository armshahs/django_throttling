from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response

# for individual class throttles import here
from rest_framework.throttling import (
    AnonRateThrottle,
    UserRateThrottle,
    ScopedRateThrottle,
)

from .models import Todo
from .serializers import TodoSerializer
from .throttle import post_todo_generics_throttle


# Create your views here.
@api_view(["GET"])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def get_todos(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Rewriting the above in GenericAPIView
class get_todos_generics(generics.GenericAPIView):

    # adding throttle for individual class
    throttle_classes = (AnonRateThrottle,)

    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# Custom throttle
@throttle_classes([post_todo_generics_throttle])
def post_todo(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(
        {"message": "Request failed, please try again"},
        status=status.HTTP_400_BAD_REQUEST,
    )


# Rewriting the post request in GenericAPIView
class post_todo_generics(generics.GenericAPIView):

    # Default throttle-->
    # throttle_classes = (AnonRateThrottle,UserRateThrottle,) OR
    # throttle_classes = (AnonRateThrottle,)

    # ScopedRateThrottling-->
    # throttle_classes = (ScopedRateThrottle,)
    # throttle_scope = "todo-post"

    # CustomThrottling-->
    throttle_classes = (post_todo_generics_throttle,)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "Request failed, please try again"},
            status=status.HTTP_400_BAD_REQUEST,
        )
