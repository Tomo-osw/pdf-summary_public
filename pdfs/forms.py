from django import forms
from django.core.mail import EmailMessage

class ContactForm(forms.Form):
    name = forms.CharField(label='Name/お名前', max_length=30)
    email = forms.EmailField(label='MailAddress/メールアドレス')
    title = forms.CharField(label='Title/件名', max_length=40)
    message = forms.CharField(label='Message/内容', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = 'Please enter your name. / お名前を入力してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'Please enter your email address. / メールアドレスを入力してください。'

        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'Please enter the subject. / 件名を入力してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'Please enter the content. / 内容を入力してください。'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ: {}'.format(title)
        message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(name, email, message)
        from_email = '***'
        to_list = [
            email
        ]
        cc_list = [
            
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()

class UploadImageForm(forms.Form):
    Uploadfile = forms.FileField()