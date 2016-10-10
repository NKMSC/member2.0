# This Python file uses the following encoding: utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models




class Activity(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
    memo = models.TextField()

    class Meta:
        #managed = False
        db_table = 'activity'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        #managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.ForeignKey(AuthGroup)
    permission_id = models.ForeignKey('AuthPermission')

    class Meta:
        #managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=50)
    content_type_id = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
       # managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
       # managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.ForeignKey(AuthUser)
    group_id = models.ForeignKey(AuthGroup)

    class Meta:
        #managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.ForeignKey(AuthUser)
    permission_id = models.ForeignKey(AuthPermission)

    class Meta:
        #managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Code(models.Model):
    id = models.IntegerField(primary_key=True)
    use = models.ForeignKey('User')
    code = models.CharField(max_length=16)
    type = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    effective = models.IntegerField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'code'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()

    class Meta:
        #managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        #managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
       # managed = False
        db_table = 'django_site'


class EmailHistory(models.Model):
    student_id = models.CharField(max_length=20)
    time = models.DateTimeField()
    status = models.IntegerField()
    abstract = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    unused2 = models.CharField(max_length=100)

    class Meta:
      #  managed = False
        db_table = 'email_history'


class FreshMembers(models.Model):# memberqualifiction为笔误
    student_id = models.CharField(db_column='Student ID', max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=10, blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    mailbox = models.CharField(db_column='mailBox', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aspiration1 = models.CharField(max_length=20, blank=True, null=True)
    aspiration2 = models.CharField(max_length=20, blank=True, null=True)
    writtenscore = models.IntegerField(db_column='writtenScore', blank=True, null=True)  # Field name made lowercase.
    interviewperformance = models.IntegerField(db_column='interviewPerformance', blank=True, null=True)  # Field name made lowercase.
    interviewqualification = models.IntegerField(db_column='interviewQualification', blank=True, null=True)  # Field name made lowercase.
    memberqualifiction = models.IntegerField(db_column='memberQualifiction', blank=True, null=True)  # Field name made lowercase.
    finalaspiration = models.CharField(db_column='finalAspiration', max_length=20, blank=True, null=True)  # Field name made lowercase.
    campus = models.CharField(max_length=20, blank=True, null=True)
    register_year = models.IntegerField()

    class Meta:
     #   managed = False
        db_table = 'fresh members'


class Log(models.Model):
    id = models.IntegerField(primary_key=True)
    use = models.ForeignKey('User')
    content = models.TextField()
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
     #   managed = False
        db_table = 'log'


class Reg(models.Model):
    email = models.CharField(primary_key=True, max_length=64)
    mobile = models.CharField(max_length=32)
    realname = models.CharField(max_length=16)
    student_id = models.IntegerField()
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=8)
    graduateyear = models.CharField(max_length=10)
    major = models.CharField(max_length=32)
    degree = models.CharField(max_length=32)
    award = models.CharField(max_length=32)
    final_award = models.CharField(max_length=32)
    status = models.CharField(max_length=30)

    class Meta:
      #  managed = False
        db_table = 'reg'


class Section(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)
    profile = models.CharField(max_length=255)

    class Meta:
      #  managed = False
        db_table = 'section'


class User(models.Model):
    studentid = models.IntegerField(db_column='studentID', blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(primary_key=True)
    sec = models.ForeignKey(Section)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=160)
    name = models.CharField(max_length=8)
    sex = models.CharField(max_length=8)
    phone = models.CharField(max_length=16)
    school = models.CharField(max_length=16)
    college = models.CharField(max_length=32)
    major = models.CharField(max_length=32)
    entry_year = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=8)
    authority = models.BigIntegerField(blank=True, null=True)
    profile = models.CharField(max_length=255)
    position = models.CharField(max_length=16)
    open = models.BigIntegerField(blank=True, null=True)
    qq = models.CharField(max_length=16)
    province = models.CharField(max_length=16)
    city = models.CharField(max_length=16)
    area = models.CharField(max_length=16)
    effective = models.IntegerField(blank=True, null=True)
    campus = models.CharField(max_length=16)
    wechat = models.TextField()
    love = models.CharField(max_length=8)
    dormitory = models.CharField(max_length=16)

    class Meta:
      #  managed = False
        db_table = 'user'


class UserTakePartInActivity(models.Model):
    id = models.IntegerField(primary_key=True)
    use = models.ForeignKey(User)
    sign_in_time = models.DateTimeField(blank=True, null=True)

    class Meta:
       # managed = False
        db_table = 'user_take_part_in_activity'
