from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render , get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import login , logout , authenticate 
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST

def Login_Index_Function(request):
    return render(request , "index.html")


def admin_login_fun(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                # If the user is a superuser, log them in and redirect to Admin_dashboard
                login(request, user)
                return redirect('admin_dashboard')

            try:
                sub_admin_profile = Sub_Admin_Table.objects.get(user=user)
                
                if sub_admin_profile.is_sub_admin:
                    # If the user is a sub-admin, log them in and redirect to Admin_dashboard
                    login(request, user)
                    return redirect('admin_dashboard')
                else:
                    return render(request, 'index.html', {'error_message': 'Not authorized.'})
            except Sub_Admin_Table.DoesNotExist:
                return render(request, 'index.html', {'error_message': 'User Not Belongs To Sub Admin'})
        else:
            return render(request, 'index.html', {'error_message': 'Invalid username or password.'})

    return render(request , "index.html")


def admin_logout(request):
    logout(request)
    return redirect('admin_login_fun')


def admin_dashboard(request):
    return render(request , "admin/admin_dashboard.html")

def sub_admin_creation(request):
    if request.method == 'POST':
        
        employee_name = request.POST.get('employee_name')
        employee_email = request.POST.get('employee_email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username already exists'})

        
        user = User.objects.create_user(username=username, email=employee_email, password=password)
        user.first_name = employee_name
        user.save()

        
        subadmin = Sub_Admin_Table(user=user, is_sub_admin=True , created_by = request.user)
        subadmin.save()

        return JsonResponse({'success': True, 'message': 'Sub-admin created successfully'})
    return render(request , "admin/subadmin_creation.html")

def list_subadmins(request):
    subadmins = Sub_Admin_Table.objects.filter(is_sub_admin=True).order_by('-id')
    context = {
        'subadmins': subadmins
    }
    return render(request, 'admin/sub_admin_lists.html', context)

def deactivate_sub_admin_account(request):
    if request.method == 'POST':
        record_id = request.POST.get('record_id')        
        try:
            hr = Sub_Admin_Table.objects.get(pk=record_id)
            user = hr.user

            if user.is_active:
                user.is_active = False
                user.save()
                return JsonResponse({'success': True, 'message': 'Account deactivated successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Account is already deactivated'})

        except Sub_Admin_Table.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Sub_Admin_Table object does not exist'})
        
def activate_sub_admin_account(request):
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        try:
            hr = Sub_Admin_Table.objects.get(pk=record_id)
            user = hr.user

            if user.is_active:
                return JsonResponse({'success': False, 'message': 'Account is already active'})
            else:
                user.is_active = True
                user.save()
                return JsonResponse({'success': True, 'message': 'Account activated successfully'})

        except Sub_Admin_Table.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Sub_Admin_Table object does not exist'})


def edit_sub_admin_details(request, subadmin_id):
    subadmin = get_object_or_404(Sub_Admin_Table, id=subadmin_id)
    response_data = {'success': False, 'message': 'Invalid request'}
    
    if request.method == 'POST':
        try:
            employee_name = request.POST.get('employee_name')
            employee_email = request.POST.get('employee_email')
            username = request.POST.get('username')


            subadmin.user.first_name = employee_name
            subadmin.user.email = employee_email
            subadmin.user.username = username

            subadmin.user.save()
            subadmin.save()
            
            response_data = {'success': True, 'message': 'Sub-admin updated successfully'}
        except Exception as e:
            response_data = {'success': False, 'message': str(e)}

        return JsonResponse(response_data)

    context = {
        'subadmin': subadmin
    }
    return render(request , "admin/edit_sub_admin.html" , context)


def manager_creation(request):
    if request.method == 'POST':
        
        hr_name = request.POST.get('hr_name')
        hr_email = request.POST.get('hr_email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username already exists'})

        
        user = User.objects.create_user(username=username, email=hr_email, password=password , is_staff = True)
        user.first_name = hr_name
        user.save()

        
        hr = Manager_Table(user=user , created_by = request.user)
        hr.save()

        return JsonResponse({'success': True, 'message': 'Manager created successfully'})
    return render(request , "admin/manager_creation.html")

def manager_lists(request):
    
    hr_objects = Manager_Table.objects.filter(user__is_staff=True)
    context = {
        'hr_lists': hr_objects
    }
    return render(request, 'admin/manager_lists.html', context)


def edit_manager_details(request, hr_id):
    hr_object = get_object_or_404(Manager_Table, id=hr_id)
    response_data = {'success': False, 'message': 'Invalid request'}
    
    if request.method == 'POST':
        try:
            hr_name = request.POST.get('hr_name')
            hr_email = request.POST.get('hr_email')
            username = request.POST.get('username')


            hr_object.user.first_name = hr_name
            hr_object.user.email = hr_email
            hr_object.user.username = username

            hr_object.user.save()
            hr_object.save()
            
            response_data = {'success': True, 'message': 'Manager Details updated successfully'}
        except Exception as e:
            response_data = {'success': False, 'message': str(e)}

        return JsonResponse(response_data)

    context = {
        'hr_object': hr_object
    }
    return render(request , "admin/edit_hr.html" , context)

def deactivate_manager_account(request):
    if request.method == 'POST':
        record_id = request.POST.get('record_id')        
        try:
            hr = Manager_Table.objects.get(pk=record_id)
            user = hr.user

            if user.is_active:
                user.is_active = False
                user.save()
                return JsonResponse({'success': True, 'message': 'Account deactivated successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Account is already deactivated'})

        except Manager_Table.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Manager_Table object does not exist'})
        
def activate_manager_account(request):
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        try:
            hr = Manager_Table.objects.get(pk=record_id)
            user = hr.user

            if user.is_active:
                return JsonResponse({'success': False, 'message': 'Account is already active'})
            else:
                user.is_active = True
                user.save()
                return JsonResponse({'success': True, 'message': 'Account activated successfully'})

        except Manager_Table.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Manager_Table object does not exist'})
        
