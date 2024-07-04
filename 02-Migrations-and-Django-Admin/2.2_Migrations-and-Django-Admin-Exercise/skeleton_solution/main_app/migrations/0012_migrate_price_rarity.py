# Generated by Django 5.0.4 on 2024-07-04 12:21

from django.db import migrations


def set_price_rarity(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')
    
    items = item_model.objects.all()
    
    for item in items:
        if item.price <= 10:
            item.rarity = 'Rare'
        elif item.price <= 20:
            item.rarity = 'Very Rare'
        elif item.price <= 30:
            item.rarity = 'Extremely Rare'
        else:
            item.rarity = 'Mega Rare'
    
    item_model.objects.bulk_update(items, ['rarity'])
    

def set_price_rarity_default(apps, shcema_editor):
    item_model = apps.get_model('main_app', 'Item')
    
    for item in item_model.objects.all():
        item.rarity = item_model._meta.get_field('rarity').default
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_item'),
    ]

    operations = [
        migrations.RunPython(set_price_rarity, set_price_rarity_default)
    ]
