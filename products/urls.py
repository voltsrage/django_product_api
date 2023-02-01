from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
	#retrieve a single item

	# list view + create view
	path('',views.product_list_create_view),
	#path('',views.product_mixin_view),

	# update view
	path('<int:pk>/update',views.product_update_view,name='product-edit'),

	# delete view
	path('<int:pk>/delete',views.product_destroy_view),

	# details view
	path('<int:pk>/',views.product_detail_view,name='product-detail'),
	#path('<int:pk>/',views.product_mixin_view),
]