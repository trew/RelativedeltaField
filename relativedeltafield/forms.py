from django import forms
from dateutil.relativedelta import relativedelta

class RelativedeltaWidget(forms.MultiWidget):
    def __init__(self, widgets=None, *args, **kwargs):
        if widgets is None:
            widgets = [forms.TextInput(attrs={'style':'width:20px;'})
                       for x
                       in range(5)]
        super(RelativedeltaWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, values):
        if values:
            return values
        return ""

    def _has_changed(self, initial, data):
        initial = (initial.months + initial.year*12,
                   initial.days,
                   initial.hours,
                   initial.minutes,
                   initual.seconds)
        return initial == data

    def format_output(self, rendered_widgets):
        labels = [  "Mon",
                    "Day",
                    "Hou",
                    "Min",]
        output = []
        output.append("<table>")
        for widget in rendered_widgets:
            output.append("<td>")
            output.append("%s" %\
                                widget)
            output.append("</td>")
        output.append("</tr>")
        output.append("</table>")
        output.append("<span style='font-size:10px;'>")
        output.append("(Months / Days / Hours / Minutes / Seconds)")
        output.append("</span>")
        return u'\n'.join(output)

class RelativedeltaField(forms.Field):
    """
    A field to provide ability to make relative deltas.
    """
    widget = RelativedeltaWidget

    def prepare_value(self, value):
        if value is not None:
            if not isinstance(value, relativedelta):
                value = self.clean(value)
            return (value.months + value.years*12,
                    value.days,
                    value.hours,
                    value.minutes,
                    value.seconds)
        else:
            return None

    def clean(self, values):
        def to_int(v):
            try:
                return int(v)
            except:
                return 0
        (months, days, hours, minutes, seconds) = [to_int(v)
                                                   for v
                                                   in values]
        return relativedelta(months  = months,
                             days    = days,
                             hours   = hours,
                             minutes = minutes,
                             seconds = seconds)
