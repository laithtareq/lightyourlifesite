# Generated by Django 2.2.2 on 2020-01-16 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('Presence_times', models.IntegerField(default=0)),
                ('post_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('Dep_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Dep')),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_update', models.DateTimeField(auto_now=True)),
                ('Material_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Material')),
                ('Teacher_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher_Free',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Days', models.CharField(max_length=20)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('Free_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Teacher')),
                ('Material_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Material')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Days', models.CharField(max_length=20)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('Section_Class', models.IntegerField()),
                ('Section_Num', models.IntegerField()),
                ('Material_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Material')),
                ('Teacher_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Presence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Presence_Date', models.DateField()),
                ('Booking_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Booking')),
                ('Section_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Section')),
                ('Student_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='newAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('file', models.FileField(default='logo.jpg', upload_to='Ad_Files')),
                ('text', models.TextField(default='وصف الاعلان')),
                ('expirDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_update', models.DateTimeField(auto_now=True)),
                ('Material_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Material')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quastion_text', models.CharField(max_length=20)),
                ('Quastion_title', models.TextField()),
                ('Max_mark', models.IntegerField()),
                ('Dead_line', models.DateField()),
                ('Sugested_answer', models.CharField(default='', max_length=20)),
                ('Section_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Section')),
            ],
        ),
        migrations.CreateModel(
            name='fillForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times', models.CharField(max_length=20)),
                ('booked', models.BooleanField(default=False)),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_update', models.DateTimeField(auto_now=True)),
                ('Material_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Material')),
                ('Student_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='filled_Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Students_Count', models.IntegerField(default=0)),
                ('Material_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Material')),
            ],
        ),
        migrations.AddField(
            model_name='dep',
            name='Specialty_Key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Specialty'),
        ),
        migrations.AddField(
            model_name='booking',
            name='Section_Key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Section'),
        ),
        migrations.AddField(
            model_name='booking',
            name='Student_User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Answer', models.TextField()),
                ('Mark', models.IntegerField(default=0)),
                ('Trials', models.IntegerField(default=0)),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_update', models.DateTimeField(auto_now=True)),
                ('Homework_Key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bloger.Homework')),
                ('Student_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
