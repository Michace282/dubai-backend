from django.http import JsonResponse
from django.core.files.base import File
from string import ascii_letters
import random
from .models import ProductImage, ProductSizeColor
from django.template.loader import render_to_string


def upload_images_delete(request, data=None):
    id = request.POST.get('id')
    if id:
        ProductImage.objects.filter(id=id).delete()
    return JsonResponse({'status': True})


def upload_images(request, data=None):
    obj = request.POST.get('obj')
    images = []
    if obj:
        product_size_color = ProductSizeColor.objects.filter(id=obj).first()
        if product_size_color:
            for f in request.FILES.getlist('uploadfiles[]'):
                filename = ''.join(random.choice(ascii_letters) for i in range(24))

                file = File(f)
                file.name = filename

                product_image = ProductImage()
                product_image.product_size_color = product_size_color
                product_image.image.save(filename, file)
                product_image.save()

                images.append(render_to_string('admin/image.html', {'image': product_image}))

    return JsonResponse({'status': True, 'images': images})
