from django.shortcuts import render
from hello import arrytmia
from hello import dislocation

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import default_storage
import json

@csrf_exempt
def index(request):
    if request.GET.get("func") == 'arrytmia':
        func = arrytmia.get_data
    elif request.GET.get("func") == 'dislocation':
        func = dislocation.getData
    data = json.loads(request.GET.get("file"))
    return HttpResponse((func(data)).to_html())

@csrf_exempt
def upload_file(request):
    file_list = []
    if request.method == 'POST':
        if (request.FILES.getlist('arrytmia')):
            for file in request.FILES.getlist('arrytmia'):
                file_name = (default_storage.save(file.name, file))
                if file_name.endswith('hea'):
                    file_list.append(file_name)
            return HttpResponseRedirect(f'/result?file={json.dumps(file_list)}&func=arrytmia')
        else:
            for file in request.FILES.getlist('dislocation'):
                file_list.append(default_storage.save(file.name, file))
            return HttpResponseRedirect(f'/result?file={json.dumps(file_list)}&func=dislocation')
    else:
        return render(request, 'upload.html')