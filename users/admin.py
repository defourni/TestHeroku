from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from users.models import Author

from django.utils.translation import ugettext_lazy as _     # translation hook to make the project translatable

# see more: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model
# Define an inline admin descriptor for Author model
# which acts a bit like a singleton
class AuthorInline(admin.StackedInline):
    model = Author
    can_delete = False
    verbose_name_plural = 'author'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     (_('Personal info'), {'fields': ('avatar', 'first_name', 'last_name', 'github')}),
    #     (_('Join Request'), {'fields': ('approved')}),
    #     (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
    #                                    'groups', 'user_permissions')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'password1', 'password2', 'avatar', 'github'),
    #     }),
    # )
    # list_display = ('username', 'first_name', 'last_name', 'approved', 'is_staff')
    inlines = (AuthorInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# from .models import User, Author


# class AuthorInline(admin.StackedInline):
#     model = Author
#     can_delete = False


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                        'groups', 'user_permissions')}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('username', 'first_name', 'last_name', 'is_staff')
#     search_fields = ('username', 'first_name', 'last_name')
#     ordering = ('username',)
#     inlines = (AuthorInline, )