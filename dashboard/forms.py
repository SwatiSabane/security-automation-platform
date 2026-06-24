from django import forms


class ReportUploadForm(forms.Form):

    report_file = forms.FileField()