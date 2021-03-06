from datetime import datetime

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View

from rango.admin import CategoryAdmin
from django.http.response import HttpResponseForbidden
from django.shortcuts import render

from rango.bing_search import run_query
from rango.models import Category, UserView, UserLike, UserProfile
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


def index(request):
    # cookie test
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}

    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    visitor_cookie_handler(request)
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # cookie test
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    print(request.method)
    print(request.user)
    visitor_cookie_handler(request)
    return render(request, 'rango/about.html', {'visits': request.session['visits']})


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)
        # Check whether user already liked this category or not
        # category_liked = False
        if request.user.is_authenticated:
            # user_id = request.user.id
            # category_id = category.id
            # category_liked = UserLike.objects.filter(user_id=user_id, category_id=category_id).exists()
            category_liked = is_user_liked_category(request.user.id, category.id)
        else:
            category_liked = False

        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_liked'] = category_liked

    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
        context_dict['category_liked'] = False

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        # form = CategoryForm(request.POST)
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=True)
            form.thumbnail = form.cleaned_data['thumbnail']
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
        # form = PageForm(request.POST)
        form = PageForm(request.POST, request.FILES)
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


@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    context_dict = {'form': form}
    return render(request, 'rango/profile_registration.html', context_dict)


class AboutView(View):
    def get(self, request):
        context_dict = {}

        visitor_cookie_handler(request)
        context_dict['visits'] = request.session['visits']
        return render(request, 'rango/about.html', context_dict)


class AddCategoryView(View):
    @method_decorator(login_required())
    def get(self, request):
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})

    @method_decorator(login_required())
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
        return render(request, 'rango/add_category.html', {'form': form})


class ProfileView(View):
    # @login_required
    # def get_like(self, request):
    #     user_id = request.user.id
    #     # get most recent 5 like categories (since the id is auto increment, the biggest one is added most recently)
    #     ulikes = UserLike.objects.filter(user_id=user_id).order_by('-id')[:5]
    #
    #     category_list = [x.category for x in ulikes]
    #     context_dict = {}
    #
    #     context_dict['categories'] = category_list
    #     # return render(request, 'rango/profile.html', context=context_dict)
    #     return context_dict

    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                                'picture': user_profile.picture})
        return user, user_profile, form

    @method_decorator(login_required)
    def get(self, request, username):

        try:
            # context_dict = self.get_like(request)
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        # context_dict['user_profile'] = user_profile
        # context_dict['selected_user'] = user
        # context_dict['form'] = form

        user_id = request.user.id
        # get most recent 5 like categories (since the id is auto increment, the biggest one is added most recently)
        ulikes = UserLike.objects.filter(user_id=user_id).order_by('-id')[:5]

        category_list = [x.category for x in ulikes]

        context_dict = {'categories': category_list,
                        'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'rango/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'rango/profile.html', context_dict)


# @login_required
# def register_profile(request):
#     form = UserProfileForm()
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             user_profile = form.save(commit=False)
#             user_profile.user = request.user
#             user_profile.save()
#             return redirect(reverse('rango:index'))
#         else:
#             print(form.errors)
#
#     context_dict = {'form': form}
#     return render(request, 'rango/profile_registration.html', context_dict)


# @login_required
# def restricted(request):
#     return render(request, 'rango/restricted.html')


# @login_required
# def show_user_likes(request, username):
#     context_dict = {}
#     try:
#         user_likes = UserLike.objects.filter(username=username)
#
#         context_dict['likes'] = user_likes
#
#     except Category.DoesNotExist:
#         context_dict['likes'] = None
#     return render(request, 'rango/user_likes.html', context=context_dict)


@login_required
def show_user_views(request, username):
    context_dict = {}
    try:
        user_views = UserView.objects.filter(username=username)

        context_dict['views'] = user_views

    except Category.DoesNotExist:
        context_dict['views'] = None
    return render(request, 'rango/user_views.html', context=context_dict)


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


# like category view
class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        category_id = request.GET['category_id']
        user_id = request.user.id
        category_liked = is_user_liked_category(user_id, category_id)

        try:
            category = Category.objects.get(id=int(category_id))
            check = str(user_id) + '_' + str(category_id)
            ulike = UserLike.objects.get_or_create(user_id=user_id, category_id=category_id, check=check)[0]
            ulike.save()
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        # category.likes = category.likes + 1
        # category.save()
        # Only increment the like in category table if the category is firstly liked by the login user
        if not category_liked:
            category.likes = category.likes + 1
            category.save()

        return HttpResponse(category.likes)


# @login_required
# def profile(request):
#     user_id = request.user.id
#     # get most recent 5 like categories (since the id is auto increment, the biggest one is added most recently)
#     ulikes = UserLike.objects.filter(user_id=user_id).order_by('-id')[:5]
#
#     category_list = [x.category for x in ulikes]
#     context_dict = {}
#
#     context_dict['categories'] = category_list
#     # return render(request, 'rango/profile.html', context=context_dict)
#     return render(request, 'rango/profile.html', context=context_dict)

# Check whether the user liked the category or not


def is_user_liked_category(user_id, category_id):
    return UserLike.objects.filter(user_id=user_id, category_id=category_id).exists()

    # def about(request):


#     # cookie test
#     if request.session.test_cookie_worked():
#         print("TEST COOKIE WORKED!")
#         request.session.delete_test_cookie()
#     # context_dict={'aboutmessage':'This is about message: goodluck and have a nice day!'}
#     print(request.method)
#     print(request.user)
#     visitor_cookie_handler(request)
#     return render(request, 'rango/about.html', {'visits': request.session['visits']})
#
#
# def show_category(request, category_name_slug):
#     context_dict = {}
#     try:
#         # Can we find a category name slug with the given name?
#         # If we can't, the .get() method raises a DoesNotExist exception.
#         # The .get() method returns one model instance or raises an exception.
#         category = Category.objects.get(slug=category_name_slug)
#
#         pages = Page.objects.filter(category=category)
#
#         context_dict['pages'] = pages
#         context_dict['category'] = category
#
#     except Category.DoesNotExist:
#         context_dict['pages'] = None
#         context_dict['category'] = None
#
#     return render(request, 'rango/category.html', context_dict)
#
#
# @login_required
# def add_category(request):
#     form = CategoryForm()
#
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#
#         if form.is_valid():
#             form.save(commit=True)
#             return redirect(reverse('rango:index'))
#         else:
#             print(form.errors)
#     return render(request, 'rango/add_category.html', {'form': form})
#
#
# @login_required
# def add_page(request, category_name_slug):
#     try:
#         category = Category.objects.get(slug=category_name_slug)
#     except Category.DoesNotExist:
#         category = None
#     if category is None:
#         return redirect(reverse('rango:index'))
#
#     form = PageForm()
#
#     if request.method == 'POST':
#         form = PageForm(request.POST)
#         if form.is_valid():
#             if category:
#                 page = form.save(commit=False)
#                 page.category = category
#                 page.view = 0
#                 page.save()
#                 return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
#
#         else:
#             print(form.errors)
#
#     context_dict = {'form': form, 'category': category}
#     return render(request, 'rango/add_page.html', context=context_dict)
#
#
# # def register(request):
# #     # boolean????????????????????????
# #     registered = False
# #
# #     # ?????????post?????????????????????
# #     if request.method == 'POST':
# #         # ????????????????????????
# #         user_form = UserForm(request.POST)
# #         profile_form = UserProfileForm(request.POST)
# #
# #         if user_form.is_valid() and profile_form.is_valid():
# #             # ???user???????????????????????????
# #             user = user_form.save()
# #             # ??????set_password?????????????????????????????????????????????
# #             user.set_password(user.password)
# #             user.save()
# #             # ??????profile
# #             # ???????????????commit???false?????????????????????????????????????????????(need add user element)
# #             profile = profile_form.save(commit=False)
# #             profile.user = user
# #
# #             if 'picture' in request.FILES:
# #                 profile.picture = request.FILES['picture']
# #
# #             profile.save()
# #             registered = True  # ?????????????????????true
# #         # ???????????????????????????????????????
# #         else:
# #             print(user_form.errors, profile_form.errors)
# #     else:  # ????????????post??????????????????????????????????????????
# #         user_form = UserForm()
# #         profile_form = UserProfileForm()
# #
# #     # ??????render????????????
# #     return render(request, 'rango/register.html',
# #                   context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
#
#
# # def user_login(request):
# #     # We use request.POST.get('<variable>') as opposed
# #     # to request.POST['<variable>'], because the
# #     # request.POST.get('<variable>') returns None if the
# #     # value does not exist, while request.POST['<variable>']
# #     # will raise a KeyError exception.
# #     if request.method == 'POST':
# #         username = request.POST.get('username')
# #         password = request.POST.get('password')
# #         # ??????username???psw????????????
# #         user = authenticate(username=username, password=password)
# #
# #         if user:
# #             if user.is_active:
# #                 login(request, user)
# #                 return redirect(reverse('rango:index'))  # response 302, not 200
# #             else:
# #                 return HttpResponse("Your Rango account is disabled.")
# #         else:
# #             print(f"Invalid login details: {username}, {password}")
# #             return HttpResponse("Invalid login details supplied.")
# #     else:
# #         return render(request, 'rango/login.html')
#
#
# @login_required
# def restricted(request):
#     return render(request, 'rango/restricted.html')
#
#
# # @login_required
# # def user_logout(request):
# #     logout(request)
# #     return redirect(reverse('rango:index'))
#
#
# # visit site counter// Chapter 10.5
# # def visitor_cookie_handler(request, response):
# #     # all cookie values are returned as strings
# #     visits = int(request.COOKIES.get('visits', '1'))
# #     # visits = request.COOKIES.get('visits', 1)
# #     last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
# #     last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
# #     if (datetime.now() - last_visit_time).seconds > 0:
# #         visits = visits + 1
# #         # Update the last visit cookie now that we have updated the count
# #         response.set_cookie('last_visit', str(datetime.now()))
# #     else:
# #         # Set the last visit cookie
# #         response.set_cookie('last_visit', last_visit_cookie)
# #
# #     # Update/set the visits cookie
# #     response.set_cookie('visits', visits)
#
#
# def visitor_cookie_handler(request):
#     # all cookie values are returned as strings
#     visits = int(get_server_side_cookie(request, 'visits', '1'))
#     last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
#     if (datetime.now() - last_visit_time).days > 0:
#         visits = visits + 1
#         # Update the last visit cookie now that we have updated the count
#         request.session['last_visit'] = str(datetime.now())
#     else:
#         # Set the last visit cookie
#         request.session['last_visit'] = last_visit_cookie
#
#     # Update/set the visits cookie
#     request.session['visits'] = visits
#
#
# # get cookie from server
# def get_server_side_cookie(request, cookie, default_val=None):
#     val = request.session.get(cookie)
#     if not val:
#         val = default_val
#     return val


def search(request):
    result_list = []
    query = ''
    context_dict = {}
    if request.method == 'POST':
        if request.method == 'POST':
            query = request.POST['query'].strip()

            if query:
                context_dict['result_list'] = run_query(query)
                context_dict['query'] = query

    return render(request, 'rango/search.html', context_dict)


def get_category_list(max_results=0, starts_with=''):
    category_list = []

    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]

    return category_list


def suggest_category(request):
    category_list = []
    start_with = ''
    if request.method == 'GET':
        start_with = request.GET['suggestion']
    category_list = get_category_list(8, start_with)
    if len(category_list) == 0:
        category_list = Category.objects.order_by('-likes')
    return render(request, 'rango/categories.html', {'categories': category_list})



# class CategorySuggestionView(View):
#     def get(self, request):
#         if 'suggestion' in request.GET:
#             suggestion = request.GET['suggestion']
#         else:
#             suggestion = ''
#
#         category_list = get_category_list(max_results=5, starts_with=suggestion)
#
#         if len(category_list) == 0:
#             category_list = Category.objects.order_by('-likes')
#
#         return render(request, 'rango/categories.html', {'categories': category_list})
