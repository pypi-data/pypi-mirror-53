# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.test.client import Client

from .testapp.models import SortableBook


FIXTURES = ['data.json', ]


class SortableBookTestCase(TestCase):
    fixtures = FIXTURES
    admin_password = 'secret'
    ajax_update_url = reverse('admin:testapp_sortablebook_update')
    bulk_update_url = reverse('admin:testapp_sortablebook_changelist')
    client = Client()
    http_headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def setUp(self):
        self.createAdminUser()

    def createAdminUser(self):
        self.user = User.objects.create_user(
            'admin', 'admin@example.com', self.admin_password
        )
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        logged_in = self.client.login(
            username=self.user.username, password=self.admin_password
        )
        self.assertTrue(logged_in, 'User is not logged in')

    def assertUniqueOrderValues(self):
        """
        always starting at 1!
        :return:
        """
        val = 0
        for obj in SortableBook.objects.order_by('my_order'):
            val += 1
            self.assertEqual(
                obj.my_order, val, 'Inconsistent order value on SortableBook'
            )

    def assertResponseCheck(self, in_data, raw_out_data):
        """
        TODO: what do we want to check the response for?
        """
        return
        out_data = json.loads(raw_out_data)
        startorder = in_data['startorder']
        endorder = in_data.get('endorder', 0)
        if startorder < endorder:
            self.assertEqual(len(out_data), endorder - startorder + 1)
        elif startorder > endorder:
            self.assertEqual(len(out_data), startorder - endorder + 1)
        else:
            self.assertEqual(len(out_data), 0)

    def testFilledBookShelf(self):
        self.assertEqual(
            SortableBook.objects.count(),
            20,
            'Check fixtures/data.json: Book shelf shall have 20 items')
        self.assertUniqueOrderValues()

    def test_move_down_right(self):
        three_pk = SortableBook.objects.get(my_order=3).pk
        five_pk = SortableBook.objects.get(my_order=5).pk
        six_pk = SortableBook.objects.get(my_order=6).pk
        seven_pk = SortableBook.objects.get(my_order=7).pk
        in_data = {'obj': three_pk, 'position': 'right', 'target': six_pk}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseCheck(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=three_pk).my_order, 6)
        self.assertEqual(SortableBook.objects.get(pk=five_pk).my_order, 4)
        self.assertEqual(SortableBook.objects.get(pk=six_pk).my_order, 5)
        self.assertEqual(SortableBook.objects.get(pk=seven_pk).my_order, 7)

    def test_move_down_left(self):
        return
        three_pk = SortableBook.objects.get(my_order=3).pk
        five_pk = SortableBook.objects.get(my_order=5).pk
        six_pk = SortableBook.objects.get(my_order=6).pk
        seven_pk = SortableBook.objects.get(my_order=7).pk
        in_data = {'obj': three_pk, 'position': 'left', 'target': six_pk}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseCheck(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=three_pk).my_order, 5)
        self.assertEqual(SortableBook.objects.get(pk=five_pk).my_order, 4)
        self.assertEqual(SortableBook.objects.get(pk=six_pk).my_order, 6)
        self.assertEqual(SortableBook.objects.get(pk=seven_pk).my_order, 7)

    def test_move_up_right(self):
        three_pk = SortableBook.objects.get(my_order=3).pk
        six_pk = SortableBook.objects.get(my_order=6).pk
        seven_pk = SortableBook.objects.get(my_order=7).pk
        in_data = {'obj': seven_pk, 'position': 'right', 'target': three_pk}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseCheck(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=seven_pk).my_order, 4)
        self.assertEqual(SortableBook.objects.get(pk=three_pk).my_order, 3)
        self.assertEqual(SortableBook.objects.get(pk=six_pk).my_order, 7)

    def test_move_up_left(self):
        three_pk = SortableBook.objects.get(my_order=3).pk
        six_pk = SortableBook.objects.get(my_order=6).pk
        seven_pk = SortableBook.objects.get(my_order=7).pk
        in_data = {'obj': seven_pk, 'position': 'left', 'target': three_pk}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseCheck(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=seven_pk).my_order, 3)
        self.assertEqual(SortableBook.objects.get(pk=three_pk).my_order, 4)
        self.assertEqual(SortableBook.objects.get(pk=six_pk).my_order, 7)

    def test_dontMove(self):
        seven_pk = SortableBook.objects.get(my_order=7).pk
        six_pk = SortableBook.objects.get(my_order=6).pk
        in_data = {'obj': seven_pk, 'position': 'right', 'target': six_pk}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseCheck(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=seven_pk).my_order, 7)

    def est_move_first_last_of_page(self):
        one_pk = SortableBook.objects.get(my_order=1).pk
        in_data = {'startorder': 1, 'endorder': 8}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseSequenceLength(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 8)

    def est_move_last_first_of_page(self):
        one_pk = SortableBook.objects.get(my_order=8).pk
        in_data = {'startorder': 8, 'endorder': 1}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseSequenceLength(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 1)

    """
    obsolete??!
    """
    def est_reverseMoveUp(self):
        self.assertEqual(SortableBook.objects.get(pk=12).my_order, 12)
        in_data = {'startorder': 12, 'endorder': 16}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseSequenceLength(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=12).my_order, 16)
        self.assertEqual(SortableBook.objects.get(pk=13).my_order, 12)

    def est_reverseMoveDown(self):
        self.assertEqual(SortableBook.objects.get(pk=12).my_order, 12)
        in_data = {'startorder': 12, 'endorder': 7}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseSequenceLength(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=12).my_order, 7)
        self.assertEqual(SortableBook.objects.get(pk=11).my_order, 12)

    def est_reverseDontMove(self):
        self.assertEqual(SortableBook.objects.get(pk=14).my_order, 14)
        in_data = {'startorder': 14, 'endorder': 14}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseSequenceLength(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=14).my_order, 14)
    """
    end obsolete
    """

    def est_moveFirst(self):
        second_pk = SortableBook.objects.get(my_order=2).pk
        in_data = {'startorder': 2, 'endorder': 1}
        response = self.client.post(self.ajax_update_url, in_data, **self.http_headers)
        self.assertEqual(response.status_code, 200)
        self.assertResponseSequenceLength(in_data, response.content.decode('utf-8'))
        self.assertUniqueOrderValues()
        self.assertEqual(SortableBook.objects.get(pk=second_pk).my_order, 1)

    def est_bulkMovePrevFromFirstPageDoesNothing(self):
        """
        not sure if intended like this
        """
        fourteen_pk = SortableBook.objects.get(my_order=14).pk
        fifteen_pk = SortableBook.objects.get(my_order=15).pk
        post_data = {'action': ['move_to_back_page'], 'step': 1, '_selected_action': [14, 15]}
        self.client.post(self.bulk_update_url, post_data)
        self.assertEqual(SortableBook.objects.get(pk=fourteen_pk).my_order, 14)
        self.assertEqual(SortableBook.objects.get(pk=fifteen_pk).my_order, 15)

    def est_bulkMovePreviousPage(self):
        seventeen_pk = SortableBook.objects.get(my_order=17).pk
        eighteen_pk = SortableBook.objects.get(my_order=18).pk
        nineteen_pk = SortableBook.objects.get(my_order=19).pk
        post_data = {'action': ['move_to_back_page'], 'step': 1, '_selected_action': [seventeen_pk, eighteen_pk, nineteen_pk]}
        self.client.post(self.bulk_update_url + '?p=1', post_data)
        self.assertEqual(SortableBook.objects.get(pk=seventeen_pk).my_order, 1)
        self.assertEqual(SortableBook.objects.get(pk=eighteen_pk).my_order, 2)
        self.assertEqual(SortableBook.objects.get(pk=nineteen_pk).my_order, 3)

    def est_bulkMoveForwardFromLastPage(self):
        one_pk = SortableBook.objects.get(my_order=19).pk
        two_pk = SortableBook.objects.get(my_order=20).pk
        post_data = {'action': ['move_to_forward_page'], 'step': 1, '_selected_action': [one_pk, two_pk]}
        self.client.post(self.bulk_update_url + '?p=2', post_data)
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 19)
        self.assertEqual(SortableBook.objects.get(pk=two_pk).my_order, 20)

    def est_bulkMoveNextPage(self):
        one_pk = SortableBook.objects.get(my_order=17).pk
        two_pk = SortableBook.objects.get(my_order=18).pk
        post_data = {'action': ['move_to_forward_page'], 'step': 1, '_selected_action': [one_pk, two_pk]}
        self.client.post(self.bulk_update_url + '?p=1', post_data)
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 17)
        self.assertEqual(SortableBook.objects.get(pk=two_pk).my_order, 18)

    def est_bulkMoveLastPage(self):
        one_pk = SortableBook.objects.get(my_order=1).pk
        two_pk = SortableBook.objects.get(my_order=6).pk
        post_data = {'action': ['move_to_last_page'], '_selected_action': [one_pk, two_pk]}
        self.client.post(self.bulk_update_url, post_data)
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 17)
        self.assertEqual(SortableBook.objects.get(pk=two_pk).my_order, 18)

    def est_bulkMoveFirstPage(self):
        one_pk = SortableBook.objects.get(my_order=17).pk
        two_pk = SortableBook.objects.get(my_order=20).pk
        post_data = {'action': ['move_to_first_page'], '_selected_action': [one_pk, two_pk]}
        self.client.post(self.bulk_update_url + '?p=2', post_data)
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 1)
        self.assertEqual(SortableBook.objects.get(pk=two_pk).my_order, 2)

    def est_bulkMoveBackTwoPages(self):
        one_pk = SortableBook.objects.get(my_order=17).pk
        two_pk = SortableBook.objects.get(my_order=20).pk
        post_data = {'action': ['move_to_back_page'], 'step': 2, '_selected_action': [17, 20]}
        self.client.post(self.bulk_update_url + '?p=2', post_data)
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 1)
        self.assertEqual(SortableBook.objects.get(pk=two_pk).my_order, 2)

    def est_bulkMoveForwardTwoPages(self):
        one_pk = SortableBook.objects.get(my_order=1).pk
        two_pk = SortableBook.objects.get(my_order=6).pk
        post_data = {'action': ['move_to_forward_page'], 'step': 2, '_selected_action': [one_pk, two_pk]}
        self.client.post(self.bulk_update_url, post_data)
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 17)
        self.assertEqual(SortableBook.objects.get(pk=two_pk).my_order, 18)

    def est_bulkMoveForwardTwoPagesFromLastPage(self):
        one_pk = SortableBook.objects.get(my_order=19).pk
        two_pk = SortableBook.objects.get(my_order=20).pk
        post_data = {'action': ['move_to_forward_page'], 'step': 2, '_selected_action': [one_pk, two_pk]}
        self.client.post(self.bulk_update_url + '?p=2', post_data)
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 19)
        self.assertEqual(SortableBook.objects.get(pk=two_pk).my_order, 20)

    def est_bulkMoveToSpecificPage(self):
        one_pk = SortableBook.objects.get(my_order=1).pk
        two_pk = SortableBook.objects.get(my_order=6).pk
        post_data = {'action': ['move_to_exact_page'], 'page': 3, '_selected_action': [one_pk, two_pk]}
        self.client.post(self.bulk_update_url, post_data)
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 17)
        self.assertEqual(SortableBook.objects.get(pk=two_pk).my_order, 18)

    def est_bulkMoveToSpecificInvalidPage(self):
        one_pk = SortableBook.objects.get(my_order=1).pk
        two_pk = SortableBook.objects.get(my_order=6).pk
        post_data = {'action': ['move_to_exact_page'], 'page': 10, '_selected_action': [one_pk, two_pk]}
        self.client.post(self.bulk_update_url, post_data)
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 1)
        self.assertEqual(SortableBook.objects.get(pk=two_pk).my_order, 6)

    def est_bulkMoveTooManyToLastPage(self):
        """
        if last page contains less items that are moved to it
        """
        one_pk = SortableBook.objects.get(my_order=1).pk
        two_pk = SortableBook.objects.get(my_order=2).pk
        three_pk = SortableBook.objects.get(my_order=3).pk
        four_pk = SortableBook.objects.get(my_order=4).pk
        five_pk = SortableBook.objects.get(my_order=5).pk
        six_pk = SortableBook.objects.get(my_order=6).pk
        post_data = {
            'action': ['move_to_exact_page'],
            'page': 3,
            '_selected_action': [one_pk, two_pk, three_pk, four_pk, five_pk, six_pk, ]
        }
        self.client.post(self.bulk_update_url, post_data)
        # assuming one could start at 17 is wrong
        # maybe even renaming the action to "move to end of list?"
        self.assertEqual(SortableBook.objects.get(pk=one_pk).my_order, 15)
        self.assertEqual(SortableBook.objects.get(pk=two_pk).my_order, 16)
        self.assertEqual(SortableBook.objects.get(pk=three_pk).my_order, 17)
        self.assertEqual(SortableBook.objects.get(pk=four_pk).my_order, 18)
        self.assertEqual(SortableBook.objects.get(pk=five_pk).my_order, 19)
        self.assertEqual(SortableBook.objects.get(pk=six_pk).my_order, 20)
