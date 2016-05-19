from rest_framework import serializers
from blog.models import Project, Account, Pimage, Review, Bid


	
class AccountSerializer(serializers.ModelSerializer):

	projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
	# reviews = serializers.PrimaryKeyRelatedField(many=True, queryset=Review.objects.all())

	class Meta:
		model = Account
		fields = ('id', 'email', 'username', 'created_at', 'updated_at', 'first_name', 'last_name', 'password','image','projects',)
		read_only_fields = ('created_at', 'updated_at',)



	# 	def create(self, validated_data):
	# 		return Account.objects.create(**validated_data)

	# 	def update(self, instance, validated_data):
	# 		instance.username = validated_data.get('username', instance.username)

	# 		instance.save()

	# 		password = validated_data.get('password', None)
	# 		confirm_password = validated_data.get('confirm_password', None)

		
	# 	instance.save()

	# 	update_session_auth_hash(self.context.get('request'), instance)

	# return instance

class ProjectSerializer(serializers.ModelSerializer):

	# author = AccountSerializer(read_only=True, required=False)
	author = serializers.ReadOnlyField(source='author.username')

	class Meta:
		model = Project
		fields = ('id','title','category','descrip', 'author')



class PimageSerializer(serializers.ModelSerializer):

	user = serializers.ReadOnlyField(source='user.username')
	image_url = serializers.SerializerMethodField()
	thumbnail_url = serializers.SerializerMethodField()
	

	class Meta:
		model = Pimage
		fields =('id','image','image_url','thumbnail_url' ,'user')

	def get_image_url(self, pimage):
		request = self.context.get('request')
		image_url = pimage.image.url
		return request.build_absolute_uri(image_url)

	def get_thumbnail_url(self, pimage):
		request = self.context.get('request')
		thumbnail_url = pimage.thumbnail.url
		return request.build_absolute_uri(thumbnail_url)




class ReviewSerializer(serializers.ModelSerializer):

	reviewer = serializers.ReadOnlyField(source='reviewer.username')
	profilepic_url = serializers.SerializerMethodField()

	class Meta:
		model = Review
		fields =('id','review_text','rating','reviewed','reviewer','created_date','profilepic_url')

	def get_profilepic_url(self, review):
		request = self.context.get('request')
		profilepic_url = review.reviewer.image.url
		return request.build_absolute_uri(profilepic_url)


class BidSerializer(serializers.ModelSerializer):

	bidder = serializers.ReadOnlyField(source='bidder.username')
	profilepic_url = serializers.SerializerMethodField()

	class Meta:
		model = Bid
		fields =('id','bidder','project_id','amount','descrip','created_date','profilepic_url')

	def get_profilepic_url(self, bid):
		request = self.context.get('request')
		profilepic_url = bid.bidder.image.url
		return request.build_absolute_uri(profilepic_url)
