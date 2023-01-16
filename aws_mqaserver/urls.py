"""aws_mqaserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from aws_mqaserver.views import downloadLevelContent
from aws_mqaserver.views import downloadCheckList
from aws_mqaserver.views import donwnloadVisitHistory
from aws_mqaserver.views import uploadVisit
from aws_mqaserver.views import upload_record_excel
from aws_mqaserver.views import upload_mil_excel
from aws_mqaserver.views import upload_image_video
from aws_mqaserver.views import upload_mil_to_tableau
# from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

import aws_mqaserver.apis.user
import aws_mqaserver.apis.line
import aws_mqaserver.apis.line_config
import aws_mqaserver.apis.check_list
import aws_mqaserver.apis.check_list_item
import aws_mqaserver.apis.audit_item
import aws_mqaserver.apis.kappa_item
import aws_mqaserver.apis.oba_item
import aws_mqaserver.apis.mil_item
import aws_mqaserver.apis.file

urlpatterns = [

    path('login', aws_mqaserver.apis.user.login),
    path('add_user', aws_mqaserver.apis.user.add_user),
    path('get_users_page', aws_mqaserver.apis.user.get_users_page),
    path('delete_user', aws_mqaserver.apis.user.delete_user),
    path('refresh_user', aws_mqaserver.apis.user.refresh_user),
    path('change_user_role', aws_mqaserver.apis.user.change_user_role),
    path('update_user_status', aws_mqaserver.apis.user.update_user_status),
    path('reset_user_password', aws_mqaserver.apis.user.reset_user_password),
    path('user_change_password', aws_mqaserver.apis.user.user_change_password),

    path('add_line', aws_mqaserver.apis.line.add_line),
    path('get_lines_page', aws_mqaserver.apis.line.get_lines_page),
    path('get_level_lines', aws_mqaserver.apis.line.get_level_lines),
    path('delete_line', aws_mqaserver.apis.line.delete_line),
    path('get_lines_tree', aws_mqaserver.apis.line.get_lines_tree),

    path('update_line_config', aws_mqaserver.apis.line_config.update_line_config),
    path('get_line_configs_page', aws_mqaserver.apis.line_config.get_line_configs_page),
    path('find_line_config_by_id', aws_mqaserver.apis.line_config.find_line_config_by_id),
    path('find_line_config', aws_mqaserver.apis.line_config.find_line_config),
    path('delete_line_config_item', aws_mqaserver.apis.line_config.delete_line_config_item),

    path('upload_check_list', aws_mqaserver.apis.check_list.upload_check_list),
    path('find_check_list', aws_mqaserver.apis.check_list.find_check_list),
    path('get_check_lists_page', aws_mqaserver.apis.check_list.get_check_lists_page),
    path('delete_check_list', aws_mqaserver.apis.check_list.delete_check_list),
    path('get_check_list_items_page', aws_mqaserver.apis.check_list_item.get_check_list_items_page),
    path('get_check_list_items', aws_mqaserver.apis.check_list_item.get_check_list_items),

    path('upload_audit_item', aws_mqaserver.apis.audit_item.upload_audit_item),
    path('upload_kappa_item', aws_mqaserver.apis.kappa_item.upload_kappa_item),
    path('get_kappa_items_for_year', aws_mqaserver.apis.kappa_item.get_kappa_items_for_year),
    path('upload_oba_item', aws_mqaserver.apis.oba_item.upload_oba_item),
    path('get_oba_items_for_year', aws_mqaserver.apis.oba_item.get_oba_items_for_year),

    path('get_mil_items_page', aws_mqaserver.apis.mil_item.get_mil_items_page),
    path('update_mil_item', aws_mqaserver.apis.mil_item.update_mil_item),
    path('delete_mil_item', aws_mqaserver.apis.mil_item.delete_mil_item),

    path('download_file', aws_mqaserver.apis.file.download_file),

    path('admin/', admin.site.urls),
    path('downloadCheckList/', downloadCheckList),
    path('downloadLevelContent/', downloadLevelContent),
    path('donwnloadVisitHistory/', donwnloadVisitHistory),
    path('uploadVisit/', uploadVisit),
    path('upload_record_excel/', upload_record_excel),
    path('upload_mil_excel/', upload_mil_excel),
    path('upload_image_video/', upload_image_video),
    path('upload_mil_to_tableau/', upload_mil_to_tableau),

]
