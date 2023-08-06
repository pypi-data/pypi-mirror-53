
import os
from django.conf import settings as S
from django.templatetags.static import static
from django.urls import reverse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from .. import utils

import logging


logging.basicConfig(
    level = logging.DEBUG if S.DEBUG else logging.INFO,
    format = '%(levelname)s:%(name)s: %(message)s',
)
logger = logging.getLogger(__name__)

class Mixin(object):
    """Base mixin class offered by djpub
    
    Every djpub compatible view should inherit this mixin class.

    The following attributes must be overriden:
        * djpub_install_prefix
    """
    
    _djpub_active_theme_dir_name = 'active'
    djpub_install_prefix = None     # Must override

    def __init__(self, **kwargs):
        super(Mixin, self).__init__(**kwargs)
    
    def djpub_get_install_path_relative(self):
        """Return relative path from install prefix
        
        Replaces dots ('.') with os.path.sep
        
        Returns:
            str: relative path
        """

        return os.path.join(self.djpub_install_prefix.replace('.', os.path.sep), self._djpub_active_theme_dir_name)
    
    def djpub_template(self, relative_path):
        """Convert template relative path to actual template path
        
        Args:
            relative_path (str): template path relative to your package
        
        Returns:
            str: Actual relative path to the template root
        """
        return os.path.join(self.djpub_get_install_path_relative(), relative_path)

    def djpub_templates(self, relative_paths):
        """Convert template relative paths to actual template paths
        
        Args:
            relative_paths (list): List of template paths relative to your package
        
        Returns:
            list: A new list of templates paths relative to the template root
        """
        full_paths = []
        for relative_path in relative_paths:
            full_paths.append(self.djpub_template(relative_path))
        return full_paths
    
    def djpub_static(self, path):
        return static(utils.urljoin(self.djpub_get_install_path_relative(), path))
    
    def djpub_url(self, path):
        return reverse(utils.urljoin(self.djpub_get_install_path_relative(), path))

    
    def djpub_get_new_context(self):
        """Return a context already filled with required djpub context data
        
        Must use this method to create new context.
        
        Returns:
            dict: djpub context
        """
        djpub_ctx = {
            'djpub_theme_path': self.djpub_get_install_path_relative(),
            'djpub_template': self.djpub_template,
            'djpub_templates': self.djpub_templates,
            'static': self.djpub_static,
            'url': self.djpub_url,
        }
        return djpub_ctx

    def djpub_add_context_mandatory(self, ctx):
        """Add required djpub context to an existing context inplace.
        
        Args:
            ctx (dict): existing context
        """
        ctx.update(self.djpub_get_new_context())
    
    def djpub_render(self, request, template, ctx):
        """Render and return response handling djpub theme paths
        
        Args:
            request (HttpRequest): the request object
            template (str or list): one template or multiple templates
            ctx (dict): the context
        
        Returns:
            [type]: [description]
        """
        if isinstance(template, str):
            return render(request, self.djpub_template(template), ctx)
        else:
            return render(request, self.djpub_templates(template), ctx)

    def djpub_save_and_render(self, request, template, ctx, html_file):
        """Render and return response handling djpub theme paths
        
        Args:
            request (HttpRequest): the request object
            template (str or list): one template or multiple templates
            ctx (dict): the context
        
        Returns:
            [HttpResponse]: response
        """
        if isinstance(template, str):
            html = render_to_string(self.djpub_template(template), context=ctx, request=request)
        else:
            html = render_to_string(self.djpub_templates(template), context=ctx, request=request)
        try:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
        except:
            logger.exception("Failed to write file: " + html_file)
        return HttpResponse(html, content_type="text/html")



