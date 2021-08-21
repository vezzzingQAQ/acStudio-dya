from os import name
from django.urls import path
from zusers import views
#users/
urlpatterns=[
    path("registerPage",views.register_page,name="registerpage"),
    path("registerAction",views.register_action,name="registeraction"),
    path("loginPage",views.login_page,name="loginpage"),
    path("loginAction",views.login_action,name="loginaction"),

    path("logoutAction",views.logout_action,name="logoutaction"),

    path("changeUserSettingsPage",views.change_user_settings_page,name="changeusersettingspage"),
    path("changeUserSettingsAction",views.change_user_settings_action,name="changeusersettinsaction"),

    path("showUserInfoPage/<int:userId>/<int:currentPage>",views.show_user_info_page,name="showuserinfopage"),
]