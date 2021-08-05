from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import title
from rango.models import Page, Category, UserProfile


from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import title
from rango.models import Page, Category, UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.MAX_NAME_LENGTH,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    thumbnail = forms.ImageField(required=False)

    class Meta:
        model = Category
        fields = ('name', 'thumbnail', )


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.MAX_TITLE_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.MAX_URL_LENGTH, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    thumbnail = forms.ImageField(required=False)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'  # f'': allow python express exists in {}
            cleaned_data['url'] = url

        return cleaned_data


class UserForm(forms.ModelForm):
    # Mask the password when entering eg. ******
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # do not have 'user' cuz when new UserProfile instance, there is
        # no User instance to use. 'user' sets when register user.
        fields = ('website', 'picture',)


# class CategoryForm(forms.ModelForm):
#     name = forms.CharField(max_length=Category.MAX_NAME_LENGTH,
#                            help_text="Please enter the category name.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     slug = forms.CharField(widget=forms.HiddenInput(), required=False)
#
#     class Meta:
#         model = Category
#         fields = ('name',)
#
#
# class PageForm(forms.ModelForm):
#     title = forms.CharField(max_length=Page.MAX_TITLE_LENGTH, help_text="Please enter the title of the page.")
#     url = forms.URLField(max_length=Page.MAX_URL_LENGTH, help_text="Please enter the URL of the page.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#
#     class Meta:
#         model = Page
#         exclude = ('category',)
#
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         url = cleaned_data.get('url')
#
#         if url and not url.startswith('http://'):
#             url = f'http://{url}'  # f'': allow python express exists in {}
#             cleaned_data['url'] = url
#
#         return cleaned_data
#
#
# class UserForm(forms.ModelForm):
#     # Mask the password when entering eg. ******
#     password = forms.CharField(widget=forms.PasswordInput())
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password',)
#
#
# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         # do not have 'user' cuz when new UserProfile instance, there is
#         # no User instance to use. 'user' sets when register user.
#         fields = ('website', 'picture',)
