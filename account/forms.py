from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class QueryForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput)
    # industry = forms.CharField(widget=forms.TextInput)
    # year_founded = forms.CharField(widget=forms.TextInput)
    # city = forms.CharField(widget=forms.TextInput)
    # state = forms.CharField(widget=forms.TextInput)
    # Employee = forms.CharField(widget=forms.TextInput)
