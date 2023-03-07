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

import aws_mqaserver.apis.test

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
import aws_mqaserver.apis.box

import aws_mqaserver.team_MDE.apis.line
import aws_mqaserver.team_MDE.apis.check_list
import aws_mqaserver.team_MDE.apis.check_list_item
import aws_mqaserver.team_MDE.apis.audit_item

import aws_mqaserver.team_Accessory.apis.line
import aws_mqaserver.team_Accessory.apis.check_list
import aws_mqaserver.team_Accessory.apis.check_list_item
import aws_mqaserver.team_Accessory.apis.audit_item

import aws_mqaserver.team_Display.apis.line
import aws_mqaserver.team_Display.apis.line_config
import aws_mqaserver.team_Display.apis.check_list
import aws_mqaserver.team_Display.apis.check_list_item
import aws_mqaserver.team_Display.apis.audit_item
import aws_mqaserver.team_Display.apis.mil_item

import aws_mqaserver.team_SIP.apis.line
import aws_mqaserver.team_SIP.apis.line_config
import aws_mqaserver.team_SIP.apis.check_list
import aws_mqaserver.team_SIP.apis.check_list_item
import aws_mqaserver.team_SIP.apis.audit_item
import aws_mqaserver.team_SIP.apis.mil_item

urlpatterns = [

    path('test', aws_mqaserver.apis.test.test),

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
    path('get_check_lists_page', aws_mqaserver.apis.check_list.get_check_lists_page),
    path('delete_check_list', aws_mqaserver.apis.check_list.delete_check_list),
    path('get_check_list_items_page', aws_mqaserver.apis.check_list_item.get_check_list_items_page),
    path('get_check_list_items', aws_mqaserver.apis.check_list_item.get_check_list_items),
    path('export_check_list_items', aws_mqaserver.apis.check_list_item.export_check_list_items),

    path('upload_audit_item', aws_mqaserver.apis.audit_item.upload_audit_item),
    path('upload_kappa_item', aws_mqaserver.apis.kappa_item.upload_kappa_item),
    path('get_kappa_items_for_year', aws_mqaserver.apis.kappa_item.get_kappa_items_for_year),
    path('upload_oba_item', aws_mqaserver.apis.oba_item.upload_oba_item),
    path('get_oba_items_for_year', aws_mqaserver.apis.oba_item.get_oba_items_for_year),

    path('get_mil_items_page', aws_mqaserver.apis.mil_item.get_mil_items_page),
    path('update_mil_item', aws_mqaserver.apis.mil_item.update_mil_item),
    path('delete_mil_item', aws_mqaserver.apis.mil_item.delete_mil_item),

    path('download_file', aws_mqaserver.apis.file.download_file),

    path('box_test', aws_mqaserver.apis.box.box_test),
    path('box_get_authorization', aws_mqaserver.apis.box.box_get_authorization),

    path('admin/', admin.site.urls),
    path('downloadCheckList/', downloadCheckList),
    path('downloadLevelContent/', downloadLevelContent),
    path('donwnloadVisitHistory/', donwnloadVisitHistory),
    path('uploadVisit/', uploadVisit),
    path('upload_record_excel/', upload_record_excel),
    path('upload_mil_excel/', upload_mil_excel),
    path('upload_image_video/', upload_image_video),
    path('upload_mil_to_tableau/', upload_mil_to_tableau),


    # MDE

    path('mde/add_line', aws_mqaserver.team_MDE.apis.line.add_line),
    path('mde/get_lines_page', aws_mqaserver.team_MDE.apis.line.get_lines_page),
    path('mde/get_level_lines', aws_mqaserver.team_MDE.apis.line.get_level_lines),
    path('mde/delete_line', aws_mqaserver.team_MDE.apis.line.delete_line),
    path('mde/get_lines_tree', aws_mqaserver.team_MDE.apis.line.get_lines_tree),

    path('mde/upload_check_list', aws_mqaserver.team_MDE.apis.check_list.upload_check_list),
    path('mde/get_check_lists_page', aws_mqaserver.team_MDE.apis.check_list.get_check_lists_page),
    path('mde/delete_check_list', aws_mqaserver.team_MDE.apis.check_list.delete_check_list),
    path('mde/get_check_list_items_page', aws_mqaserver.team_MDE.apis.check_list_item.get_check_list_items_page),
    path('mde/get_check_list_items', aws_mqaserver.team_MDE.apis.check_list_item.get_check_list_items),
    path('mde/export_check_list_items', aws_mqaserver.team_MDE.apis.check_list_item.export_check_list_items),

    path('mde/upload_audit_item', aws_mqaserver.team_MDE.apis.audit_item.upload_audit_item),

    # Accessory

    path('accessory/add_line', aws_mqaserver.team_Accessory.apis.line.add_line),
    path('accessory/get_lines_page', aws_mqaserver.team_Accessory.apis.line.get_lines_page),
    path('accessory/get_level_lines', aws_mqaserver.team_Accessory.apis.line.get_level_lines),
    path('accessory/delete_line', aws_mqaserver.team_Accessory.apis.line.delete_line),
    path('accessory/get_lines_tree', aws_mqaserver.team_Accessory.apis.line.get_lines_tree),

    path('accessory/upload_check_list', aws_mqaserver.team_Accessory.apis.check_list.upload_check_list),
    path('accessory/get_check_lists_page', aws_mqaserver.team_Accessory.apis.check_list.get_check_lists_page),
    path('accessory/delete_check_list', aws_mqaserver.team_Accessory.apis.check_list.delete_check_list),
    path('accessory/get_check_list_items_page', aws_mqaserver.team_Accessory.apis.check_list_item.get_check_list_items_page),
    path('accessory/get_check_list_items', aws_mqaserver.team_Accessory.apis.check_list_item.get_check_list_items),
    path('accessory/export_check_list_items', aws_mqaserver.team_Accessory.apis.check_list_item.export_check_list_items),

    path('accessory/upload_audit_item', aws_mqaserver.team_Accessory.apis.audit_item.upload_audit_item),


    # Display

    path('display/add_line', aws_mqaserver.team_Display.apis.line.add_line),
    path('display/get_lines_page', aws_mqaserver.team_Display.apis.line.get_lines_page),
    path('display/get_level_lines', aws_mqaserver.team_Display.apis.line.get_level_lines),
    path('display/delete_line', aws_mqaserver.team_Display.apis.line.delete_line),
    path('display/get_lines_tree', aws_mqaserver.team_Display.apis.line.get_lines_tree),

    path('display/upload_check_list', aws_mqaserver.team_Display.apis.check_list.upload_check_list),
    path('display/get_check_lists_page', aws_mqaserver.team_Display.apis.check_list.get_check_lists_page),
    path('display/delete_check_list', aws_mqaserver.team_Display.apis.check_list.delete_check_list),
    path('display/get_check_list_items_page', aws_mqaserver.team_Display.apis.check_list_item.get_check_list_items_page),
    path('display/get_check_list_items', aws_mqaserver.team_Display.apis.check_list_item.get_check_list_items),
    path('display/export_check_list_items', aws_mqaserver.team_Display.apis.check_list_item.export_check_list_items),

    path('display/upload_audit_item', aws_mqaserver.team_Display.apis.audit_item.upload_audit_item),
    path('display/get_mil_items_page', aws_mqaserver.team_Display.apis.mil_item.get_mil_items_page),
    path('display/update_mil_item', aws_mqaserver.team_Display.apis.mil_item.update_mil_item),
    path('display/delete_mil_item', aws_mqaserver.team_Display.apis.mil_item.delete_mil_item),

    path('display/update_line_config', aws_mqaserver.team_Display.apis.line_config.update_line_config),
    path('display/get_line_configs_page', aws_mqaserver.team_Display.apis.line_config.get_line_configs_page),
    path('display/find_line_config_by_id', aws_mqaserver.team_Display.apis.line_config.find_line_config_by_id),
    path('display/find_line_config', aws_mqaserver.team_Display.apis.line_config.find_line_config),
    path('display/delete_line_config_item', aws_mqaserver.team_Display.apis.line_config.delete_line_config_item),

    # SIP

    path('sip/add_line', aws_mqaserver.team_SIP.apis.line.add_line),
    path('sip/get_lines_page', aws_mqaserver.team_SIP.apis.line.get_lines_page),
    path('sip/get_level_lines', aws_mqaserver.team_SIP.apis.line.get_level_lines),
    path('sip/delete_line', aws_mqaserver.team_SIP.apis.line.delete_line),
    path('sip/get_lines_tree', aws_mqaserver.team_SIP.apis.line.get_lines_tree),

    path('sip/upload_check_list', aws_mqaserver.team_SIP.apis.check_list.upload_check_list),
    path('sip/get_check_lists_page', aws_mqaserver.team_SIP.apis.check_list.get_check_lists_page),
    path('sip/delete_check_list', aws_mqaserver.team_SIP.apis.check_list.delete_check_list),
    path('sip/get_check_list_items_page', aws_mqaserver.team_SIP.apis.check_list_item.get_check_list_items_page),
    path('sip/get_check_list_items', aws_mqaserver.team_SIP.apis.check_list_item.get_check_list_items),
    path('sip/export_check_list_items', aws_mqaserver.team_SIP.apis.check_list_item.export_check_list_items),

    path('sip/upload_audit_item', aws_mqaserver.team_SIP.apis.audit_item.upload_audit_item),
    path('sip/get_mil_items_page', aws_mqaserver.team_SIP.apis.mil_item.get_mil_items_page),
    path('sip/update_mil_item', aws_mqaserver.team_SIP.apis.mil_item.update_mil_item),
    path('sip/delete_mil_item', aws_mqaserver.team_SIP.apis.mil_item.delete_mil_item),

    path('sip/update_line_config', aws_mqaserver.team_SIP.apis.line_config.update_line_config),
    path('sip/get_line_configs_page', aws_mqaserver.team_SIP.apis.line_config.get_line_configs_page),
    path('sip/find_line_config_by_id', aws_mqaserver.team_SIP.apis.line_config.find_line_config_by_id),
    path('sip/find_line_config', aws_mqaserver.team_SIP.apis.line_config.find_line_config),
    path('sip/delete_line_config_item', aws_mqaserver.team_SIP.apis.line_config.delete_line_config_item),
]
