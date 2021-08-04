from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.models import User, UserLike, UserView
from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator

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


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def show_user_likes(request, username):
    context_dict = {}
    try:
        user_likes = UserLike.objects.filter(username=username)

        context_dict['likes'] = user_likes

    except Category.DoesNotExist:
        context_dict['likes'] = None
    return render(request, 'rango/user_likes.html', context=context_dict)


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

        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        category.likes = category.likes + 1
        category.save()

        return HttpResponse(category.likes)
