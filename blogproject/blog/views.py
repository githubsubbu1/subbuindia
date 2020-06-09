from django.shortcuts import render,redirect,get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from .forms import EmailSendForm
from blog.forms import CommentForm
from taggit.models import Tag
from django.http import HttpResponse
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])
    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list})

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year
    ,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
        else:
            form=CommentForm()
    return render(request,'blog/post_detail.html',{'post':post,'form':CommentForm,'comments':comments,
    'csubmit':csubmit})

def mail_send_view(request,id):
    i=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(i.get_absolute_url())
            subject='{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],i.title)
            message='read to post AT:\n{}\n\n{}\'Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'python6656@gmail.com',[cd['to']])
            sent=True
        else:
            form=EmailSendForm()
    return render(request,'blog/sharebyemail.html',{'i':i,'sent':sent,'form':EmailSendForm})
def check_mail(request):
    s='<h1>hello this is india||</h2>'
    return HttpResponse(s)
    return redirect('mail_send_view')
