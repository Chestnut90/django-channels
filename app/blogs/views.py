from django.shortcuts import render, get_object_or_404

from blogs.models import Post


def posts_index(request):
    queryset = Post.objects.all()
    return render(
        request,
        "blogs/posts_index.html",
        {"posts": queryset},
    )


def posts_partial(request, id):
    obj = get_object_or_404(Post, pk=id)
    return render(
        request,
        "blogs/partial/post.html",
        {"post": obj},
    )
