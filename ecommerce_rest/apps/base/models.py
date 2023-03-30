from django.db import models

# Create your models here.
class BaseModel(models.Model):

    id = models.AutoField(primary_key=True)
    state = models.BooleanField('Estado', default=True)
    created_date = models.DateField(auto_now_add=True,auto_now=False, verbose_name='Date created')
    modified_date = models.DateField(auto_now_add=False,auto_now=True, verbose_name='Date modified')
    delete_date = models.DateField(auto_now_add=False,auto_now=True, verbose_name='Date deleted')

    class Meta:
        abstract = True
        verbose_name = 'Model base'
        verbose_name_plural ='Models base'

