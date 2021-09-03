from django import forms

class EncryptForm(forms.Form):
    plain = forms.CharField(label="plain", required=True, widget=forms.Textarea)
    key = forms.CharField(label="key", required=True, widget=forms.Textarea)

class DecryptForm(forms.Form):
    cipher = forms.CharField(label="cipher", required=True, widget=forms.Textarea)
    key = forms.CharField(label="key", required=True, widget=forms.Textarea)

class AffineEncryptForm(forms.Form):
    plain = forms.CharField(label="plain", required=True, widget=forms.Textarea)
    m = forms.CharField(label="m", max_length=2, required=True)
    b = forms.CharField(label="b", required=True)
    
class AffineDecryptForm(forms.Form):
    cipher = forms.CharField(label="cipher", required=True, widget=forms.Textarea)
    m = forms.CharField(label="m", max_length=2, required=True)
    b = forms.CharField(label="b", required=True)