import urllib

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from products.api.v1.serializers import ProductModelSerializer, ProductSizeModelSerializer
from products.models import Product, ProductSize
from products.task import upload_csv_for_bonds


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()


class ProductSizeModelViewSet(ModelViewSet):
    serializer_class = ProductSizeModelSerializer
    queryset = ProductSize.objects.all()


class ProductCSVUploadViewSet(APIView):
    def post(self, request, version: str, *args, **kwargs) -> Response:
        """
        post method for creating data of bonds from csv file
        """
        file = request.FILES.get("file")
        if not file:
            raise ValidationError("File is required")
        file = file.read().decode("utf-8")
        upload_csv_for_bonds(file)
        return Response()

    def get(self, request, version: str, *args, **kwargs) -> Response:
        file_id = self.request.GET.get("id")
        if not file_id:
            return Response(
                # response_data(
                #     SUCCESS, status.HTTP_400_BAD_REQUEST, BOND_DOWNLOADED_ERROR
                # )
            )
        static_root = request.build_absolute_uri(settings.STATIC_URL)
        file_name = "bonds/csv_samples/bond.csv"
        file_url = urllib.parse.urljoin(static_root, file_name)
        # return Response(response_data(SUCCESS, status.HTTP_200_OK, file_url))
