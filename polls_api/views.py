from polls.models import Question, Vote
from polls_api.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly, IsVoter

class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated] #IsAuthenticated 로그인 X일 땐 못 봄

    #내가 작성한 vote만 보여줌
    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter =self.request.user)
    
    #투표한 사람(로그인된) voter로 저장
    def create(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data['voter'] = request.user.id
        serializer = self.get_serializer(data=new_data) #serializer가 is_valid하기 전에 voter가 있는지 확인
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) #perform_create에 serializer을 넣는것
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    #상세정보 Read, Update, Delete 내가 작성한 Vote만 가능
    permission_classes = [permissions.IsAuthenticated, IsVoter]

    #수정 시: 투표자 로그인된 사람으로 지정
    def perform_update(self, serializer):
        serializer.save(voter=self.request.user)

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    #로그인된 사용자만 질문 생성 가능
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    #create할 때 이미 로그인된 사용지를 owner로 지정
    #오버라이드 됨
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    #로그인된 사용자만 질문 수정가능
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class =UserSerializer

class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterSerializer