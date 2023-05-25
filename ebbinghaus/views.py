from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LearnWordsSerializer


# Create your views here.
class LearnWordsView(APIView):
    """学习单词的试图"""
    def get(self, request):
        import datetime
        from ebbinghaus.models import LearnWords
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


class PutWordsView(APIView):
    """提交每日单词的视图"""
    def get(self, request):
        return Response("我被调用了")

    def post(self, request):
        for word_data in request.data.values():
            serializer = LearnWordsSerializer(data=word_data)
            if serializer.is_valid():
                serializer.save()
            else:
                import logging
                logger = logging.getLogger('ebbinghaus')
                logger.info(f"{word_data}")
                logger.info(serializer.errors)
        return Response("你提交了一个post请求")