from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from user.models import UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30,label= 'User Name :')
    email = forms.EmailField(max_length=200,label= 'Email :')
    first_name = forms.CharField(max_length=100,label= 'First Name :')
    last_name = forms.CharField(max_length=100,label= 'Last Name :')

    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'password1', 'password2', )


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'first_name'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'last_name' }),
        }


Country = [
    ('India', 'India'),
]

state = [
    ("Andaman & Nicobar Islands",'Andaman & Nicobar Islands'),
    ("Andhra Pradesh",'Andhra Pradesh'),
    ("Arunachal Pradesh",'Arunachal Pradesh'),
    ("Assam",'Assam'),
    ("Bihar",'Bihar'),
    ("Chandigarh",'Chandigarh'),
    ("Chhattisgarh",'Chhattisgarh'),
    ("Dadra & Nagar Haveli",'Dadra & Nagar Haveli'),
    ("Daman and Diu",'Daman and Diu'),
    ("Delhi",'Delhi'),
    ("Goa",'Goa'),
    ("Gujarat",'Gujarat'),
    ("Haryana",'Haryana'),
    ("Himachal Pradesh",'Himachal Pradesh'),
    ("Jammu & Kashmir",'Jammu & Kashmir'),
    ("Jharkhand",'Jharkhand'),
    ("Karnataka",'Karnataka'),
    ("Kerala",'Kerala'),
    ("Lakshadweep",'Lakshadweep'),
    ("Madhya Pradesh",'Madhya Pradesh'),
    ("Maharashtra",'Maharashtra'),
    ("Manipur",'Manipur'),
    ("Meghalaya",'Meghalaya'),
    ("Mizoram",'Mizoram'),
    ("Nagaland",'Nagaland'),
    ("Odisha",'Odisha'),
    ("Puducherry",'Puducherry'),
    ("Punjab",'Punjab'),
    ("Rajasthan",'Rajasthan'),
    ("Sikkim",'Sikkim'),
    ("Tamil Nadu",'Tamil Nadu'),
    ("Telangana",'Telangana'),
    ("Tripura",'Tripura'),
    ("Uttarakhand",'Uttarakhand'),
    ("Uttar Pradesh",'Uttar Pradesh'),
    ("West Bengal",'West Bengal'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city','state','country','image')
        widgets = {
            'phone'     : TextInput(attrs={'class': 'input','placeholder':'phone'}),
            'address'   : TextInput(attrs={'class': 'input','placeholder':'address'}),
            'city'      : TextInput(attrs={'class': 'input','placeholder':'city'}),
            'state': Select(attrs={'class': 'input', 'placeholder': 'country'}, choices=state),
            'country'   : Select(attrs={'class': 'input','placeholder':'country' },choices=Country),
            'image'     : FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }
