# Generated by Django 5.1.3 on 2024-11-25 21:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('host_id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('os', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HostStats',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('time', models.DateTimeField()),
                ('cpu_percent', models.FloatField()),
                ('ram_total', models.IntegerField()),
                ('ram_available', models.IntegerField()),
                ('ram_used', models.IntegerField()),
                ('os', models.CharField(max_length=255)),
                ('platform', models.CharField(max_length=255)),
                ('platform_version', models.CharField(max_length=255)),
                ('processes', models.IntegerField()),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='system_monitor.host')),
            ],
        ),
    ]
