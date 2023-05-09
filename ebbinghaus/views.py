from django.shortcuts import render
from ebbinghaus.models import LearnWords
import datetime


# Create your views here.
def index(request):
    if request.method == 'POST':
        for word_form in request.POST:
            word = LearnWords.objects.filter(word=word_form).first()
            if word:
                review_index = eval(request.POST[word_form][0])
                review_list = word.get_review_times
                # print(review_list)
                review_list[review_index-1] = True
                # print(review_list)
                word.review_times = review_list
                word.save()
    today = datetime.date.today()
    words = LearnWords.objects.filter(next_date__lte=today)[:30]
    return render(request, 'ebbinghaus.html', locals())