from django.shortcuts import render
from django.views import generic
from .forms import ContactForm
from .forms import UploadImageForm
from django.contrib import messages
from django.urls import reverse_lazy
import logging
from django.shortcuts import render
from .application import pdf2summary_2, pdf2summary_1
from django.conf import settings
import os


logger = logging.getLogger(__name__)

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        if 'pdf' in request.FILES:
            if "1_dan" == request.POST.get("dan"):
                form = UploadImageForm(request.POST, request.FILES)
                updata = request.FILES['pdf']    #2
                number = request.POST.get("number")
                pdf_link = request.FILES['pdf'].name
                with open(settings.MEDIA_ROOT  + '/pdf/' + request.FILES['pdf'].name, 'wb+') as f:    #3
                    for chunk in updata.chunks():
                        f.write(chunk)
                form = UploadImageForm()
                summary = pdf2summary_1.pdf_s(pdf_link, number)
                os.remove(settings.MEDIA_ROOT  + '/pdf/' + request.FILES['pdf'].name)
                context = {'form': form,
                           'summary': summary,
                           'number': number,
                           'pdf_link': pdf_link,
                           'dan': request.POST.get("dan"),
                           'type': request.POST.get("type"),
                           'lang': request.POST.get("lang"),
                           }
                return render(request, ResultView.template_name, context=context)
            else:
                form = UploadImageForm(request.POST, request.FILES)
                updata = request.FILES['pdf']    #2
                number = request.POST.get("number")
                pdf_link = request.FILES['pdf'].name
                with open(settings.MEDIA_ROOT  + '/pdf/' + request.FILES['pdf'].name, 'wb+') as f:    #3
                    for chunk in updata.chunks():
                        f.write(chunk)
                form = UploadImageForm()
                summary, text_link = pdf2summary_2.main(pdf_link, number)
                os.remove(text_link)
                os.remove(settings.MEDIA_ROOT  + '/pdf/' + request.FILES['pdf'].name)
                context = {'form': form,
                           'summary': summary,
                           'number': number,
                           'pdf_link': pdf_link,
                           'dan': request.POST.get("dan"),
                           'type': request.POST.get("type"),
                           'lang': request.POST.get("lang"),
                           }
                return render(request, ResultView.template_name, context=context)
        else:
            return render(request, self.template_name, context=self.kwargs)
        

class ContactView(generic.FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('pdfs:contact')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Contact sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class ResultView(generic.TemplateView):
    template_name = "result.html"