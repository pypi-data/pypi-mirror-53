# -*- coding: utf-8 -*-

"""Common views for djpub


-------------------------------------------------------------------
Copyright: Md. Jahidul Hamid <jahidulhamid@yahoo.com>

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
-------------------------------------------------------------------
"""

from django.http import HttpResponse
from django.views import View
from django.utils.module_loading import import_string

class BaseView(View):
    """Base view to be inherited by other views
    """
    pass