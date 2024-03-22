from django.test import TestCase

from ad_surface.models import Surface


# from customer.models import Placement
# from datetime import datetime, timedelta
#
#
# class CheckFreeSufacesTestCase(TestCase):
#     def test_get_free_surfaces(self):
#         surface = Surface.objects.create(name='s1', description='d1', width=1200, height=800, price=700,
#                                          adress='address', place='place', is_active=True)
#         start_at = datetime.now() - timedelta(days=2)
#         placement = Placement.objects.create(start_at=start_at, duration=timedelta(days=4))

class CheckSurfaceTestCase(TestCase):
    def test_check_area(self):
        surface = Surface.objects.create(name='test_name', description='test_description', width=15600, height=6500,
                                         price=50000,
                                         address='test_address', place='test_place')
        self.assertEquals(surface.get_area(), 101.4)


class CheckActiveManagerTestCase(TestCase):
    def test_check_active_surfaces(self):
        surface_1 = Surface.objects.create(name='test_name1', description='test_description1', width=15600, height=6500,
                                           price=50000,
                                           address='test_address', place='test_place')
        surface_2 = Surface.objects.create(name='test_name2', description='test_description2', width=15600, height=6500,
                                           price=50000,
                                           address='test_address', place='test_place', is_active=False)
        surface_3 = Surface.objects.create(name='test_name3', description='test_description', width=15600, height=6500,
                                           price=50000,
                                           address='test_address', place='test_place')
        surface_4 = Surface.objects.create(name='test_name4', description='test_description', width=15600, height=6500,
                                           price=50000,
                                           address='test_address', place='test_place', is_active=False)

        self.assertListEqual([surface_1, surface_3], list(Surface.active_surfaces.all()))
