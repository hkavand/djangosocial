# Generated by Django 4.2.1 on 2023-05-22 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_comment_parent_alter_post_likes_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
