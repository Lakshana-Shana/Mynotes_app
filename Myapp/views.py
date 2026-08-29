from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from .models import Note
from .serializers import NoteSerializer


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not name or not email or not password:
            return Response(
                {
                    'message': 'All fields are required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=email).exists():
            return Response(
                {
                    'message': 'User already exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        return Response(
            {
                'message': 'Registration successful'
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            username=email,
            password=password
        )

        if user is None:
            return Response(
                {
                    'message': 'Invalid email or password'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'message': 'Login successful',

                'access': str(refresh.access_token),

                'refresh': str(refresh),

                'name': user.first_name,

                'email': user.email
            },
            status=status.HTTP_200_OK
        )
class NoteListCreateView(APIView):

    def get(self, request):

        notes = Note.objects.filter(
            user=request.user
        ).order_by('-created_at')

        serializer = NoteSerializer(
            notes,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = NoteSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class NoteDetailView(APIView):

    def get_object(self, pk, user):

        try:
            return Note.objects.get(
                pk=pk,
                user=user
            )

        except Note.DoesNotExist:
            return None

    def get(self, request, pk):

        note = self.get_object(
            pk,
            request.user
        )

        if note is None:
            return Response(
                {
                    'message': 'Note not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NoteSerializer(note)

        return Response(serializer.data)

    def put(self, request, pk):

        note = self.get_object(
            pk,
            request.user
        )

        if note is None:
            return Response(
                {
                    'message': 'Note not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NoteSerializer(
            note,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        note = self.get_object(
            pk,
            request.user
        )

        if note is None:
            return Response(
                {
                    'message': 'Note not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        note.delete()

        return Response(
            {
                'message': 'Note deleted successfully'
            },
            status=status.HTTP_200_OK
        )
