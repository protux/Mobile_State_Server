# Generated by Django 2.1.1 on 2018-10-07 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mosta.base.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('power', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[mosta.base.validators.positive_or_zero_number])),
            ],
        ),
        migrations.CreateModel(
            name='CallHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_number', models.CharField(max_length=20)),
                ('destination_number', models.CharField(max_length=20)),
                ('started', models.DateTimeField()),
                ('ended', models.DateTimeField()),
                ('direction', models.CharField(choices=[('in', 'Inbound'), ('out', 'Outbound'), ('u', 'Unknown')], max_length=3)),
                ('hangup_reason', models.CharField(choices=[('abort', 'Aborted'), ('callee_hung_up', 'Callee hung up'), ('caller_hung_up', 'Caller hung up'), ('unknown', 'Unknown')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ChargingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('issue_type', models.CharField(choices=[('requested_charging', 'Requested charging'), ('announced_charging', 'Announced charging'), ('announced_full_battery', 'Announced full battery'), ('stopped_charging', 'Stopped charging')], max_length=25)),
                ('battery_state', models.IntegerField(validators=[mosta.base.validators.number_between_zero_and_one_hundred])),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=20)),
                ('battery_level', models.IntegerField(blank=True, null=True, validators=[mosta.base.validators.number_between_zero_and_one_hundred])),
                ('needs_charging', models.BooleanField(default=False)),
                ('state', models.CharField(choices=[('calling', 'Calling'), ('idle', 'Idle'), ('switched_off', 'Switched off'), ('removed', 'Removed from pool'), ('unknown', 'Unknown')], default='idle', max_length=15)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('attached_power_socket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='power.PowerSocket')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=20)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[mosta.base.validators.positive_or_zero_number])),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('can_call', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phone.Phone')),
            ],
        ),
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=20)),
                ('content', models.CharField(max_length=160)),
                ('time_received', models.DateTimeField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phone.Sim')),
            ],
        ),
        migrations.AddField(
            model_name='charginghistory',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phone.Phone'),
        ),
        migrations.AddField(
            model_name='callhistory',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phone.Sim'),
        ),
        migrations.AddField(
            model_name='callhistory',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='balancehistory',
            name='sim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phone.Sim'),
        ),
        migrations.AlterUniqueTogether(
            name='sim',
            unique_together={('owner', 'label')},
        ),
        migrations.AlterUniqueTogether(
            name='phone',
            unique_together={('owner', 'label')},
        ),
    ]
