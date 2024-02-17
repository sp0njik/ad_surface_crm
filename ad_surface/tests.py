from django.test import TestCase
from ad_surface.models import Surface
from customer.models import Placement
from datetime import datetime, timedelta

class CheckFreeSufacesTestCase(TestCase):
    def test_get_free_surfaces(self):
        surface = Surface.objects.create(name='s1', description='d1', width=1200, height=800, price=700m, adress='address', place='place', is_active=True)
        start_at = datetime.now() - timedelta(days=2)
        placement = Placement.objects.create(start_at=start_at, duration=timedelta(days=4))