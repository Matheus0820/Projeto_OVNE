from django.urls import path
from .views import (
                    login, controller, add_video, 
                    logout, list_video, add_materia, 
                    list_materia, delete_video, delete_materia, 
                    edit_video, edit_materia, manage_materia,  preview_materia,
                    add_imagem_materia, edit_imagem_materia, delete_imagem_materia,
                    add_texto_materia, edit_texto_materia, delete_texto_materia,
                    add_user, list_users, delete_user, info_user, profile_user, alterar_senha
                    )

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('', controller, name="controller"),
    path('add_video/', add_video, name="add_video"),
    path('list_video/', list_video, name="list_video"),
    path('edit_video/<int:id>/', edit_video, name="edit_video"),
    path('delete_video/<int:id>/', delete_video, name="delete_video"),
    path('add_materia/', add_materia, name="add_materia"),
    path('list_materia/', list_materia, name="list_materia"),
    path('preview/<int:id>/', preview_materia, name="preview_materia"),
    path('edit_materia/<int:id>/', edit_materia, name="edit_materia"),
    path('manage_materia/<int:id>/', manage_materia, name="manage_materia"),
    path('delete_materia/<int:id>/', delete_materia, name="delete_materia"),
    path('add_imagem_materia/<int:id>/', add_imagem_materia, name="add_imagem_materia"),
    path('edit_imagem_materia/<int:id>/', edit_imagem_materia, name="edit_imagem_materia"),
    path('delete_imagem_materia/<int:id>/<int:im_id>/', delete_imagem_materia, name="delete_imagem_materia"),
    path('add_texto_materia/<int:id>/', add_texto_materia, name="add_texto_materia"),
    path('edit_texto_materia/<int:id>/', edit_texto_materia, name="edit_texto_materia"),
    path('delete_texto_materia/<int:id>/<int:tx_id>/', delete_texto_materia, name="delete_texto_materia"),
    path('add_user/', add_user, name="add_user"),
    path('list_users/', list_users, name="list_users"),
    path('info_user/<int:id>/', info_user, name="info_user"),
    path('delete_user/<int:id>/', delete_user, name="delete_user"),
    path('profile/', profile_user, name="profile"),
    path('alterar_senha/', alterar_senha, name="alterar_senha"),
   
    
]