import StringIO
from django.db.models.query import ValuesQuerySet, QuerySet

class CSVResponse(HttpResponse):

  def __init__(self, data, output_name='data', headers=None, encoding='utf8'):
    valid_data = False
    if isinstance(data, ValuesQuerySet):
        data = list(data)
    elif isinstance(data, QuerySet):
        data = list(data.values())
    if hasattr(data, '__getitem__'):
        if isinstance(data[0], dict):
            if headers is None:
                headers = data[0].keys()
            data = [[row[col] for col in headers] for row in data]
            data.insert(0, headers)
        if hasattr(data[0], '__getitem__'):
            valid_data = True
    assert valid_data is True, "CSVResponse requires a sequence of sequences"

    output = StringIO.StringIO()
    for row in data:
        out_row = []
        for value in row:
            if not isinstance(value, basestring):
                value = unicode(value)
            value = value.encode(encoding)
            out_row.append(value.replace('"', '""'))
        output.write('"%s"\n' %
                     '","'.join(out_row))            
    mimetype = 'text/csv'
    file_ext = 'csv'
    output.seek(0)
    super(CSVResponse, self).__init__(content=output.getvalue(),
                                        mimetype=mimetype)
    self['Content-Disposition'] = 'attachment;filename="%s.%s"' % \
        (output_name.replace('"', '\"'), file_ext)