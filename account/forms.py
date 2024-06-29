
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm




        
        
class SignupForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            ''' to save the old value of inputs in case of unsuccessful attempt to register'''
            self.fields['username'].initial = self.instance.username
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['password1'].initial = ''
            self.fields['password2'].initial = ''
            
    class Meta:
        model = get_user_model()
        fields = ('username',  'password1', 'password2', 'first_name', 'last_name', "father_name", "pesonal_code", "national_code", "telephone", "phone", "address",)
        