from django.forms import ModelForm
from forum.models import Forum
from django.utils.html import strip_tags
class ForumEntryForm(ModelForm):
    class Meta:
        model = Forum
        fields = ["title", "details"]
    def clean_title(self):
        title = self.cleaned_data["title"]
        return strip_tags(title)

    def clean_details(self):
        details = self.cleaned_data["details"]
        return strip_tags(details)
    
