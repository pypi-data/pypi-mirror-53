
from django.urls import path
import djpub
from .views import HomeView, PostView

class UrlPatterns(djpub.urls.UrlPatterns):
    """A class named UrlPatterns must be avaiable directly under djpub_view
    
    class path: [any_leading_path].djpub_view.UrlPatterns
    """

    def get_urlpatterns(self):
        """Return the url patterns handled by this view package
        
        Returns:
            list: django url patterns
        """
        urlpatterns = [
            path('', HomeView.as_view()),
            path('post/', PostView.as_view()),
        ]
        return urlpatterns

    def get_desired_position_index(self):
        """Return the index where these url patterns will be inserted.
        
        Returns:
            int: Desired position index
        """
        return 0