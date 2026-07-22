from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('db', '001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('alert_name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='alerts',
            index=models.Index(fields=['user_id']),
        ),
        migrations.AddIndex(
            model_name='alerts',
            index=models.Index(fields=['category']),
        ),
        migrations.AddIndex(
            model_name='alerts',
            index=models.Index(fields=['region']),
        ),
    ]
