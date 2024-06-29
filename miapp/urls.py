from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from django.contrib.auth import views as auth_views
from .views import CheckoutView, PaymentFormView, generate_order_pdf, export_sales_to_excel

urlpatterns = [
    path("", views.home),
    path('volver/', views.home, name="volver"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("category-title/<val>", views.CategoryTitle.as_view(), name="category-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('address/', views.address, name="address"),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name="updateAddress"),

    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.show_cart, name='showcart'),
    #path('checkout/', views.checkout.as_view(), name='checkout'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentFormView.as_view(), name='payment_form'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    #autenticación login
    path('registration/', views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name="login"),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('captcha/', include('captcha.urls')),
    path('export_users/', views.export_users_to_excel, name='export_users'),
    path('export_products/', views.export_products_to_excel, name='export_products'),
    path('productoadd/', views.ProductAddView.as_view(), name="productoadd"),
    path('generate_order_pdf/<int:payment_id>/', views.generate_order_pdf, name='generate_order_pdf'),
    path('export_sales/', views.export_sales_to_excel, name='export_sales_to_excel'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "LIMONATURA"
admin.site.site_title = "LIMONATURA"
admin.site.site_index_title = "Bienvenid@ a la tienda LIMONATURA"