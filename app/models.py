from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Content(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    body = RichTextUploadingField()
    
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Highlight(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='highlights')
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word



class Explanation(models.Model):
    highlight = models.ForeignKey(Highlight, on_delete=models.CASCADE, related_name='explanations')
    text = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    audio = models.FileField(upload_to='audio/', blank=True, null=True)
    video = models.FileField(upload_to='video/', blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Explanation for {self.highlight.word}"



class Review(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)