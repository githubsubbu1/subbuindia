from django import forms

class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)
    widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control col-6'
                }
            ),
            'email':forms.EmailInput(attrs={'class':'form-control col-6'}),
            'to': forms.EmailInput(
                attrs={
                    'class': 'form-control col-6'
                }
            ),
            #'email_to':forms.EmailInput(attrs={'class':'form-control col-6'}),

        }


from blog.models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')
