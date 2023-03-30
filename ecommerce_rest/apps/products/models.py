from django.db import models

from simple_history.models import HistoricalRecords


from apps.base.models import BaseModel


class MeasureUnit(BaseModel):

    description = models.CharField(max_length=50,blank=False, null=False, unique=True, verbose_name='Description')
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
    

    class Meta:
        verbose_name = "MeasureUnit"
        verbose_name_plural = "MeasureUnits"

    def __str__(self):
        return self.description
    

class CategoryProduct(BaseModel):

    description = models.CharField(max_length=50,blank=False, null=False, unique=True, verbose_name='Description')    
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:
        verbose_name = "CategoryProduct"
        verbose_name_plural = "CategoryProducts"

    def __str__(self):
        return self.description

  
class Indicator(BaseModel):

    descount_value = models.PositiveIntegerField(default=0)
    category_product = models.ForeignKey(CategoryProduct, verbose_name="Category product", on_delete=models.CASCADE)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:
        verbose_name = "Indicator"
        verbose_name_plural = "Indicators"

    def __str__(self):
        return f'Offer from category {self.category_product}: {self.descount_value}%'


class Product(BaseModel):

    name = models.CharField(verbose_name="Name of product", max_length=150,unique=True, blank=False, null= False)
    description = models.TextField(verbose_name="Description of product",blank=False, null= False)
    image = models.ImageField(verbose_name='Image product', upload_to='products/',blank=True, null=True)
    measure_unit = models.ForeignKey(MeasureUnit, verbose_name="Unit of Measure", on_delete=models.CASCADE, null=True)
    category_product = models.ForeignKey(CategoryProduct, verbose_name="Category product", on_delete=models.CASCADE, null=True)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


  
