from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.request import Request

from .validators import check_items_for_import, check_valid_uuid, check_date_iso
from .utils import create_new_item, update_existing_item, remove_item
from .utils import update_parent_prices_after_item_deleting
from .utils import satisfies_date_interval
from .utils import add_parents_changes_to_history
from .utils import get_node_statistics_filtered_by_date
from .custom_types import ERROR_400, ERROR_404
from .constants import SHOP_UNIT_TYPES
from .models import ShopUnit, HistoryTable
from .serializers import shop_unit_to_dict


class ImportsAPIView(views.APIView):
    def post(self, request: Request) -> Response:
        if 'updateDate' not in request.data:
            return Response(ERROR_400.to_dict(), status=status.HTTP_400_BAD_REQUEST)

        if 'items' not in request.data:
            return Response(ERROR_400.to_dict(), status=status.HTTP_400_BAD_REQUEST)

        received_update_date = request.data['updateDate']
        received_items = request.data['items']

        if not check_items_for_import(received_items, received_update_date):
            return Response(ERROR_400.to_dict(), status=status.HTTP_400_BAD_REQUEST)

        for item in received_items:
            existing_units = ShopUnit.objects
            with_similar_id = existing_units.filter(id=item['id'])

            if len(with_similar_id) == 0:
                create_new_item(item, received_update_date)
            elif len(with_similar_id) == 1:
                update_existing_item(item, received_update_date)

        return Response(status=status.HTTP_200_OK)


class DeleteAPIView(views.APIView):
    def delete(self, request: Request, to_delete: str = None) -> Response:
        if not check_valid_uuid(to_delete):
            return Response(ERROR_400.to_dict(), status=status.HTTP_400_BAD_REQUEST)

        found_item = ShopUnit.objects.filter(id=to_delete)

        if len(found_item) == 0:
            return Response(ERROR_404.to_dict(), status=status.HTTP_404_NOT_FOUND)

        deleted_goods_count: int = found_item[0].totally_inner_goods_count
        deleted_total_sum: int = found_item[0].total_inner_sum
        parent = ShopUnit.objects.filter(id=found_item[0].parentId)

        remove_item(found_item[0])

        if len(parent) != 0:
            if (deleted_total_sum is not None) and (deleted_goods_count != 0):
                update_parent_prices_after_item_deleting(parent, deleted_total_sum, deleted_goods_count)
                add_parents_changes_to_history(parent)

        return Response(status=status.HTTP_200_OK)


class NodesAPIView(views.APIView):
    def get(self, request: Request, to_get: str) -> Response:
        if not check_valid_uuid(to_get):
            return Response(ERROR_400.to_dict(), status=status.HTTP_400_BAD_REQUEST)

        found_items = ShopUnit.objects.filter(id=to_get)

        if len(found_items) == 0:
            return Response(ERROR_404.to_dict(), status=status.HTTP_404_NOT_FOUND)

        found_item = found_items[0]

        return Response(shop_unit_to_dict(found_item), status=status.HTTP_200_OK)


class SalesAPIView(views.APIView):
    def get(self, request: Request) -> Response:
        if 'date' not in request.query_params:
            return Response(ERROR_400.to_dict(), status=status.HTTP_400_BAD_REQUEST)

        date_to_get: str = request.query_params['date']

        if not check_date_iso(date_to_get):
            return Response(ERROR_400.to_dict(), status=status.HTTP_400_BAD_REQUEST)

        all_offers = ShopUnit.objects.filter(type=SHOP_UNIT_TYPES[1][1])

        response: list = list()

        for offer in all_offers:
            if satisfies_date_interval(offer.date, date_to_get):
                response.append(shop_unit_to_dict(offer, False))

        return Response(response, status=status.HTTP_200_OK)


class NodeStatisticsAPIView(views.APIView):
    def get(self, request: Request, to_get: str) -> Response:
        if not check_valid_uuid(to_get):
            return Response(ERROR_400.to_dict(), status=status.HTTP_400_BAD_REQUEST)

        if 'dateStart' in request.query_params:
            if not check_date_iso(request.query_params['dateStart']):
                return Response(ERROR_400.to_dict(), status=status.HTTP_400_BAD_REQUEST)

        if 'dateEnd' in request.query_params:
            if not check_date_iso(request.query_params['dateEnd']):
                return Response(ERROR_400.to_dict(), status=status.HTTP_400_BAD_REQUEST)

        found_item = HistoryTable.objects.filter(id=to_get)

        if len(found_item) == 0:
            return Response(ERROR_404.to_dict(), status=status.HTTP_404_NOT_FOUND)

        filtered = get_node_statistics_filtered_by_date(found_item[0], request.query_params.get('dateStart'), request.query_params.get('dateEnd'))

        response: list[dict] = list(map(lambda item: shop_unit_to_dict(item, False), filtered))

        return Response(response, status=status.HTTP_200_OK)
