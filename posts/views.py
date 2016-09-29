from urllib import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone

# Create your views here.
from forms import PostForm
from .models import Post


def post_create(request ):
	if not request.user.is_staff or not request.user.is_superuser:
		return render(request,'indexx.html',status=404)


	form =PostForm(request.POST  or None, request.FILES  or None)

	if form.is_valid():
		instance = form.save(commit = False)
		print form.cleaned_data.get("title")
		instance.save()
		#message sucess
		
		messages.info(request,'sucessessfully Created.')
		return HttpResponseRedirect(instance.get_absolute_url())
	context= {
			"form":form,
	}
	return render(request,"post_form.html",context)

def post_detail(request,id=None ):#retrieve
	#instance= Post.objects.get(id=1)
	instance= get_object_or_404(Post, id=id)
	share_string=quote_plus(instance.content)
	context ={
		"title":instance.title,
		"instance":instance,
		"share_string":share_string,
	}
	return render(request,"post_detail.html",context)

def post_list(request):#list items
	today = timezone.now().date()
	queryset_list=Post.objects.filter(draft=False).filter(pubs__lte=timezone.now() )#.order_by("-timestamp")#.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list=Post.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains= query) |
			Q(content__icontains= query)|
			Q(user__first_name__icontains= query)|
			Q(user__last_name__icontains= query)
			).distinct()

	paginator = Paginator(queryset_list, 4) # Show 10 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
 		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
 		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
		"object_list":queryset,
		"title":"List",
		"page_request_var":page_request_var
	}
	return render(request,  "post_list.html", context)




def post_update(request,id= None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance= get_object_or_404(Post, id=id)
	form = PostForm(request.POST  or None, request.FILES  or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.info(request,"<a href='#'>Item</a>Saved",extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
	context ={
		"title":instance.title,
		"instance":instance,
		"form":form,
	}
	return render(request,"post_form.html",context)

def post_delete(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance= get_object_or_404(Post, id=id)
	instance.delete()
	messages.sucess(request,"sucessessfully Deleted")
	return redirect("posts:list")
