"""wtd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from accounts import views as accountsViews
from orders import views as ordersViews
from payments import views as paymentsView
from wtd import settings
from rest_framework import permissions
from django.conf.urls.static import static
from otp import views as otpViews


router = routers.DefaultRouter()
router.register(r'users', accountsViews.UserViewSet)
router.register(r'person', accountsViews.PersonViewSet)
# router.register(r'order', ordersViews.OrderViewSet)


urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls + [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # accounts
    path('accounts/register/', accountsViews.registration_view, name="register"),
    path('accounts/login/', accountsViews.CustomObtainAuthToken.as_view(), name="login"),
    path('accounts/reset/password', accountsViews.UpdateUserPasswordView.as_view()),
    path('accounts/profile/allClientProfiles/', accountsViews.AllClientProfilesView.as_view()),
    path('accounts/profile/persons/', accountsViews.GetPersonsOfUserView.as_view()),
    path('accounts/profile/persons/<str:phone_number>', accountsViews.GetPersonsOfUserViewByPhone.as_view()),
    path('accounts/profile/create/persons/', accountsViews.CreatePersonView.as_view()),
    path('accounts/profile/update/persons/<pk>', accountsViews.UpdatePersonView.as_view()),
    path('accounts/profile/delete/persons/<pk>', accountsViews.DeletePersonView.as_view()),

    path('accounts/profile/availableProviders/<order_id>', accountsViews.GetAvailableProviderView.as_view()),
    # path('accounts/profile/GetProvidelApproval/<pk>', accountsViews.GetProvidelApproval.as_view()),
    path('accounts/profile/provider_change_availability/<pk>', accountsViews.UpdateProviderAvailabilityView.as_view()),
    #Order Client
    path('order/create/', ordersViews.CreateOrderView.as_view()),
    path('order/userOrders/', ordersViews.GetOrdersOfUserView.as_view()),
    path('order/discount/', ordersViews.check_discount),
    path('order/userDeletedDoneOrders/', ordersViews.GetDeletedDoneOrdersOfUserView.as_view()),
    path('order/client_action/<pk>', ordersViews.ApproveOrderByClient.as_view()),
    path('order/extraServices/', ordersViews.GetExtraServicesView.as_view()),
    path('order/calculateCost/', ordersViews.calculateCost_view, name="calculate_cost"),


    # Order Operation
    path('order/operationOrders/', ordersViews.GetOrdersOperation.as_view()),
    path('order/operationOrdersHistory/', ordersViews.GetDeletedDoneOrdersOperation.as_view()),
    path('order/operation_send_to_amb/<pk>', ordersViews.SendOrderToAmbView.as_view()),
    path('order/operation_order_action/<pk>', ordersViews.ActionOrderByOperation.as_view()),

    # Order Provider
    path('order/providerOrders/', ordersViews.GetOrdersProvider.as_view()),
    path('order/providerOrdersHistory/', ordersViews.GetDeletedDoneOrdersProvider.as_view()),
    path('order/provider_order_action/<pk>', ordersViews.ActionOrderByProvider.as_view()),
    path('order/send_report/<pk>', ordersViews.UpdateAmbReport.as_view()),

    # path('order/provider_change_availability/<pk>', ordersViews.ActionOrderByProvider.as_view()),


    # OTP
    path('accounts/otp/<int:otpToken>/login/',
         otpViews.OTPAuthentication.as_view(), name="otp-login"),
    path('accounts/otp/', otpViews.OTPAuthentication.as_view(), name="otp"),
    path('accounts/reset/token/', otpViews.resetPasswordToken.as_view(), name="reset-password-token"),

    # order/payment_info

    #Payment
    path('payment/pay/', paymentsView.pay_view, name="pay"),
    path('payment/', paymentsView.CreatePaymentView.as_view(), name="pay"),
    path('payment/<id>', paymentsView.amwal_pay, name="pay"),
    path('add/payment/', paymentsView.add_pay_view, name="pay"),
    path('order/payment_info/<str:paymentId>', paymentsView.paymentInfo_view.as_view(), name="payment_info"),

    path('download_orders_data/',
         ordersViews.download_orders_data, name='download_orders_data'),
    path('download_invoices/',
         ordersViews.download_invoices, name='download_invoices'),
]
