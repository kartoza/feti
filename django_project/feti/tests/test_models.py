# # coding=utf-8
# """Module related to test for all the models."""
# from django.test import TestCase
#
# from feti.tests.model_factories import FloodStatusFactory
#
#
# class TestFloodStatus(TestCase):
#     """Class to test FloodStatus model."""
#     def setUp(self):
#         pass
#
#     def test_create_flood_status(self):
#         """Method to test flood_status creation."""
#         flood_status = FloodStatusFactory.create()
#         message = 'The flood_status is not instantiated successfully.'
#         self.assertIsNotNone(flood_status.id, message)
#
#     def test_read_flood_status(self):
#         """Method to test reading flood_status."""
#         flood_status_name = 'Testing FloodStatus'
#         flood_status = FloodStatusFactory.create(name=flood_status_name)
#         message = 'The flood_status name should be %s, but it gives %s' % (
#             flood_status_name, flood_status.name)
#         self.assertEqual(flood_status_name, flood_status.name, message)
#
#     def test_update_flood_status(self):
#         """Method to test updating flood_status."""
#         flood_status = FloodStatusFactory.create(name='Testing User')
#         flood_status_name = 'Updated Testing User'
#         flood_status.name = flood_status_name
#         flood_status.save()
#         message = 'The flood_status name should be %s, but it gives %s' % (
#             flood_status_name, flood_status.name)
#         self.assertEqual(flood_status_name, flood_status.name, message)
#
#     def test_delete_flood_status(self):
#         """Method to test deleting flood_status."""
#         flood_status = FloodStatusFactory.create()
#         self.assertIsNotNone(flood_status.id)
#         flood_status.delete()
#         message = 'The flood_status is not deleted.'
#         self.assertIsNone(flood_status.id, message)
