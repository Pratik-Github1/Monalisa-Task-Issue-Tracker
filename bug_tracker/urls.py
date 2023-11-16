
from django.contrib import admin
from django.urls import path , include
from tracker_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Login_Index_Function, name="Index_function") ,
    path('admin-login/', views.admin_login_fun , name="admin_login_fun") ,
    path('admin-logout/', views.admin_logout , name="admin_logout") ,
    path('admin-dashboard/', views.admin_dashboard , name="admin_dashboard"),
    
    path('sub-admin_creation/', views.sub_admin_creation , name="sub_admin_creation") ,
    path('list-subadmins/', views.list_subadmins , name="list_subadmins") ,
    path('subadmins/edit/<int:subadmin_id>/', views.edit_sub_admin_details, name='edit_sub_admin_details'),
    
    path('deactivate-sub_admin_account/', views.deactivate_sub_admin_account, name='deactivate_sub_admin_account'),
    path('activate-sub_admin_account/', views.activate_sub_admin_account, name='activate_sub_admin_account'),
    
    path('admin-logout/', views.admin_logout , name="admin_logout") ,
    
    path('manager-creation/', views.manager_creation , name="manager_creation") ,
    path('manager-lists/', views.manager_lists , name="manager_lists") ,
    path('Manager-edit/<int:hr_id>/', views.edit_manager_details, name='edit_manager_details'),
    
    path('deactivate_manager_account/', views.deactivate_manager_account, name='deactivate_manager_account'),
    path('activate_manager_account/', views.activate_manager_account, name='activate_manager_account'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)