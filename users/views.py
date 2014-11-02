from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets

from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import AuthenticatedUserSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    """API endpoint for viewing and editing users."""

    queryset = User.objects.all()
    permission_classes = (IsUserOrReadOnly,)
    serializer_class = UserSerializer

    def get_serializer(self, instance=None, *args, **kwargs):
        context = self.get_serializer_context()
        if (self.request.user.is_authenticated()
                and instance == self.request.user):
            serializer_class = AuthenticatedUserSerializer
        else:
            serializer_class = self.serializer_class
        return serializer_class(instance, context=context, *args, **kwargs)

    def initial(self, request, *args, **kwargs):
        """Retrieve given user or current user if ``pk`` is "me"."""
        if self.kwargs.get('pk') == 'me' and request.user.is_authenticated():
            self.kwargs['pk'] = self.request.user.pk
        super().initial(request, *args, **kwargs)
