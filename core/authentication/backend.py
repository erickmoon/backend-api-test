from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        """Create a new user from OIDC claims."""
        user = super().create_user(claims)

        # Update user details from claims
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email", "")

        if "groups" in claims:
            # Handle group assignments
            pass

        user.save()
        return user

    def update_user(self, user, claims):
        """Update existing user with new claims."""
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email", "")
        user.save()
        return user

    def filter_users_by_claims(self, claims):
        """Find existing users by email from claims."""
        email = claims.get("email")
        if not email:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(email=email)
