from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):


	def has_object_permission(self, request, view, obj):
	# Read permissions are allowed to any request,
	# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the owner of the snippet.
		return obj.author == request.user

class IsReviewerOrReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.reviewer == request.user


class IsBidderOrReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.bidder == request.user