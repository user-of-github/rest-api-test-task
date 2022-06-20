from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.request import Request

from uuid import UUID

from .utils import check_items_for_import, check_id_for_delete
from .utils import create_new_item, update_existing_item, remove_item
from .custom_types import Error
from .models import ShopUnit


class ImportsAPIView(views.APIView):
    def post(self, request: Request) -> Response:
        received_post_data = request.data

        received_update_date = received_post_data['updateDate']
        received_items = received_post_data['items']

        check_result: bool = check_items_for_import(received_items, received_update_date)

        if not check_result:
            return Response(Error(400, 'Validation Failed').to_dict(), status=status.HTTP_400_BAD_REQUEST)

        existing_units = ShopUnit.objects

        for item in received_items:
            with_similar_id = existing_units.filter(id=item['id'])

            if len(with_similar_id) == 0:
                print('CREATING NEW: ', item['name'])
                create_new_item(item, received_update_date)
            elif len(with_similar_id) == 1:
                update_existing_item(item, received_update_date)

        return Response(status=status.HTTP_200_OK)


class DeleteAPIView(views.APIView):
    def delete(self, request: Request, to_delete: str = None) -> Response:
        if not check_id_for_delete(to_delete):
            return Response(Error(400, 'Validation Failed').to_dict(), status=status.HTTP_400_BAD_REQUEST)

        found_item = ShopUnit.objects.filter(id=to_delete)

        if len(found_item) == 0:
            return Response(Error(404, 'Item not found').to_dict(), status=status.HTTP_404_NOT_FOUND)

        remove_item(found_item[0])

        return Response(status=status.HTTP_200_OK)



