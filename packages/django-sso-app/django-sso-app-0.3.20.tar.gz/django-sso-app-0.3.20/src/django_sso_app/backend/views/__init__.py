import logging
import os
import platform

from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

logger = logging.getLogger('backend')

CURRENT_DIR = os.getcwd()


if platform.system() == 'Windows':
    def local_space_available(dir):
        """Return space available on local filesystem."""
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dir), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
else:
    def local_space_available(dir):
        destination_stats = os.statvfs(dir)
        return destination_stats.f_bsize * destination_stats.f_bavail


class StatsView(APIView):
    """
    Return instance stats
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            #stats = os.statvfs(CURRENT_DIR)
            free_space_mb = int(local_space_available(CURRENT_DIR) / (1024 * 1024))
            # free_space_mb = int(
            #     (stats.f_bavail * stats.f_frsize) / (1024 * 1024))

            logger.info(
                'Free space (MB): {}.'.format(free_space_mb))

            if free_space_mb > 200:
                health_status = 'green'
            else:
                if free_space_mb < 100:
                    health_status = 'yellow'
                else:
                    health_status = 'red'

            data = {
                'status': health_status,
            }

            if request.user is not None and request.user.is_staff:
                data['free_space_mb'] = free_space_mb

            return Response(data, status.HTTP_200_OK)

        except Exception as e:
            err_msg = str(e)
            logger.exception('Error getting health {}'.format(err_msg))
            return Response(err_msg, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SwaggerSchemaView(APIView):
    """
    OpenAPI
    """
    permission_classes = (AllowAny,)
    renderer_classes = (
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    )
    title = 'Django Fisherman'
    patterns = []

    def get(self, request):
        generator = SchemaGenerator(title=self.title, patterns=self.patterns)
        schema = generator.get_schema(request=request)

        return Response(schema)
