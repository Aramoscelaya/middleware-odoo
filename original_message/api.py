from .models import original_message
from rest_framework import viewsets, permissions
from .serializers import original_messageSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .data import Data
from .models import original_message
from .serializers import original_messageParameterSerializer
from django.core.serializers.json import DjangoJSONEncoder
import json


class OriginalMessageViewSet(viewsets.ModelViewSet):
    queryset = original_message.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = original_messageSerializer


class OriginalMessagesApi(APIView):
    def get(self, request):
        res = original_message.objects.all()
        #res2 = json.dumps(list(res.values()), cls=DjangoJSONEncoder)
        return Response(res.values(), status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = original_messageParameterSerializer(data=request.data)
        if serializer.is_valid():
            parameters = serializer.validated_data['parameters']
            dat = Data()
            res = dat.get_products(parameters)
            #res2 = json.dumps(list(res.values()), cls=DjangoJSONEncoder)
            return Response(res.values(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
