from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.request import Request

from .utils import check_items_for_import
from .utils import create_new_item, update_existing_item
from .custom_types import Error
from .models import ShopUnit


class ImportsAPIView(views.APIView):
    def post(self, request: Request) -> Response:
        received_post_data = request.data

        received_update_date = received_post_data['updateDate']
        received_items = received_post_data['items']

        check_result: bool = check_items_for_import(received_items, received_update_date)

        if not check_result:
            return Response(Error(400, 'Validation Failed').to_dict(), status.HTTP_400_BAD_REQUEST)

        existing_units = ShopUnit.objects

        for item in received_items:
            with_similar_id = existing_units.filter(id=item['id'])

            if len(with_similar_id) == 0:
                print('CREATING NEW: ', item['name'])
                create_new_item(item, received_update_date)
            elif len(with_similar_id) == 1:
                update_existing_item(item, received_update_date)

        return Response(status.HTTP_200_OK)
