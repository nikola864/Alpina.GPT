from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Bot
from scenarios.models import Scenario


class BotApiTest(APITestCase):
    def setUp(self):
        self.scenario = Scenario.objects.create(title="Test Scenario")

    def test_create_bot(self):
        data = {
            "name": "Test Bot",
            "description": "My bot",
            "telegram_token": "abc123",
            "scenario_id": self.scenario.id
        }
        response = self.client.post('/api/bots/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bot.objects.count(), 1)