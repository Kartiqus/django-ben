from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None and user.is_staff:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=401)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_products = Product.objects.filter(stock__lt=10)
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['get'])
    def customer_orders(self, request):
        email = request.query_params.get('email', None)
        if email is None:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        orders = Order.objects.filter(email=email)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sales_report(self, request):
        total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        order_count = Order.objects.count()
        return Response({
            "total_sales": total_sales,
            "order_count": order_count,
            "average_order_value": total_sales / order_count if order_count > 0 else 0
        })
