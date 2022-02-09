from django.urls import path, re_path
from django.contrib.auth import views as auth_views


from .views import (homepage_view, dashboard_view, logout_request, update_profile_view,
                    manage_instagram_links_view, update_company_info_view, company_info_view, login_or_register_view,
                    ResetPasswordView

                    )

from .action_views import (validate_category_creation_view, validate_link_creation_view, edit_category_view,
                           edit_link_view, delete_category_or_link_view, validate_company_create_product_or_service_view,
                           validate_login_form_view, validate_register_form_view,
                           validate_company_create_image_view, update_company_image_view, delete_company_image_view
                           )
from .admin_view import ManageSubsView

app_name = 'accounts'

urlpatterns = [

    path('admin/manage-subs/', ManageSubsView.as_view(), name='manageSubsView'),

    path('homepage/', homepage_view, name='homepage_view'),
    path('register/', login_or_register_view, name='register'),
    path('logout/', logout_request, name='logout'),

    path('dashboard/', dashboard_view, name='dashboard_view'),
    path('update-profile/', update_profile_view, name='update-profile'),
    path('manage-instagram/<str:slug>/', manage_instagram_links_view, name='manage_links'),
    path('update-company-info/<str:slug>/', company_info_view, name='update_company_info'),
    path('update-company/<int:pk>/', update_company_info_view, name='update_company_data'),

    path('action/create/link/<str:slug>/', validate_link_creation_view, name='validate_create_link'),
    path('action/create/category/<str:slug>/', validate_category_creation_view, name='validate_create_category'),
    path('action/edit/link/<int:pk>/', edit_link_view, name='edit_link'),
    path('action/edit/category/<int:pk>/', edit_category_view, name='edit_category'),
    path('action/delete/<str:action>/<int:pk>/', delete_category_or_link_view, name='delete_link_or_category'),
    path('action/validate/create-product-or-service/<str:slug>/<slug:action>/',
         validate_company_create_product_or_service_view,
         name='validate_product_or_service'
         ),

    path('action/validate/login/', validate_login_form_view, name='validate_login'),
    path('action/validate/register/', validate_register_form_view, name='validate_register'),

    path('action/validate-company-create-image/<str:slug>/', validate_company_create_image_view, name='create_company_image'),
    path('action/update-company-image/<int:pk>/', update_company_image_view, name='update_company_image'),
    path('action/delete-company-image/<int:pk>/', delete_company_image_view, name='delete_company_image'),


    # passwords resets etc
    path('reset-password', ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='auth_templates/change_password.html'),
         name='change_password'),






]