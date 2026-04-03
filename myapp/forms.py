from django import  forms

class InputForm(forms.Form):

    city = forms.CharField(label="Enter City", max_length=50,
                           widget=forms.TextInput(attrs={
                               "placeholder": "Enter city (e.g., Bangalore)",
                               "class": "form-input"
                           })
                           )

    languages = [("english","English"),("telugu","Telugu"),("kannada","Kannada"),("tamil","Tamil"),("hindi","Hindi")]

    language_field = forms.ChoiceField(choices=languages)