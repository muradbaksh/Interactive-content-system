from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Content)
admin.site.register(Highlight)
admin.site.register(Explanation)
admin.site.register(Review)