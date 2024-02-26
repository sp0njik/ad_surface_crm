from django.test import TestCase
from django.utils import timezone

from ad_surface.models import Surface
from customer.models import Company, Placement

from datetime import timedelta


class CompanyPageTestCase(TestCase):

    def test_company_page_success(self):
        cocmpany = Company.objects.create(name='Test Company', phone='123456789', legal_address='Test Address',
                                          actual_address='Test Address', inn='123456789', kpp='123456789',
                                          ogrn='123456789', checking_account='123456789',
                                          correspondent_account='123456789', bik='123456789', bank_name='Test Bank',
                                          bank_address='Test Address', is_agency=False, agency=None)
        surface = Surface.objects.create(name='Test Surface', description='Test Description', width=10, height=10,
                                         price=100, address='Test Address', place='Test Place', is_active=True)

        surface_2 = Surface.objects.create(name='Test Surface 2', description='Test Description 2', width=20, height=20,
                                           price=200, address='Test Address2', place='Test Place2', is_active=False)
        start_at = timezone.now() - timedelta(days=2)
        placement = Placement.objects.create(surface=surface, company=cocmpany, start_at=start_at,
                                             duration=timedelta(days=4))
        start_at = timezone.now() - timedelta(days=5)
        placement_2 = Placement.objects.create(surface=surface_2, company=cocmpany, start_at=start_at,
                                               duration=timedelta(days=3))
        with self.assertNumQueries(3):
            response = self.client.get('/customer/company/1/')
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, 'Test Company')
            # self.assertInHTML('<p><input type="text" name="phone"  value="123456789"></p>',
            #                   response.content.decode("utf-8"))
            self.assertEqual(cocmpany, response.context['company'])
            self.assertContains(response, placement.surface.name)
            self.assertContains(response, placement.start_at.strftime("%d.%m.%Y"))
            self.assertContains(response, placement.finish_at().strftime("%d.%m.%Y"))
