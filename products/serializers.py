from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from api.serializers import UserPublicSerializer
from .validators import validate_title

# In order to add calculed fields a serializer is required
class ProductSerializer(serializers.ModelSerializer):
	# in order to change name of field user (1)
	user = UserPublicSerializer(read_only=True)
	discount = serializers.SerializerMethodField(read_only=True)
	url = serializers.SerializerMethodField(read_only=True)
	edit_url = serializers.HyperlinkedIdentityField(
		view_name='product-edit',
		lookup_field = 'pk'
	)

	# Extra Field not in db
	email = serializers.EmailField(write_only=True)
	title = serializers.CharField(validators=[validate_title])

	# if want to create another field with the same info
	# name = serializers.CharField(source='title', read_only=True)
	class Meta:
		model = Product
		fields = [
			'user',
			'url',
			'edit_url',
			'email',
			'id',
			'title',
			'content',
			'price',
			'sale_price',
			'discount'
		]

	# def validate_title(self, value):
	# 	qs = Product.objects.filter(title__iexact=value)
	# 	if qs.exists():
	# 		raise serializers.ValidationError(f"{value} is already a product name!")
	# 	return value

	def create(self, validated_data):
		# first remove non db field
		email = validated_data.pop('email')
		# save the rest fields to the db
		obj = super().create(validated_data)
		return obj

	def update(self,instance , validated_data):
		# first remove non db field
		email = validated_data.pop('email')
		# save the rest fields to the db
		obj = super().update(instance,validated_data)
		return obj

	def get_url(self, obj):
		request = self.context.get('request')
		if request is None:
			return None
		return reverse("product-detail",kwargs={'pk':obj.id}, request=request)

	# in order to change name of field user (2)
	# This is not in the database, therefore not serializable on Post
	def get_discount(self, obj):
		if not hasattr(obj,'id'):
			return None
		if not isinstance(obj,Product):
			return None
		return obj.get_discount()

