from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUp, SaveImage, EditImage
from django.contrib import messages
from .models import Images
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.utils.datastructures import MultiValueDictKeyError


def register(request):
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Welcome to the page, {username}")
            return redirect("index")
    form = SignUp()
    return render(request, "register.html", {"form": form})


# @transaction.atomic
def index(request):
    images = Images.objects.all()
    paginator = Paginator(images, 3)
    page = request.GET.get("page")

    try:
        paginated_pics = paginator.page(page)
    except PageNotAnInteger:
        paginated_pics = paginator.page(1)
    except EmptyPage:
        paginated_pics = paginator.page(paginator.num_pages)
    if request.method == "POST":
        form = SaveImage(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            image_file = image_instance.image
            try:
                # opening the image with pillow
                image = Image.open(image_file.path)

                # resizing the image
                image.thumbnail((200, 200))
                image.save(image_file.path)
                image_instance.save()
                messages.success(request, "Image saved successfully")
                return redirect("index")
            except Exception as e:
                last_entry = Images.objects.latest("created")
                last_entry.delete()
                messages.error(request, "Please choose a valid image file.")
                return redirect("index")
    else:
        form = SaveImage()
        return render(
            request,
            "index.html",
            {"images": images, "form": form, "paginated_pics": paginated_pics},
        )


def edit_image(request, pk):
    current_image = get_object_or_404(Images, pk=pk)
    if request.method == "POST":
        form = EditImage(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_image = request.FILES["image"]
                current_image.image = new_image
                current_image.save()
                # form.save()
                messages.success(request, "Image updated successfully")
                return redirect("index")
            except MultiValueDictKeyError:
                current_image.delete()
                return redirect("index")

    return render(request, "edit.html", {"image": current_image})


def delete_image(request, pk):
    image = get_object_or_404(Images, pk=pk)
    image.delete()
    return redirect("index")
