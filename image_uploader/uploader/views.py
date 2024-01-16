from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUp, SaveImage
from django.contrib import messages
from .models import Images
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction

def register(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Welcome to the page, {username}')
            return redirect('index')
    form = SignUp()
    return render(request, 'register.html', {'form': form})

# @transaction.atomic
def index(request):
    images = Images.objects.all()
    paginator = Paginator(images, 3)
    page = request.GET.get('page')

    try:
        paginated_pics = paginator.page(page)
    except PageNotAnInteger:
        paginated_pics = paginator.page(1)
    except EmptyPage:
        paginated_pics = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        form = SaveImage(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            image_file = image_instance.image
            print(image_file)
            print('image file')
            try:
            # opening the image with pillow
                image = Image.open(image_file.path)
                print('image opened successfully')

                # resizing the image
                image.thumbnail((200, 200))
                image.save(image_file.path)
                image_instance.save()
                messages.success(request, 'Image saved successfully')
                return redirect('index')
            except Exception as e:
                messages.error(request, 'Please choose a valid image file.')
                return redirect('index')
    else:
        last_entry = Images.objects.latest('created')
        last_entry.delete()
        form = SaveImage()
        return render(request, 'index.html', {'images': images, 'form': form, 'paginated_pics':paginated_pics})

def edit_image(request,pk):
    image = get_object_or_404(Images, pk=pk)
    return render(request, 'edit.html',{'image':image})

def delete_image(request,pk):
    image = get_object_or_404(Images, pk=pk)
    image.delete()
    return redirect('index')