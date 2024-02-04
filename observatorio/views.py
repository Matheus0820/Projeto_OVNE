from django.shortcuts import render
from django.core.paginator import Paginator
from controller.models import Videos, Materias, TextosMaterias, ImagensMaterias


def home(request):
    return render(request, 'homepage.html')

def noticia(request):
    if request.GET.get('search'):
        search = request.GET.get('search')

        if request.GET.get('filtro'):
            filtro = request.GET.get('filtro')
            if filtro == 'Recentes':   
               materias = Materias.objects.filter(titulo__icontains=search).order_by('-id')

            elif filtro == 'Antigos':
                materias = Materias.objects.filter(titulo__icontains=search).order_by('id')

            elif filtro == 'A-Z': 
                materias = Materias.objects.filter(titulo__icontains=search).order_by('titulo')
            
            elif filtro == 'Z-A':
                materias = Materias.objects.filter(titulo__icontains=search).order_by('-titulo')
        else:
            materias = Materias.objects.filter(titulo__icontains=search)
            
        materias_pagination = Paginator(materias, 3)
        numemro_pagina = request.GET.get('page')
        pagina = materias_pagination.get_page(numemro_pagina)
        return render(request, 'noticias.html', {'pagina': pagina})
    
    elif request.GET.get('filtro'):
        filtro = request.GET.get('filtro')

        if filtro == 'Recentes':   
            materias = Materias.objects.all().order_by('-id')

        elif filtro == 'Antigos':
            materias = Materias.objects.all().order_by('id')

        elif filtro == 'A-Z': 
            materias = Materias.objects.all().order_by('titulo')
        
        elif filtro == 'Z-A':
            materias = Materias.objects.all().order_by('-titulo')

        materias_pagination = Paginator(materias, 3)
        numemro_pagina = request.GET.get('page')
        pagina = materias_pagination.get_page(numemro_pagina)
        return render(request, 'noticias.html', {'pagina': pagina})
    else:
        materias = Materias.objects.all().order_by('-id')
        materias_pagination = Paginator(materias, 3)
        numemro_pagina = request.GET.get('page')
        pagina = materias_pagination.get_page(numemro_pagina)
        return render(request, 'noticias.html', {'pagina': pagina})

def view_noticia(request, id):
    materia = Materias.objects.get(id=id)
    textos = TextosMaterias.objects.filter(materia=materia)
    imagens = ImagensMaterias.objects.filter(materia=materia)
    materias = Materias.objects.exclude(id=id)
    context = {
        'materias': materias,
        'materia': materia,
        'textos': textos,
        'imagens': imagens
    }
    return render(request, 'view_noticia.html', context)

def video(request):
    if request.GET.get('search'):
        search = request.GET.get('search')

        if request.GET.get('filtro'):
            filtro = request.GET.get('filtro')
            if filtro == 'Recentes':   
               videos = Videos.objects.filter(titulo__icontains=search).order_by('-id')

            elif filtro == 'Antigos':
                videos = Videos.objects.filter(titulo__icontains=search).order_by('id')

            elif filtro == 'A-Z': 
                videos = Videos.objects.filter(titulo__icontains=search).order_by('titulo')
            
            elif filtro == 'Z-A':
                videos = Videos.objects.filter(titulo__icontains=search).order_by('-titulo')
        else:
            videos = Videos.objects.filter(titulo__icontains=search)
            
        videos_pagination = Paginator(videos, 3)
        numero_pagina = request.GET.get('page')
        pagina = videos_pagination.get_page(numero_pagina)
        return render(request, 'videos.html', {'pagina': pagina})
    
    elif request.GET.get('filtro'):
        filtro = request.GET.get('filtro')

        if filtro == 'Recentes':   
            videos = Videos.objects.all().order_by('-id')

        elif filtro == 'Antigos':
            videos = Videos.objects.all().order_by('id')

        elif filtro == 'A-Z': 
            videos = Videos.objects.all().order_by('titulo')
        
        elif filtro == 'Z-A':
            videos = Videos.objects.all().order_by('-titulo')

        videos_pagination = Paginator(videos, 3)
        numero_pagina = request.GET.get('page')
        pagina = videos_pagination.get_page(numero_pagina)
        return render(request, 'videos.html', {'pagina': pagina})
    else:
        videos = Videos.objects.all().order_by('-id')
        videos_pagination = Paginator(videos, 3)
        numero_pagina = request.GET.get('page')
        pagina = videos_pagination.get_page(numero_pagina)
        return render(request, 'videos.html', {'pagina': pagina})

def play_video(request, id):
    video = Videos.objects.get(id=id)
    videos_all = Videos.objects.exclude(id=id).order_by('-id')
    videos_pagination = Paginator(videos_all, 5)
    numero_pagina = 1
    videos = videos_pagination.get_page(numero_pagina)
    context = {
        'videos': videos,
        'video': video
    }
    return render(request, 'play_video.html', context)

def sobre(request):
    return render(request, 'sobre.html')



