# Generated by Django 2.2.12 on 2020-11-06 06:42

from django.db import migrations, models
import django.db.models.deletion
import otree.db.idmap
import otree.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='red_line_lottery_group', to='otree.Session')),
            ],
            options={
                'db_table': 'red_line_lottery_group',
            },
            bases=(models.Model, otree.db.idmap.GroupIDMapMixin),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='red_line_lottery_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'red_line_lottery_subsession',
            },
            bases=(models.Model, otree.db.idmap.SubsessionIDMapMixin),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_role', otree.db.models.StringField(max_length=10000, null=True)),
                ('choice_1', otree.db.models.BooleanField(choices=[(True, 'A'), (False, 'B')], null=True, verbose_name='\n        <td>10%</td>\n        <td>20</td>\n        <td>90%</td>\n        <td>16</td>\n        <td>10%</td>\n        <td>38.5</td>\n        <td>90%</td>\n        <td>1</td>\n    ')),
                ('choice_2', otree.db.models.BooleanField(choices=[(True, 'A'), (False, 'B')], null=True, verbose_name='\n        <td>20%</td>\n        <td>20</td>\n        <td>80%</td>\n        <td>16</td>\n        <td>20%</td>\n        <td>38.5</td>\n        <td>80%</td>\n        <td>1</td>\n    ')),
                ('choice_3', otree.db.models.BooleanField(choices=[(True, 'A'), (False, 'B')], null=True, verbose_name='\n        <td>30%</td>\n        <td>20</td>\n        <td>70%</td>\n        <td>16</td>\n        <td>30%</td>\n        <td>38.5</td>\n        <td>70%</td>\n        <td>1</td>\n    ')),
                ('choice_4', otree.db.models.BooleanField(choices=[(True, 'A'), (False, 'B')], null=True, verbose_name='\n        <td>40%</td>\n        <td>20</td>\n        <td>60%</td>\n        <td>16</td>\n        <td>40%</td>\n        <td>38.5</td>\n        <td>60%</td>\n        <td>1</td>\n    ')),
                ('choice_5', otree.db.models.BooleanField(choices=[(True, 'A'), (False, 'B')], null=True, verbose_name='\n        <td>50%</td>\n        <td>20</td>\n        <td>50%</td>\n        <td>16</td>\n        <td>50%</td>\n        <td>38.5</td>\n        <td>50%</td>\n        <td>1</td>\n    ')),
                ('choice_6', otree.db.models.BooleanField(choices=[(True, 'A'), (False, 'B')], null=True, verbose_name='\n        <td>60%</td>\n        <td>20</td>\n        <td>40%</td>\n        <td>16</td>\n        <td>60%</td>\n        <td>38.5</td>\n        <td>40%</td>\n        <td>1</td>\n    ')),
                ('choice_7', otree.db.models.BooleanField(choices=[(True, 'A'), (False, 'B')], null=True, verbose_name='\n        <td>70%</td>\n        <td>20</td>\n        <td>30%</td>\n        <td>16</td>\n        <td>70%</td>\n        <td>38.5</td>\n        <td>30%</td>\n        <td>1</td>\n    ')),
                ('choice_8', otree.db.models.BooleanField(choices=[(True, 'A'), (False, 'B')], null=True, verbose_name='\n        <td>80%</td>\n        <td>20</td>\n        <td>20%</td>\n        <td>16</td>\n        <td>80%</td>\n        <td>38.5</td>\n        <td>20%</td>\n        <td>1</td>\n    ')),
                ('choice_9', otree.db.models.BooleanField(choices=[(True, 'A'), (False, 'B')], null=True, verbose_name='\n        <td>90%</td>\n        <td>20</td>\n        <td>10%</td>\n        <td>16</td>\n        <td>90%</td>\n        <td>38.5</td>\n        <td>10%</td>\n        <td>1</td>\n    ')),
                ('choice_10', otree.db.models.BooleanField(choices=[(True, 'A'), (False, 'B')], null=True, verbose_name='\n        <td>100%</td>\n        <td>20</td>\n        <td>0%</td>\n        <td>16</td>\n        <td>100%</td>\n        <td>38.5</td>\n        <td>0%</td>\n        <td>1</td>\n    ')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='red_line_lottery.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='red_line_lottery_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='red_line_lottery_player', to='otree.Session')),
                ('subsession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='red_line_lottery.Subsession')),
            ],
            options={
                'db_table': 'red_line_lottery_player',
            },
            bases=(models.Model, otree.db.idmap.PlayerIDMapMixin),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='red_line_lottery.Subsession'),
        ),
    ]
