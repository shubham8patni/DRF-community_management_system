from functools import wraps
from django.core.cache import cache
from django.http import HttpResponse

def custom_cache_page(timeout):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(self, request, *args, **kwargs):
            # Define your custom cache key using self.request.path
            cache_key = f"custom_cache_{self.request.path}"
            
            # Try to fetch from cache
            cached_response = cache.get(cache_key)

            if cached_response is None:
                response = view_func(self, request, *args, **kwargs)

                # Render the response to make sure it's fully prepared before caching
                rendered_response = response.render()
                cache.set(cache_key, rendered_response, timeout)
                return rendered_response
            else:
                return cached_response

        return wrapped_view

    return decorator



