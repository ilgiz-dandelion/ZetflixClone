# from django.contrib.auth.models import User                                # Django Build in User Model

from rest_framework.decorators import api_view
from django.db.models import Q
from account.models import MyUser
from rest_framework.response import Response
from chat.models import Message
from chat.serializers import MessageSerializer, UserSerializer
# Users View
@api_view(["GET",])
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = MyUser.objects.filter(id=pk)
        else:
            users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data, )




@api_view(["POST", "GET"])
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(Q(sender_id=sender, receiver_id=receiver)|Q(sender_id=receiver, receiver_id=sender))
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return Response(serializer.data, )

    elif request.method == 'POST':
        data = request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
