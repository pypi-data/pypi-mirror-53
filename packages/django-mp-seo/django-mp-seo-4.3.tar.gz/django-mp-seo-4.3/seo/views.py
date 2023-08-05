
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from seo.models import RedirectRecord, ErrorRecord


def page_not_found(request, **kwargs):

    path = request.path

    try:
        record = RedirectRecord.objects.get(old_path=path)
        return redirect(record.new_path, permanent=True)
    except RedirectRecord.DoesNotExist:
        pass

    if not path.startswith('/static/') and not path.startswith('/media/'):
        ErrorRecord.create(request, 404)

    return render(request, '404.html')
