from django import forms
from .models import Tracker
class TrackerCreationForm(forms.ModelForm):
	class Meta:
		model = Tracker
		fields = ["recipient_name","recipient_email","email_subject","email_content"]