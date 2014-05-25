import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from polls.models import Poll

class PollMethodTests(TestCase):
    def test_was_published_recently_with_future_pub_date(self):
        """
        was_published_recently() should return False for polls if the pub_date is in the future
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=3))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently should return false if poll is older than 1 day
        """
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=3))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        was_published recently should return true if poll was published within the last day
        """
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertTrue(recent_poll.was_published_recently())

def create_poll(question, days):
    """
    factory to create a poll with the given question and the pub_date with given number of 'days' offset to now
    """
    return Poll.objects.create(question=question,
        pub_date=timezone.now() + datetime.timedelta(days=days))

class PollViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        """
        Display the appropriate message when no polls exist
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Polls available right now.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_past_poll(self):
        """
        Polls published in the past should show up
        """
        create_poll(question="past poll", days=-3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: past poll>']
        )

    def test_index_view_with_future_poll(self):
        """
        Polls with pub_at dates in the future should not show up
        """
        create_poll(question="future poll", days=+3)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No Polls available right now.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_futre_and_past_poll(self):
        """
        Only the past poll should show up
        """
        create_poll(question="Past poll", days=-3)
        create_poll(question="Future poll", days=+3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll>']
        )

    def test_index_view_with_two_past_polls(self):
        """
        Page can show multiple polls
        """
        create_poll(question="Past poll 1", days=-5)
        create_poll(question="Past poll 2", days=-4)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll 2>', '<Poll: Past poll 1>']
        )

