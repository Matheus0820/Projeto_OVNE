from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from .models import Videos, Materias, TextosMaterias, ImagensMaterias

class FormCadastrarVideo(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ('capa', 'titulo', 'url', 'descricao',)
        widgets = {
            'capa': forms.FileInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'name': 'titulo', 'autocomplete': 'off'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'name': 'url', 'autocomplete': 'off'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'name': 'descricao', 'rows': 5}),
        }

class FormCadastroMateria(forms.ModelForm):
    class Meta:
        model = Materias
        fields = ('capa', 'titulo', 'resumo', 'autor',)
        widgets = {
            'capa': forms.FileInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'name': 'titulo', 'autocomplete': 'off'}),
            'resumo': forms.Textarea(attrs={'class': 'form-control', 'name': 'resumo', 'rows': 5}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'name': 'autor', 'autocomplete': 'off'}),
        }

class FormTextoMateria(forms.ModelForm):
    class Meta:
        model = TextosMaterias
        fields = ('topico', 'texto',)
        widgets = {
            'topico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Introdução', 'autocomplete': 'off'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class FormImagemMateria(forms.ModelForm):
    class Meta:
        model = ImagensMaterias
        fields = ('legenda', 'fonte', 'imagem',)
        widgets = {
            'legenda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Imagem do Centro Histórico', 'autocomplete': 'off'}),
            'fonte': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Imagem registrada por Matheus Ramos em 2023', 'autocomplete': 'off'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }

ImagemFormset = inlineformset_factory(Materias, ImagensMaterias, form=FormImagemMateria, extra=1, can_delete=True)
TextoFormset = inlineformset_factory(Materias, TextosMaterias, form=FormTextoMateria, extra=1, can_delete=True)

class FormUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'password1', 'password2', 'username', 'email',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'}), 
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

