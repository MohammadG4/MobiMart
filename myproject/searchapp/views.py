from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import meilisearch
from rest_framework.permissions import AllowAny,IsAdminUser, IsAuthenticated


class ProductSearchView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        q = request.GET.get("q", "")
        limit = int(request.GET.get("limit", 20))
        offset = int(request.GET.get("offset", 0))
        filter_str = request.GET.get("filter")  # e.g., brand="Apple"
        sort_str = request.GET.get("sort") 

        client = meilisearch.Client(
            settings.MEILISEARCH_URL,
            settings.MEILISEARCH_API_KEY
        )

        index = client.index(settings.MEILISEARCH_INDEX)

        results = index.search(q, {
            "limit": limit,
            "offset": offset,
            "filter": filter_str,
            "sort": [sort_str] if sort_str else None
        })

        return Response(results)
