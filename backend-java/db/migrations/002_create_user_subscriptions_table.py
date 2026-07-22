from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=255)),
                ('notification_method', models.CharField(max_length=100)),
                ('user_id', models.ForeignKey(on_delete=models.CASCADE, to='users.User')),
            ],
        ),
        migrations.AddIndex(
            model_name='usersubscription',
            index=models.Index(fields=['event_type']),
        ),
        migrations.AddIndex(
            model_name='usersubscription',
            index=models.Index(fields=['notification_method']),
        ),
    ]
