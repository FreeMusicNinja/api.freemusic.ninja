from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets

from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import AuthenticatedUserSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    """API endpoint for viewing and editing users."""

    queryset = User.objects.all()
    permission_classes = (IsUserOrReadOnly,)

    def get_serializer_class(self):
        try:
            obj = self.get_object()
        except AssertionError:  # assume list view, use non-authenticated
            pass
        else:
            if (self.request.user.is_authenticated()
                    and obj == self.request.user):
                return AuthenticatedUserSerializer
        return UserSerializer

    def initial(self, request, *args, **kwargs):
        """Retrieve given user or current user if ``pk`` is "me"."""
        if self.kwargs.get('pk') == 'me' and request.user.is_authenticated():
            self.kwargs['pk'] = self.request.user.pk
        super().initial(request, *args, **kwargs)
