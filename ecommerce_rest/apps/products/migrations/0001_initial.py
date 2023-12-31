# Generated by Django 4.1.5 on 2023-03-22 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Date created')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Date modified')),
                ('delete_date', models.DateField(auto_now=True, verbose_name='Date deleted')),
                ('description', models.CharField(max_length=50, unique=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'CategoryProduct',
                'verbose_name_plural': 'CategoryProducts',
            },
        ),
        migrations.CreateModel(
            name='MeasureUnit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Date created')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Date modified')),
                ('delete_date', models.DateField(auto_now=True, verbose_name='Date deleted')),
                ('description', models.CharField(max_length=50, unique=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'MeasureUnit',
                'verbose_name_plural': 'MeasureUnits',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Date created')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Date modified')),
                ('delete_date', models.DateField(auto_now=True, verbose_name='Date deleted')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Name of product')),
                ('description', models.TextField(verbose_name='Description of product')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Image product')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Date created')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Date modified')),
                ('delete_date', models.DateField(auto_now=True, verbose_name='Date deleted')),
                ('descount_value', models.PositiveIntegerField(default=0)),
                ('category_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.categoryproduct', verbose_name='Category product')),
            ],
            options={
                'verbose_name': 'Indicator',
                'verbose_name_plural': 'Indicators',
            },
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(blank=True, editable=False, verbose_name='Date created')),
                ('modified_date', models.DateField(blank=True, editable=False, verbose_name='Date modified')),
                ('delete_date', models.DateField(blank=True, editable=False, verbose_name='Date deleted')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='Name of product')),
                ('description', models.TextField(verbose_name='Description of product')),
                ('image', models.TextField(blank=True, max_length=100, null=True, verbose_name='Image product')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Product',
                'verbose_name_plural': 'historical Products',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalMeasureUnit',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(blank=True, editable=False, verbose_name='Date created')),
                ('modified_date', models.DateField(blank=True, editable=False, verbose_name='Date modified')),
                ('delete_date', models.DateField(blank=True, editable=False, verbose_name='Date deleted')),
                ('description', models.CharField(db_index=True, max_length=50, verbose_name='Description')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical MeasureUnit',
                'verbose_name_plural': 'historical MeasureUnits',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalIndicator',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(blank=True, editable=False, verbose_name='Date created')),
                ('modified_date', models.DateField(blank=True, editable=False, verbose_name='Date modified')),
                ('delete_date', models.DateField(blank=True, editable=False, verbose_name='Date deleted')),
                ('descount_value', models.PositiveIntegerField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('category_product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='products.categoryproduct', verbose_name='Category product')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Indicator',
                'verbose_name_plural': 'historical Indicators',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCategoryProduct',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(blank=True, editable=False, verbose_name='Date created')),
                ('modified_date', models.DateField(blank=True, editable=False, verbose_name='Date modified')),
                ('delete_date', models.DateField(blank=True, editable=False, verbose_name='Date deleted')),
                ('description', models.CharField(db_index=True, max_length=50, verbose_name='Description')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('measure_unit', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='products.measureunit', verbose_name='Unit of Measure')),
            ],
            options={
                'verbose_name': 'historical CategoryProduct',
                'verbose_name_plural': 'historical CategoryProducts',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='categoryproduct',
            name='measure_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.measureunit', verbose_name='Unit of Measure'),
        ),
    ]
