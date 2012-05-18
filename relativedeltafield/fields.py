from django.db import models
from dateutil.relativedelta import relativedelta
from forms import RelativedeltaField as RelativedeltaFormField

class RelativedeltaField(models.Field):

    description = "A relative timedelta"

    __metaclass__ = models.SubfieldBase

    def db_type(self, connection=None):
        """
        Current representation of RelativedeltaField in the database.
        """
        return 'char(30)'

    def to_python(self, value):
        """
        Creates a relativedelta object from what we get from the database.
        """
        if not value:
            return None
        if isinstance(value, (str, unicode)):
            #raises ValueError if split not possible.
            years, months, days, hours, minutes, seconds = [int(v)
                                         for v
                                         in value.split("_")]
            return relativedelta(years   = years,
                                 months  = months,
                                 days    = days,
                                 hours   = hours,
                                 minutes = minutes,
                                 seconds = seconds)
        elif isinstance(value, relativedelta):
            return value
        else:
            return None

    def get_db_prep_value(self, value, connection=None, prepared=False):
        """
        Concatenate unit and timedelta into a string.
        """
        return "%i_%i_%i_%i_%i_%i" % (value.years,
                                      value.months,
                                      value.days,
                                      value.hours,
                                      value.minutes,
                                      value.seconds)

    def formfield(self, **kwargs):
        """
        Using a RelativedeltaField to represent this field in a form.
        """
        defaults = { 'form_class' : RelativedeltaFormField }
        defaults.update(kwargs)
        return super(RelativedeltaField, self).formfield(**defaults)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

