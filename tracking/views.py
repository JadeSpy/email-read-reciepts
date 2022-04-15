from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from PIL import Image, ImageDraw
from .forms import TrackerCreationForm
from django.urls import reverse
from .models import Tracker, TrackerHit
from django.template.loader import render_to_string
from django.conf import settings
img = Image.new('RGBA', (1, 1), color = (0,0,0,0))
from django.core.mail import send_mail,BadHeaderError



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def renderEmailHtml(tracker):
	return "empty for now."
def publicImgUrl(tracker):
	relUrl = reverse("tracking:url_of_emailed_tracker_image",args=(tracker.id,))
	return "http://"+settings.SITE_IP+relUrl

def sendMail(tracker):
	subject = tracker.email_subject
	subject = subject.replace("\n","") #just in case
	recipient = tracker.recipient_email
	sender = settings.EMAIL_HOST_USER
	plain_content = tracker.email_content
	imgUrl = publicImgUrl(tracker)
	html_content = render_to_string("tracking/tracker_email_content.html",{"imgUrl":imgUrl,"email_content":plain_content})
	print(html_content)
	try:
		send_mail(subject,plain_content,sender,[recipient],html_message=html_content)
	except BadHeaderError:
		return False
	return True

def trackerCreationSuccessful(request,id):
	tracker = Tracker.objects.get(id=id)
	email_html = renderEmailHtml(tracker)
	return render(request,"tracking/tracker_created_successfully.html",{tracker:tracker,email_html:email_html})
class trackerCreatedSuccessfully(generic.DetailView):
	model = Tracker
	template_name = "tracking/tracker_created_successfully.html"
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context["email_html"] = renderEmailHtml(context["tracker"])
		return context

def create_tracker_form(request):
	if request.method =='POST':
		form = TrackerCreationForm(request.POST)
		if form.is_valid():
			new_tracker = form.save(commit=False)
			new_tracker.save()
			#Add concurrency later, maybe.
			sendMail(new_tracker)
			return HttpResponseRedirect(reverse('tracking:tracker_created_successfully', args=(new_tracker.id,)))
	else:
		form = TrackerCreationForm()
	return render(request, 'tracking/create_tracker_form.html', {"form":form})
	

def get_identifier_image(request,id):
	#log visit
	ip = get_client_ip(request)
	hit = TrackerHit(ip=ip,tracker_id=Tracker.objects.get(id=id))
	hit.save()
	#make response
	response = HttpResponse(content_type='image/png')
	img.save(response, "PNG")
	return response