from django import forms

class LoginForm(forms.Form):
    login_username = forms.CharField(label='Username', max_length=150)
    login_password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', required=False)
    firstname = forms.CharField(label='Firstname', required=False, max_length=30)
    lastname = forms.CharField(label='Lastname', required=False, max_length=150)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Passwords not match!")
