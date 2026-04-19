from django.contrib import admin

from projects.models import(
   Message,ClientReview, BlogPost, Property, Project
)

admin.site.register(Project)
admin.site.register(Property)
admin.site.register(ClientReview)
admin.site.register(BlogPost)
admin.site.register(Message)