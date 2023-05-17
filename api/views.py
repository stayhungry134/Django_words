from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LearnWordsSerializer


# Create your views here.
class LearnWordsView(APIView):
    """
    学习单词的表单
    """
    def get(self, request):
        import datetime
        from ebbinghaus.models import LearnWords
        print("我被请求了")
        today = datetime.date.today()
        queryset = LearnWords.objects.filter(next_date__lte=today)[:30]
        serializer = LearnWordsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LearnWordsSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer, type(serializer))
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
