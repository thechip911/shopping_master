from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "mobile_number",
            "is_staff",
            "is_superuser",
            "profile_picture",
            "is_deleted",
        )

    def update(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
