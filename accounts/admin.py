from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User




class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth', 'address_1',
                  'address_2', 'post_code', 'telephone', 'email', 'username',
                  'password', 'picture', 'is_verified', 'is_active', 'is_admin')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    form = UserForm
    list_display = ('first_name', 'last_name', 'username', 'email',)


admin.site.register(User, CustomUserAdmin)