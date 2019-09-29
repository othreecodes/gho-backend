# Generated by Django 2.1.9 on 2019-09-29 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_balance_subscription_usersubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllBanks',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('acronym', models.CharField(max_length=50)),
                ('bank_code', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'All Banks',
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=50)),
                ('account_type', models.CharField(max_length=50)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.AllBanks')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorization_code', models.CharField(max_length=200)),
                ('ctype', models.CharField(max_length=200)),
                ('cbin', models.CharField(default=None, max_length=200)),
                ('cbrand', models.CharField(default=None, max_length=200)),
                ('country_code', models.CharField(default=None, max_length=200)),
                ('first_name', models.CharField(default=None, max_length=200)),
                ('last_name', models.CharField(default=None, max_length=200)),
                ('number', models.CharField(max_length=200)),
                ('bank', models.CharField(max_length=200)),
                ('expiry_month', models.CharField(max_length=10)),
                ('expiry_year', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Gho Rewards',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('reference', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('amount', models.FloatField(default=0.0)),
                ('new_balance', models.FloatField(default=0.0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='balance',
            options={'verbose_name': 'Gho Balance', 'verbose_name_plural': 'Gho Balances'},
        ),
        migrations.AlterModelOptions(
            name='phonenumber',
            options={'verbose_name': 'Phone Number'},
        ),
        migrations.AlterModelOptions(
            name='referral',
            options={'verbose_name': 'User referral'},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Gho Subscription Package'},
        ),
        migrations.AlterModelOptions(
            name='usersubscription',
            options={'verbose_name': 'Users that have Subcribed', 'verbose_name_plural': 'Users that have Subcribed'},
        ),
        migrations.AlterField(
            model_name='subscription',
            name='discount',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='BankTransfer',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Transaction')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Bank')),
            ],
            options={
                'verbose_name_plural': 'Bank Transfers',
            },
            bases=('users.transaction',),
        ),
        migrations.CreateModel(
            name='P2PTransfer',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Transaction')),
                ('receipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'P2P Transfers',
            },
            bases=('users.transaction',),
        ),
        migrations.AddField(
            model_name='transaction',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reward',
            name='refferal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Referral'),
        ),
        migrations.AddField(
            model_name='reward',
            name='reward_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reward',
            name='user_subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserSubscription'),
        ),
    ]
