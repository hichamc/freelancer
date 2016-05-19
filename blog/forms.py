from django import forms
from django.contrib.auth.models import User
from .models import Project, Bid, Account, Pimage

#from .models import SignUp

# class SignUpForm(forms.ModelForm):
# 	class Meta:
# 		model = SignUp
# 		fields = ['full_name','email']

# 	def clean_email(self):
# 		email = self.cleaned_data.get('email')
# 		return email



class SignUpForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget = forms.PasswordInput)
    password_repeat = forms.CharField(max_length=255, widget = forms.PasswordInput)
    
    # def clean(self):
    #     form_data = self.cleaned_data
    #     if form_data['password'] != form_data['password_repeat']:
    #         self._errors["password"] = ["Password do not match"] # Will raise a error message
    #         del form_data['password']
    #     return form_data

    class Meta:
        model = Account
        # widgets = {'password': forms.PasswordInput(),}
        fields = ['email','first_name', 'last_name', 'image', 'username', 'password']


class LoginForm(forms.ModelForm):
    class Meta:
        model = Account
        widgets = {'password': forms.PasswordInput(),}
        fields = ['email','password']



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','category','descrip']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount','descrip']

class PimageForm(forms.ModelForm):
    image = forms.FileField(label='Image')
    class Meta:
        model = Pimage
        fields =['image']