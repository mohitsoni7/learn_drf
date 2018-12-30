# Generic Views: Pre-built views, shortcuts
# APIview: Regular
from django.db.models import Q
from rest_framework import generics, mixins
from postings.models import BlogPost
from .serializers import BlogPostSerializer
from .permissions import IsOwnerOrReadOnly


class BlogPostCreateListSearchView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = BlogPostSerializer
    # We can override the permissions from here
    # [] means all permissions
    # permission_classes = []

    def get_queryset(self):
        qs = BlogPost.objects.all()
        # Search function
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(Q(title__icontains=query)|(Q(content__icontains=query)))
        return qs
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # create post method in HARD CODED FASHION
    # def post(self, request, *args, **kwargs):
    #     pass
    
    # Instead of Hard CODED way we will use MIXIN
    # This post method will be handled by the CreateModelMixin
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    
    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}



class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    # pass
    # lookup_field = 'pk'
    # queryset = BlogPost.objects.all()

    # def get_queryset(self):
    #     return BlogPost.objects.all()
    
    # def get_object(self):
    #     pk = self.kwargs.get('pk')
    #     return BlogPost.objects.get(pk=pk)

    lookup_field = 'pk'
    serializer_class = BlogPostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return BlogPost.objects.all()
    
    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}
