# Generated by Django 4.2.3 on 2023-07-22 08:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("creators", "0003_alter_channelbasic_options_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ChannelBasic",
        ),
    ]
