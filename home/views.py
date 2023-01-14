from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Category
from . import tasks
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from utils import IsAdminUserMixin
import boto3
from django.conf import settings
import logging
from botocore.exceptions import ClientError

class HomeView(View):

    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/index.html', {'products':products, 'categories':categories})


class ProductDetailView(View):
    
    def get(self, request, slug):
        product = get_object_or_404(Product, slug = slug)
        return render(request, 'home/detail.html', {'product':product})


class BucketHome(IsAdminUserMixin ,View):
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects':objects})
    

class DeleteBucketObjects(IsAdminUserMixin, View):
    def get(self, requst, key):
        tasks.delete_object_task.delay(key)
        messages.success(requst, 'your object will be delete soon', 'info')
        return redirect('home:bucket')

    

class DownloadBucketObject(IsAdminUserMixin, View):
    
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your download will start soon', 'info')
        return redirect('home:bucket')


class UploadBucketObject(IsAdminUserMixin, View):

    def get(self, request):
        logging.basicConfig(level=logging.INFO)

        try:
            s3_resource = boto3.resource(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

        except Exception as exc:
            logging.error(exc)
        else:
            try:
                bucket = s3_resource.Bucket('bucket-name')
                file_path = 'the/abs/path/to/file.txt'
                object_name = 'file.txt'

                with open(file_path, "rb") as file:
                    bucket.put_object(
                        ACL='private',
                        Body=file,
                        Key=object_name
                    )
            except ClientError as e:
                logging.error(e)

    def post(self, request):
        pass