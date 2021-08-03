from datetime import datetime

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.admin import CategoryAdmin
from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse

from django.http import HttpResponse


def index(request):
    # cookie test
    request.session.set_test_cookie()
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # context_dict={'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!'}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    # context_dict={'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!', 'categories': Category_list}
    # context_dict={'categories': Category_list}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    # ??? it should not use here cuz it only count the view times of about.html???
    visitor_cookie_handler(request)
    # context_dict['visits'] = int(request.session['visits'])
    # context_dict['visits'] = request.COOKIES.get('visits', '1')

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # cookie test
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    # context_dict={'aboutmessage':'This is about message: goodluck and have a nice day!'}
    print(request.method)
    print(request.user)
    visitor_cookie_handler(request)
    return render(request, 'rango/about.html', {'visits':request.session['visits']})


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.view = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))

        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


# def register(request):
#     # boolean表示注册是否成功
#     registered = False
#
#     # 如果是post请求，储存数据
#     if request.method == 'POST':
#         # 获取原始表单数据
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             # 将user表单数据存入数据库
#             user = user_form.save()
#             # 调用set_password方法，计算对应加密后的密码哈希
#             user.set_password(user.password)
#             user.save()
#             # 处理profile
#             # 自行处理，commit为false，延迟保存，避免数据完整性问题(need add user element)
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#             registered = True  # 完成注册，设为true
#         # 如果表单数据有误，打印错误
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:  # 如果不是post，渲染两个表单让用户填写注册
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     # 调用render渲染模板
#     return render(request, 'rango/register.html',
#                   context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


# def user_login(request):
#     # We use request.POST.get('<variable>') as opposed
#     # to request.POST['<variable>'], because the
#     # request.POST.get('<variable>') returns None if the
#     # value does not exist, while request.POST['<variable>']
#     # will raise a KeyError exception.
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # 检查username和psw是否有效
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect(reverse('rango:index'))  # response 302, not 200
#             else:
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             print(f"Invalid login details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")
#     else:
#         return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect(reverse('rango:index'))


# visit site counter// Chapter 10.5
# def visitor_cookie_handler(request, response):
#     # all cookie values are returned as strings
#     visits = int(request.COOKIES.get('visits', '1'))
#     # visits = request.COOKIES.get('visits', 1)
#     last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
#     if (datetime.now() - last_visit_time).seconds > 0:
#         visits = visits + 1
#         # Update the last visit cookie now that we have updated the count
#         response.set_cookie('last_visit', str(datetime.now()))
#     else:
#         # Set the last visit cookie
#         response.set_cookie('last_visit', last_visit_cookie)
#
#     # Update/set the visits cookie
#     response.set_cookie('visits', visits)


def visitor_cookie_handler(request):
    # all cookie values are returned as strings
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits


# get cookie from server
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

