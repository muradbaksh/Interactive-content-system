from django.shortcuts import render, get_object_or_404
from .models import Content, Explanation, Review
from .forms import ContentForm
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re

@login_required
def create_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('content_list')
    else:
        form = ContentForm()

    return render(request, 'create_content.html', {'form': form})


def content_list(request):
    contents = Content.objects.prefetch_related('highlights').all()

    processed_contents = []

    for content in contents:
        body = str(content.body)

        for h in content.highlights.all():
            pattern = re.escape(h.word)
            replacement = f'<span class="highlight" data-id="{h.id}">{h.word}</span>'
            body = re.sub(pattern, replacement, body, flags=re.IGNORECASE)

        content.processed_body = mark_safe(body)
        processed_contents.append(content)

    return render(request, 'content_list.html', {
        'contents': processed_contents
    })


def content_detail(request, pk):
    content = get_object_or_404(
        Content.objects.select_related('category', 'subcategory')
        .prefetch_related('highlights__explanations', 'reviews'),
        pk=pk
    )

    highlights = content.highlights.all()

    body = str(content.body)

    for h in highlights:
        pattern = re.escape(h.word)
        replacement = f'<span class="highlight" data-id="{h.id}">{h.word}</span>'
        body = re.sub(pattern, replacement, body, flags=re.IGNORECASE)

    return render(request, 'content_detail.html', {
        'content': content,
        'body': mark_safe(body),
        'reviews': content.reviews.all(),
        'highlights': highlights
    })



import re

def get_explanation(request, id):
    exp = get_object_or_404(Explanation, highlight_id=id)

    youtube = None

    if exp.youtube_link:
        match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]+)", exp.youtube_link)
        if match:
            video_id = match.group(1)
            youtube = f"https://www.youtube.com/embed/{video_id}"

    return JsonResponse({
        "text": exp.text,
        "image": exp.image.url if exp.image else None,
        "audio": exp.audio.url if exp.audio else None,
        "video": exp.video.url if exp.video else None,
        "youtube": youtube
    })


@login_required
def add_review(request, pk):
    content = get_object_or_404(Content, pk=pk)

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        comment = request.POST.get('comment', '').strip()

        if not name or not comment:
            messages.error(request, "Name and comment required!")
            return redirect('content_detail', pk=pk)

        try:
            rating = int(request.POST.get('rating', 5))
        except:
            rating = 5

        if rating < 1:
            rating = 1
        elif rating > 5:
            rating = 5

        Review.objects.create(
            content=content,
            name=name,
            comment=comment,
            rating=rating
        )

    return redirect('content_detail', pk=pk)
