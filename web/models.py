# This file is part of Lod4Stat.
#
# Copyright (C) 2014 Provincia autonoma di Trento
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Django models for l4s project.
"""

from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class Test3(models.Model):
    """
    Test with 3 columns.
    """
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    numerosity = models.IntegerField(_('numerosity'))


class Test4(models.Model):
    """
    Test with 4 columns.
    """
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    id3 = models.IntegerField()
    numerosity = models.IntegerField(_('numerosity'))


class Test5(models.Model):
    """
    Test with 5 columns.
    """
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    id3 = models.IntegerField()
    id4 = models.IntegerField()
    numerosity = models.IntegerField(_('numerosity'))


class TerritorialLevel(models.Model):
    """
    Territorial Level model.
    """
    name = models.CharField(max_length=255)


class OntologyFileModel(models.Model):
    """
    Ontology file.
    """
    name = models.CharField(max_length=255)
    upload = models.FileField(upload_to='ontologies')

    def delete(self, *args, **kwargs):
        """
        Delete ontology file and its model.

        :param args:
        :param kwargs:
        """
        self.upload.delete()
        super(OntologyFileModel, self).delete(*args, **kwargs)

    @property
    def __unicode__(self):
        """
        In unicode format.

        :return: Name in unicode.
        """
        return u'%s' % self.name


class Metadata(models.Model):
    """
    A Metadata used to add <key, value> to main db table and columns.
    """
    table_name = models.CharField(_('table name'), max_length=30, blank=False)
    column_name = models.CharField(_('column name'), max_length=30, null=True)
    key = models.CharField(_('key'), max_length=256, blank=False)
    value = models.CharField(_('value'), max_length=256, blank=False)


class ManualRequest(models.Model):
    """
    Model used in order to enable the user to do a manual request to be
    processed by an human user.
    """
    inquirer = models.ForeignKey("User", null=True)
    dispatcher = models.CharField(max_length=30, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    dispatch_date = models.DateTimeField(blank=True, null=True)
    dispatch_note = models.CharField(max_length=400,
                                     blank=True,
                                     null=True)
    subject = models.CharField(_('subject'), max_length=60, blank=False)
    goal = models.CharField(_('goal'), max_length=30, blank=False)
    topic = models.CharField(_('topic'), max_length=100, blank=False)
    requested_data = models.CharField(_('requested data'),
                                      max_length=400,
                                      blank=False)
    references_years = models.CharField(_('referenced years'),
                                        max_length=30,
                                        blank=False)
    territorial_level = models.CharField(_('territorial level'),
                                         max_length=30,
                                         blank=False)
    other_territorial_level = models.CharField(
        _('other territorial level (specify)'),
        max_length=30,
        blank=True)
    specific_territorial_level = models.CharField(
        _('specific territorial level'),
        max_length=400,
        blank=True)
    query = models.IntegerField(null=True)
    dispatched = models.BooleanField(default=False)


class UserType(models.Model):
    """
    A metadata to enrich the user with an user type.
    The user type contains some user types used for statistical purposes.
    """
    name = models.CharField(_('user type'), max_length=128)
    position = models.IntegerField()

    def __unicode__(self):
        """
        Retun the name in unicode format.

        :return: The name in unicode.
        """
        return self.name


class UserManager(BaseUserManager):
    """
    The User model has a custom manager that has
    the following helper methods
    (in addition to the methods provided by BaseUserManager).
    """

    def _create_user(self, email, password, is_staff, is_superuser,
                     is_man_req_dispatcher, **extra_fields):
        """
        Creates and saves a new user with the given email and password.

        :param email: Email.
        :param password: Password.
        :param is_staff: Is the user a staff member?
        :param is_superuser: Is the user a superuser)
        :param is_man_req_dispatcher: Can the user dispatch manual requests?
        :param extra_fields: Unused.
        """
        now = timezone.now()
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_manual_request_dispatcher=is_man_req_dispatcher,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create an user without password.

        :param email: Email.
        :param password: password.
        :param extra_fields: Unused
        :return: The created User.
        """
        return self._create_user(email, password, False, False, True,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a superuser.

        :param email:
        :param password:
        :param extra_fields:
        :return:The created User with super user privileges.
        """
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'),
                              max_length=128,
                              unique=True,
                              blank=False)

    first_name = models.CharField(_('first name'), max_length=32, blank=False)
    last_name = models.CharField(_('last name'), max_length=32, blank=False)
    phone_number = models.CharField(_('phone_number'),
                                    max_length=15,
                                    blank=True)

    user_type = models.ForeignKey("UserType", verbose_name=_('User type'),
                                  null=True)

    is_staff_hlp = _('Designates whether the user can log'
                     'into this admin site.')
    is_staff = models.BooleanField(_('staff status'),
                                   default=False,
                                   help_text=is_staff_hlp)

    is_manual_request_dispatcher_hlp = _(
        'Designates whether the user can receive '
        'manual request nofications.')
    is_manual_request_dispatcher = models.BooleanField(
        _('manual request dispatcher status'),
        default=False,
        help_text=is_manual_request_dispatcher_hlp)

    is_active_hlp = _('Designates whether this user should be treated as '
                      'active. Unselect this instead of deleting accounts.')
    is_active = models.BooleanField(_('active'),
                                    default=True,
                                    help_text=is_active_hlp)

    date_joined = models.DateTimeField(_('date joined'),
                                       default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        """
        Get the url with absolute path.

        :return: The absolute url.
        """
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.

        :return: The full user name.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.

        :return: The short user name.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.

        :param subject: Email subject.
        :param message: Email text message.
        :param from_email: Sender email address.
        """
        send_mail(subject, message, from_email, [self.email])