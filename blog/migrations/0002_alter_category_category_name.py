# Generated by Django 3.2.2 on 2021-05-09 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(choices=[('world', 'World'), ('environment', 'Environment'), ('technology', 'Technology'), ('design', 'Design'), ('culture', 'Culture'), ('travel', 'Travel'), ('style', 'Style'), ('health', 'Health'), ('science', 'Science'), ('opinion', 'Opinion'), ('politics', 'Politics'), ('business', 'Business')], default='World', max_length=20),
        ),
    ]
