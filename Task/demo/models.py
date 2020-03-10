from django.db import models
from django.contrib.postgres.fields import JSONField

class User(models.Model):
    name =  models.CharField(max_length = 50,blank=True, null=True)
    age = models.IntegerField(blank=True,null=True)
    mobile = models.BigIntegerField(unique=True,blank=True,null=True)

class Document(models.Model):
    SOURCE_CHOICES = (
       ('HTML', 'html'),
       ('PDF', 'pdf'),
       ('DOC', 'docx'),
       ('PPT', 'ppt'),
       ('JPEG','jpeg'),
    )
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='exports')
    created_time = models.DateTimeField(auto_now_add=True)
    types = models.CharField(max_length=100,null=True,blank=True)
    source_type = models.CharField(choices=SOURCE_CHOICES,blank=True,null=True,max_length=20)
    source_id = models.CharField(blank=True,null=True,max_length=50)
    input_meta_data = JSONField(default=dict,null=True,blank=True)


