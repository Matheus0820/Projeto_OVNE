from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import (
    FormCadastrarVideo, FormCadastroMateria, FormTextoMateria, 
    FormImagemMateria, ImagemFormset, TextoFormset, FormUser
)
from .models import Videos, Materias, TextosMaterias, ImagensMaterias
import os

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('user')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if authenticate(username=username, password=password): 
            login_django(request, user)
            return redirect(controller)
        else:
            messages.error(request, 'Sua Senha ou usuário devem está errados')
            return render(request, 'login.html')

@login_required
def logout(request):
    logout_django(request)
    return render(request, 'login.html')

@login_required
def add_user(request):
    if request.method == 'GET':
        form = FormUser()

        context = {
            'form': form,
        }

        return render(request, 'forms/add_user.html', context)

    elif request.method == 'POST':
        form = FormUser(request.POST)

        context = {
            'form': form,
        }

        if form.is_valid():
            form.save()

            messages.success(request, 'Usuário adicionado com sucesso!')
            return render(request, 'forms/add_user.html', context)

        else:
            StrErros = ""
            for campo, mensagem in form.errors.items():
                StrErros += mensagem

            messages.error(request, StrErros)
            return render(request, 'forms/add_user.html', context)

@login_required
def info_user(request, id):
    if request.method == 'GET':
        usuario = User.objects.get(id=id)

        context = {
            'usuario': usuario,
        }

        return render(request, 'pages/info_user.html', context)

@login_required
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()

    messages.success(request, "Usuário removido com sucesso!")
    return redirect(list_users)

@login_required
def list_users(request):
    if request.method == 'GET':
        if request.GET.get('search'):
            search = request.GET.get('search')

            if request.GET.get('filtro'):
                filtro = request.GET.get('filtro')

                if filtro == 'Recentes':   
                   users = User.objects.filter(first_name__icontains=search).order_by('-id')

                elif filtro == 'Antigos':
                   users = User.objects.filter(first_name__icontains=search).order_by('id')

                elif filtro == 'A-Z': 
                   users = User.objects.filter(first_name__icontains=search).order_by('first_name')
                
                elif filtro == 'Z-A':
                   users = User.objects.filter(first_name__icontains=search).order_by('-first_name')
            else:
                users = User.objects.filter(first_name__icontains=search)

            users_pagination = Paginator(users, 5)
            numero_pagina = request.GET.get('page')
            pagina = users_pagination.get_page(numero_pagina)
            return render(request, 'pages/list_users.html', {'pagina': pagina})
        
        elif request.GET.get('filtro'):
            filtro = request.GET.get('filtro')

            if filtro == 'Recentes':   
                users = User.objects.all().order_by('-id')

            elif filtro == 'Antigos':
                users = User.objects.all().order_by('id')

            elif filtro == 'A-Z': 
                users = User.objects.all().order_by('first_name')
            
            elif filtro == 'Z-A':
                users = User.objects.all().order_by('-first_name')

            users_pagination = Paginator(users, 5)
            numero_pagina = request.GET.get('page')
            pagina = users_pagination.get_page(numero_pagina)
            return render(request, 'pages/list_users.html', {'pagina': pagina})
        else:
            users = User.objects.all().order_by('-id')
            users_pagination = Paginator(users, 5)
            numero_pagina = request.GET.get('page')
            pagina = users_pagination.get_page(numero_pagina)
            return render(request, 'pages/list_users.html', {'pagina': pagina})


@login_required
def profile_user(request):
    if request.method == 'GET':
        id_user = request.user.id
        usuario = User.objects.get(id=id_user)
        form = FormUser(instance=usuario)

        context = {
            'usuario': usuario,
            'form': form,
        }

        return render(request, 'pages/perfil_user.html', context)

    elif request.method == 'POST':
        id_user = request.user.id
        usuario = User.objects.get(id=id_user)

        form = FormUser(request.POST, instance=usuario)

        context = {
            'usuario': usuario,
            'form': form,
        }

        first_name = request.POST.get('first_name')
        email = request.POST.get('email')

        if request.user.email != email and User.objects.filter(email=email).exists():
            messages.error(request, "Email já usado por outro usuário!")
            return render(request, 'pages/perfil_user.html', context)

        else:
            usuario.first_name = first_name
            usuario.email = email
            usuario.save()

            messages.success(request, "Informações modificadas com sucesso!")
            return redirect(profile_user)

@login_required
def alterar_senha(request):
    if request.method == 'GET':

        return render(request, 'forms/alterar_senha.html')
    
    elif request.method == 'POST':
        id_user = request.user.id
        user = User.objects.get(id=id_user)

        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password is not None and confirm_password is not None:
            if new_password == confirm_password:
                if not new_password.isdigit():
                    vector_password = []
                    for carcter in new_password:
                        vector_password.append(carcter)

                    if len(vector_password) >= 8:
                        user.set_password(str(new_password))
                        user.save()

                        messages.success(request, 'Senha alterada com sucesso')
                        return redirect(profile_user)

                    else:
                        messages.error(request, 'Senha possui menos de 8 (oito) caracteres! Corrija.')
                        return render(request, 'forms/alterar_senha.html')

                else:
                    messages.error(request, 'A senha contém somente números. Digite novamente')
                    return render(request, 'forms/alterar_senha.html')

            else:
                messages.error(request, 'Os campos de senha não Coincidem. Digite novamente!')
                return render(request, 'forms/alterar_senha.html')
        
        else:
            messages.error(request, 'Senha não digitada! Alteração não pode ser feita.')
            return render(request, 'forms/alterar_senha.html')


@login_required
def controller(request):
    totalvideos = Videos.objects.count()
    totalmaterias = Materias.objects.count()
    totalusuarios = User.objects.count()

    context = {
        'totalvideos': totalvideos,
        'totalmaterias': totalmaterias,
        'totalusuarios': totalusuarios
    }

    return render(request, 'controller.html', context)
    
@login_required
def add_video(request):
    if request.method == 'GET':
        form = FormCadastrarVideo()
        return render(request, 'pages/add_video.html', {'form': form})
    else: 
        form = FormCadastrarVideo(request.POST, request.FILES)
        if form.is_valid():
            titulo = form.data['titulo']
            if Videos.objects.filter(titulo=titulo).exists():
                messages.error(request, "Vídeo já cadastrado!")
                return render(request, 'pages/add_video.html', {'form': form})
            else:
                form.save()
                videos = Videos.objects.all()
                messages.success(request, "Vídeo cadastrado com sucesso!")
                return redirect(list_video)
        else:
            messages.error(request, "Algum campo foi digitado incorretamente. Corrija!")
            return render(request, 'pages/add_video.html', {'form': form})


@login_required
def list_video(request):
    if request.method == 'GET':
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

            videos_pagination = Paginator(videos, 5)
            numero_pagina = request.GET.get('page')
            pagina = videos_pagination.get_page(numero_pagina)
            return render(request, 'pages/list_video.html', {'pagina': pagina})
        
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

            videos_pagination = Paginator(videos, 5)
            numero_pagina = request.GET.get('page')
            pagina = videos_pagination.get_page(numero_pagina)
            return render(request, 'pages/list_video.html', {'pagina': pagina})
        else:
            videos = Videos.objects.all().order_by('-id')
            videos_pagination = Paginator(videos, 5)
            numero_pagina = request.GET.get('page')
            pagina = videos_pagination.get_page(numero_pagina)
            return render(request, 'pages/list_video.html', {'pagina': pagina})
    else: 
        pass

@login_required
def edit_video(request, id):
    video = Videos.objects.get(id=id)
    if request.method == 'GET':
        form = FormCadastrarVideo(instance=video)
        return render(request, 'pages/edit_video.html', {'form': form, 'id': id})
    else:
        form = FormCadastrarVideo(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, "Modificações feitas e salvas com sucesso.")
            return redirect(list_video)
        else:
            messages.error(request, "Algum campo foi digitado incorretamente. Corrija!")
            return render(request, 'pages/edit_video.html', {'form': form, 'id': id})
            

@login_required
def delete_video(request, id):
    if request.method == 'GET':
        video = Videos.objects.get(id=id)
        if os.path.isfile(video.capa.path):
                os.remove(video.capa.path)
        video.delete()
        return redirect(list_video)
    else: 
        pass

@login_required
def add_materia(request):
    if request.method == 'GET':
        form = FormCadastroMateria()
        formset_texto = TextoFormset()
        formset_imagem = ImagemFormset()

        context = {
            'form': form,
            'form_texto': formset_texto,
            'form_imagem': formset_imagem,
        }
        return render(request, 'pages/add_materia.html', context)
    else:
        form = FormCadastroMateria(request.POST, request.FILES)
        formset_texto = TextoFormset(request.POST)
        formset_imagem = ImagemFormset(request.POST, request.FILES)
        context = {
            'form': form,
            'form_texto': formset_texto,
            'form_imagem': formset_imagem,
        }

        if form.is_valid() and formset_texto.is_valid() and formset_imagem.is_valid():
            titulo = form.data['titulo']
            if Materias.objects.filter(titulo=titulo).exists():
                messages.error(request, "Já existe uma materia cadastrada com esse titulo!")
                return render(request, 'pages/add_materia.html', context)
            else:
                materia = form.save()
                formset_imagem.instance = materia
                formset_imagem.save()
                formset_texto.instance = materia
                formset_texto.save()
                messages.success(request, "Matéria cadastrada com sucesso")
                return redirect(list_materia)

        else:
            messages.error(request, "Algum campo foi preenchido incorretamente. Corrija!")
            return render(request, 'pages/add_materia.html', context)



@login_required
def list_materia(request):
    if request.method == 'GET':
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

            materias_pagination = Paginator(materias, 5)
            numero_pagina = request.GET.get('page')
            pagina = materias_pagination.get_page(numero_pagina)

            return render(request, 'pages/list_materia.html', {'pagina': pagina})
        
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

            materias_pagination = Paginator(materias, 5)
            numero_pagina = request.GET.get('page')
            pagina = materias_pagination.get_page(numero_pagina)
            return render(request, 'pages/list_materia.html', {'pagina': pagina})
        
        else:
            materias = Materias.objects.all().order_by('-id')
            materias_pagination = Paginator(materias, 5)
            numero_pagina = request.GET.get('page')
            pagina = materias_pagination.get_page(numero_pagina)

            return render(request, 'pages/list_materia.html', {'pagina': pagina})

    else: 
        pass

@login_required
def preview_materia(request, id):
    materia = Materias.objects.get(id=id)
    imagens = ImagensMaterias.objects.filter(materia=materia)
    textos = TextosMaterias.objects.filter(materia=materia)
    
    context = {'materia': materia, 'imagens': imagens, 'textos': textos}
    return render(request, 'pages/preview_materia.html', context)

@login_required
def edit_materia(request, id):
    materia = Materias.objects.get(id=id)
    if request.method == 'GET':
        form = FormCadastroMateria(instance=materia)

        context = {
            'form': form,
            'id': id,
        }
        return render(request, 'pages/edit_materia.html', context)

    else:
        form = FormCadastroMateria(request.POST, request.FILES, instance=materia)
        context = {
            'form': form,
            'id': id,
        }
        if form.is_valid():
                materia = form.save()

                manage_materia_url = reverse('manage_materia', args=[id])
                messages.success(request, "Modificações feitas e salvas com sucesso.")
                return redirect(manage_materia_url)

        else:
            messages.error(request, "Algum campo foi preenchido incorretamente. Corrija!")
            return render(request, 'pages/edit_materia.html', context)


@login_required
def manage_materia(request, id):
    if request.method == 'GET':
        materia = Materias.objects.get(id=id)
        imagens = ImagensMaterias.objects.filter(materia=materia).order_by('id')
        textos = TextosMaterias.objects.filter(materia=materia).order_by('id')

        context = {
            'id': id,
            'imagens': imagens,
            'textos': textos,
            'materia': materia,
        }
        return render(request, 'pages/manage_materia.html', context)


@login_required
def delete_materia(request, id):
    if request.method == 'GET':
        materia = Materias.objects.get(id=id)
        imagens = ImagensMaterias.objects.filter(materia=materia)
        if os.path.isfile(materia.capa.path):
            os.remove(materia.capa.path)
        for imagem in imagens:
            if os.path.isfile(imagem.imagem.path):
                os.remove(imagem.imagem.path)
        materia.delete()
        return redirect(list_materia)

@login_required
def add_imagem_materia(request, id):
    materia = Materias.objects.get(id=id)
    if request.method == 'GET':
        form = FormImagemMateria()

        context = {
            'form': form,
            'id': id,
        }

        return render(request, 'forms/add_imagem_materia.html', context)

    elif request.method == 'POST':
        form = FormImagemMateria(request.POST, request.FILES)

        context = {
            'form': form,
            'id': id, 
        }

        if form.is_valid():
            imagem = form.save(commit=False)
            imagem.materia = materia
            imagem.save()

            context = {
                'form': form,
                'id': id,
            }

            messages.success(request, "Imagem adicionada com sucesso!")
            return render(request, 'forms/add_imagem_materia.html', context)
        
        else: 
            messages.error(request, "Preencha os dados corretamente!")
            return render(request, 'forms/add_imagem_materia.html', context)

@login_required
def edit_imagem_materia(request, id):
    imagem = ImagensMaterias.objects.get(id=id)
    if request.method == 'GET':
        form = FormImagemMateria(instance=imagem)
        materia = request.GET.get('materia')

        context = {
            'form': form,
            'id': id,
            'materia': materia
        }

        return render(request, 'forms/edit_imagem_materia.html', context)
    
    elif request.method == 'POST':
        form = FormImagemMateria(request.POST, request.FILES, instance=imagem)
        materia = request.POST.get('materia')

        context = {
            'form': form,
            'id': id,
            'materia': materia
        }

        if form.is_valid():
            form.save()

            messages.success(request, "Alterações feitas com sucesso")
            return render(request, 'forms/edit_imagem_materia.html', context)
            """
                Mudar página de edição das matéria, 
                colocando uma página intermediaria que possibilita escole 
                se ele vai editar as informações gerais, 
                algum texto da matéria ou alguma imagem
            """
        else:
            messages.error(request, "Formulário preenchido incorretamente!")
            return render(request, 'forms/edit_imagem_materia.html', context)

@login_required
def delete_imagem_materia(request, id, im_id):
    imagem = ImagensMaterias.objects.get(id=im_id)
    if os.path.isfile(imagem.imagem.path):
        os.remove(imagem.imagem.path)
    
    imagem.delete()

    manage_materia_url = reverse('manage_materia', args=[id])
    messages.success(request, "Imagem removida com sucesso!")
    return redirect(manage_materia_url)

@login_required
def add_texto_materia(request, id):
    materia = Materias.objects.get(id=id)
    if request.method == 'GET':
        form = FormTextoMateria()

        context = {
            'form': form,
            'id': id,
        }

        return render(request, 'forms/add_texto_materia.html', context)

    elif request.method == 'POST':
        form = FormTextoMateria(request.POST)

        context = {
            'form': form,
            'id': id, 
        }

        if form.is_valid():
            texto = form.save(commit=False)
            texto.materia = materia
            texto.save()

            context = {
                'form': form,
                'id': id,
            }

            messages.success(request, "Texto adicionado com sucesso!")
            return render(request, 'forms/add_texto_materia.html', context)
        
        else: 
            messages.error(request, "Preencha os dados corretamente!")
            return render(request, 'forms/add_texto_materia.html', context)

@login_required
def edit_texto_materia(request, id):
    texto = TextosMaterias.objects.get(id=id)
    if request.method == 'GET':
        form = FormTextoMateria(instance=texto)
        materia = request.GET.get('materia')

        context = {
            'form': form,
            'id': id,
            'materia': materia
        }

        return render(request, 'forms/edit_texto_materia.html', context)
    
    elif request.method == 'POST':
        form = FormTextoMateria(request.POST, instance=texto)
        materia = request.POST.get('materia')

        context = {
            'form': form,
            'id': id,
            'materia': materia
        }

        if form.is_valid():
            form.save()

            messages.success(request, "Alterações feitas com sucesso")
            return render(request, 'forms/edit_texto_materia.html', context)
 
        else:
            messages.error(request, "Formulário preenchido incorretamente!")
            return render(request, 'forms/edit_texto_materia.html', context)

@login_required
def delete_texto_materia(request, id, tx_id):
    texto = TextosMaterias.objects.get(id=tx_id)
    texto.delete()

    manage_materia_url = reverse('manage_materia', args=[id])
    messages.success(request, "Tópico removido com sucesso!")
    return redirect(manage_materia_url)
    



