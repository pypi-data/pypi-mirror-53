# Generated by Django 2.0.9 on 2018-11-20 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terra', '0015_auto_20181005_1302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feature',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='featurerelation',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='layer',
            options={'ordering': ['id'], 'permissions': (('can_update_features_properties', 'Is able update geometries properties'),)},
        ),
        migrations.AlterModelOptions(
            name='layerrelation',
            options={'ordering': ['id']},
        ),
    ]
