import datetime
from django.db import models

class Videos(models.Model):
    titulo = models.CharField(max_length=100, help_text= "Coloque um titulo para o vídeo. Esse titulo será visivel ao público")
    url = models.URLField(help_text="Coloque nesse campo a URL do vídeo fornecida pelo YouTube")
    descricao = models.TextField(max_length=1000, help_text="Coloque nesse campo uma descricao para o vídeo")
    publicacao = models.DateTimeField(default=datetime.datetime.now())
    capa = models.ImageField(upload_to="capas", default=None)

    class Meta:
        db_table = "Videos"
        verbose_name_plural = "Videos"

    def __str__(self) -> str:
        return f"Título: {self.titulo} - URL: {self.url}"

class Materias(models.Model):
    titulo = models.CharField(max_length=100, help_text= "Preencha esse campo com o titulo da materias")
    resumo = models.TextField(max_length=2500, help_text="Preencha com o resumo da materias")
    autor = models.CharField(max_length=200, help_text="Nome do criador da materia")
    publicacao = models.DateTimeField(default=datetime.datetime.now())
    capa = models.ImageField(upload_to="capas", default=None)

    class Meta:
        db_table = "Materias"
        verbose_name_plural = "Materias"

    def __str__(self) -> str:
        return f"Título: {self.titulo} - Autor: {self.autor}"
    
class TextosMaterias(models.Model):
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name="materia_textos")
    topico = models.CharField(max_length=50, help_text="Preencha com o nome do Tópico")
    texto = models.TextField(max_length=3000, help_text="Preencha com o texto da sua materia")

    class Meta:
        db_table = 'Textos Materias'
        verbose_name = 'Textos Materias'
        verbose_name_plural = 'Textos Materias'

    def __str__(self) -> str:
        return f"Texto da matéria: {self.materia} - Tópico: {self.topico}"

class ImagensMaterias(models.Model):
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name="materia_imagens")
    legenda = models.CharField(max_length=50, help_text="Preencha com uma legenda para imagem")
    fonte = models.CharField(max_length=200, help_text="Preencha com a Fonte da imagem")
    imagem = models.ImageField(upload_to='imagens')

    class Mata: 
        db_table = 'Imagens Materias'
        verbose_name = 'Imagens Materias'
        verbose_name_plural = 'Imagens Materias'
    
    def __str__(self) -> str:
        return f"Imagem da matéria: {self.materia} - Legenda: {self.legenda}"
