from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from smslink import api

@csrf_exempt
def sms_received(request):
    if request.method == 'POST':
        number = request.POST['From']
        text = request.POST['Body']

        api.sms_received(number, text)

    return HttpResponse(status=200)


