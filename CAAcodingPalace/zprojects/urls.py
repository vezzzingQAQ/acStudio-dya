from django.urls import path
from zprojects import views

urlpatterns=[
    #path("listProjects",views.register_page,name="listprojects"),
    path("indexPage/<int:currentPage>",views.index_page,name="indexpage"),

    path("addProjectPage",views.add_project_page,name="addprojectpage"),
    path("addProjectAction",views.add_project_action,name="addprojectaction"),

    path("deleteProjectAction/<int:projectId>",views.delete_project_action,name="deleteprojectaction"),

    path("showProjectPage/<int:projectId>",views.show_project_page,name="showprojectpage"),

    path("addCommentAction",views.add_comment_action,name="addcommentaction"),
]