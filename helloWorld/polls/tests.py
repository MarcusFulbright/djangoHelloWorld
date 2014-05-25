import datetime

from django.utils import timezone
from django.test import TestCase

from polls.models import Poll

class PollMethodTests(TestCase):
    def test_was_published_recently_with_future_pub_date(self):
        """
        was_published_recently() should return False for polls if the pub_date is in the future
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=3))
        self.assertEqual(future_poll.was_published_recently(), False)

