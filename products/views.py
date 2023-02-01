from rest_framework import generics,mixins


from api.mixins import (StaffEditorPermissionMixin, UserQuerySetMixin)
from .models import Product
from .serializers import ProductSerializer

#---------------------------------------------------
# Mixin Class Based Crud Start
#---------------------------------------------------
class ProductMixinView(
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.CreateModelMixin,
	mixins.DestroyModelMixin,
	mixins.UpdateModelMixin,
	generics.GenericAPIView
	):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	lookup_field = 'pk'

	def get(self, request, *args,**kwargs): #HTTP -> get
		print(args,kwargs)
		pk = kwargs.get("pk")
		if pk is not None:
			return self.retrieve(request, *args,**kwargs )
		return self.list(request, *args,**kwargs )

	def post(self, request, *args,**kwargs):
		return self.create(request, *args,**kwargs )

	def perform_create(self, serializer):
		title = serializer.validated_data.get('title')
		content = serializer.validated_data.get('content') or None
		if content is None:
			content = title
		serializer.save(content=content)

product_mixin_view = ProductMixinView.as_view()
#---------------------------------------------------
# Mixin Class Based Crud End
#---------------------------------------------------

#---------------------------------------------------
# Basic Crud Start
#---------------------------------------------------

class ProductDetailAPIView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	lookup_field = 'pk'

product_detail_view = ProductDetailAPIView.as_view()

class ProductUpdateAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	lookup_field = 'pk'

	def perform_update(self, serializer):
		instance = serializer.save()
		if not instance.content:
			instance.content = instance.title

product_update_view = ProductUpdateAPIView.as_view()

class ProductDestroyAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	lookup_field = 'pk'

	def perform_destroy(self, instance):
		super().perform_destroy(instance)

product_destroy_view = ProductDestroyAPIView.as_view()

class ProductListCreateAPIView(UserQuerySetMixin,StaffEditorPermissionMixin, generics.ListCreateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	# authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]

	# Adding additional functionality to object creation
	# Content = title if content is Null
	def perform_create(self, serializer):
		title = serializer.validated_data.get('title')
		content = serializer.validated_data.get('content') or None
		if content is None:
			content = title
		serializer.save(user=self.request.user, content=content)

	# def get_queryset(self, *args, **kwargs):
	# 	qs = super().get_queryset(*args, **kwargs)
	# 	request = self.request
	# 	user = request.user
	# 	if not user.is_authenticated:
	# 		return Product.objects.none()
	# 	return qs.filter(user=request.user)

product_list_create_view = ProductListCreateAPIView.as_view()

#---------------------------------------------------
# Basic Crud End
#---------------------------------------------------