# Generated by Django 2.0.9 on 2018-10-12 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_generator', '0003_auto_20180911_0827'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documenttemplate',
            options={'permissions': (('can_upload_template', 'Is allowed to upload a template'), ('can_update_template', 'Is allowed to update a template'), ('can_delete_template', 'Is allowed to delete a template'))},
        ),
        migrations.AlterField(
            model_name='documenttemplate',
            name='documenttemplate',
            field=models.FileField(upload_to='templates/%Y/%m/'),
        ),
    ]
