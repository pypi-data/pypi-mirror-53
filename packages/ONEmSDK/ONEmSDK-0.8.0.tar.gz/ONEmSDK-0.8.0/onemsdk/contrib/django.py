from onemsdk.parser.util import load_html
from onemsdk.schema.v1 import Response


class HtmlToOnemResponseMiddleware:
    """ Converts the html rendered by the Django templating engine into a ONEm
    json response

    This middleware should be placed last in the settings.MIDDLEWARE chain
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        dont_convert = (
            response['Content-Type'] == 'application/json' or
            response.status_code != 200
        )
        if dont_convert:
            return response

        tag = load_html(html_str=response.content.decode('utf-8'))

        response.content = Response.from_tag(tag).json()
        response['Content-Type'] = 'application/json'

        return response
