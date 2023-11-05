from django import forms
from .models import Account

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'inp px-3','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'inp px-3','placeholder':'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if email:
    #         email_exists = CompanyUser.objects.filter(email=email).exists()
    #         if email_exists:
    #             raise forms.ValidationError("This Email Already Exists")

    #         company_domain = get_email_domain(self.user.email)
    #         user_domain = get_email_domain(email)
    #         if user_domain != company_domain:
    #             raise forms.ValidationError("This email domain does not belong to your company")
    #     return email