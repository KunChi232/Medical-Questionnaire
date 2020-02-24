# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Question(models.Model):
    question_type = models.TextField()
    name = models.TextField()
    question_count = models.IntegerField()
    wellcome = models.TextField()
    questions = models.TextField()
    summary = models.TextField()

    class Meta:
        managed = False
        db_table = 'question'


class Record(models.Model):
    line_id = models.TextField()
    session_id = models.TextField()
    question_type = models.TextField()
    name = models.TextField()
    user_select = models.TextField()
    next_question = models.IntegerField()
    complete = models.IntegerField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'record'


class Users(models.Model):
    line_id = models.TextField()
    scores = models.TextField()
    current_session = models.TextField()

    class Meta:
        managed = False
        db_table = 'users'
