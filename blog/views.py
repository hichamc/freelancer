from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms	import SignUpForm, LoginForm, ProjectForm, BidForm, PimageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from blog.serializers import ProjectSerializer, AccountSerializer, PimageSerializer, ReviewSerializer, BidSerializer
from rest_framework import generics
from rest_framework import permissions
from blog.permissions import IsOwnerOrReadOnly, IsReviewerOrReadOnly, IsBidderOrReadOnly


class BidList(generics.ListCreateAPIView):
	queryset = Bid.objects.all()
	serializer_class = BidSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(bidder=self.request.user)

	def get_queryset(self):
	
		pk = self.kwargs['pk']
		return Bid.objects.filter(project_id__id=pk)

class BidDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Bid.objects.all()
	serializer_class = BidSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsBidderOrReadOnly,)


class ReviewList(generics.ListCreateAPIView):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(reviewer=self.request.user)

	def get_queryset(self):
	
		username = self.kwargs['username']
		return Review.objects.filter(reviewed__username=username)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsReviewerOrReadOnly,)


class PimageList(generics.ListCreateAPIView):
	queryset = Pimage.objects.all()
	serializer_class = PimageSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def get_queryset(self):
	
		username = self.kwargs['username']
		return Pimage.objects.filter(user__username=username)


class ProjectList(generics.ListCreateAPIView):
	queryset = Project.objects.all()
	serializer_class = ProjectSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Project.objects.all()
	serializer_class = ProjectSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class AccountList(generics.ListAPIView):
	queryset = Account.objects.all()
	serializer_class = AccountSerializer


class AccountDetail(generics.RetrieveAPIView):
	queryset = Account.objects.all()
	serializer_class = AccountSerializer



def projects(request):
	return	render(request, 'projectlist.html')




def newPimage(request):
	if request.method == 'POST' and request.FILES.get('imagefile'):
			image = request.FILES.get('imagefile')
			new_image = request.user.user_images.create(imagefile = image)
			new_image.save()
			return HttpResponseRedirect('/'+request.user.username)

	return HttpResponseRedirect('/')

def profile(request, username):
	user_instance = get_object_or_404(Account, username=username)

	user_reviews = user_instance.reviewed.all() #reviewed is the related name that replaces reviews_set
	number_reviews = user_instance.reviewed.count()
	portfolio_images = user_instance.user_images.all()

	ratingSum = 0

	form = PimageForm(request.POST or None, request.FILES or None)


	for review in user_reviews:
		ratingSum = ratingSum + review.rating

	if number_reviews == 0:
		userRating = ratingSum
	else:
		userRating = ratingSum / number_reviews

	userRating = round(userRating,2)


	if request.method == 'POST':
		
		review_text = request.POST.get('review_text')
		rating = request.POST.get('note')

		new_review = user_instance.reviewed.create(reviewer=request.user, rating=float(rating), review_text=review_text)
		new_review.save()

		return HttpResponseRedirect('/'+username)

	context = {
		"user_instance": user_instance,
		"reviews" : user_reviews,
		"number_reviews": number_reviews,
		"userRating": userRating,
		"form": form,
		"portfolio_images": portfolio_images
	}

	return	render(request, 'profile.html', context)


def home(request):
	
	# queryset = Project.objects.filter(author=request.user)
	queryset_list = Project.objects.all().order_by("-created_date")
	query = request.GET.get("cat")
	if query:
		queryset_list = queryset_list.filter(category=query).order_by('-created_date')
	
	categories = Category.objects.all()


	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page

	page = request.GET.get('page')
	
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"queryset": queryset,
		"categories": categories,
	}

	return	render(request, 'index.html', context)

def register(request):

	title = "Registeration Page"
	form = SignUpForm(request.POST or None, request.FILES or None)

	if form.is_valid():

		instance = form.save(commit=False)
		instance.set_password(request.POST.get('password'))
		instance.save()

		email = request.POST.get('email')
		password = request.POST.get('password')

		user = authenticate(username=email, password=password)

		# user = authenticate(username=instance.username, password=instance.password)
		login(request, user)

		return HttpResponseRedirect('/')
	
	context = {
		"title" : title,
		"form" : form,

	}
	return	render(request, 'register.html', context)

def loginView(request):
	return	render(request, 'login.html', {})

def auth_view(request):

	username = request.POST.get('email')
	password = request.POST.get('password')

	user = authenticate(username=username, password=password)

	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect('/')

	return	HttpResponseRedirect('/login')


@login_required()
def newProjectView(request):
	title = "Registeration Page"
	# form = ProjectForm(request.POST or None)

	categories = Category.objects.all()
	current_user = request.user

	if request.method == 'POST':
		
		title = request.POST.get('title')
		category = request.POST.get('category')
		descrip = request.POST.get('descrip')

		new_project = current_user.projects.create( title=title, category=category, descrip=descrip )
		new_project.save()
	
		return HttpResponseRedirect('/')
	
	context = {
		"title" : title,
		# "form" : form,
		"categories": categories,

	}
	return	render(request, 'newproject.html', context)

@login_required()
def project_update(request, id=None):
	title = "Modification de projet"
	# form = ProjectForm(request.POST or None)
	instance = get_object_or_404(Project, id=id)
	categories = Category.objects.all()

	if request.method == 'POST':
		
		instance.title = request.POST.get('title')
		instance.category = request.POST.get('category')
		instance.descrip = request.POST.get('descrip')

		instance.save()
	
		return HttpResponseRedirect('/'+id)
	
	context = {
		"title" : title,
		"instance" : instance,
		"categories": categories,

	}
	return	render(request, 'project_update.html', context)

@login_required()
def project_delete(request, id=None):

	instance = get_object_or_404(Project, id=id)
	instance.delete()
	

	return HttpResponseRedirect('/')
	


def project_detail(request, id):


	project_instance = get_object_or_404(Project, id=id)
	
	form = BidForm(request.POST or None)

	if request.method == 'POST':
		if form.is_valid():
		
			amount = request.POST.get('amount')
			descrip = request.POST.get('descrip')

			new_bid = project_instance.project_bids.create(bidder=request.user, amount=amount, descrip=descrip )
			new_bid.save()
			return HttpResponseRedirect('/'+id)
	

	project_bids = Bid.objects.filter(project_id=id)

	context = {
		"title": project_instance.title,
		"project_instance": project_instance,
		"project_bids": project_bids,
		"form" : form,
	}

	return	render(request, 'project_detail.html', context)


def logout_view(request): 
	logout(request)
	return HttpResponseRedirect('/')

# def my_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             # Redirect to a success page.