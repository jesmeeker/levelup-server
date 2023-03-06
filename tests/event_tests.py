import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Gamer, Game, Event
from rest_framework.authtoken.models import Token


class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'event']

    def setUp(self):
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/events"

        # Define the request body
        data = {
            "date_of_event": "2023-12-22",
            "start_time": "18:00",
            "location": "Jes's House",
            "game": 1
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["date_of_event"], "2023-12-22")
        self.assertEqual(json_response["start_time"], "18:00")
        self.assertEqual(json_response["location"], "Jes's House")

    def test_get_event(self):
        """
        Ensure we can get an existing event.
        """

        # Seed the database with a event
        event = Event()
        event.date_of_event="2023-12-25"
        event.start_time="09:00"
        event.location="The Moon"
        event.host_id= 1
        event.game_id= 1
        event.save()

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["date_of_event"], "2023-12-25")
        self.assertEqual(json_response["start_time"], "09:00:00")
        self.assertEqual(json_response["location"], "The Moon")

    def test_change_event(self):
        """
        Ensure we can change an existing event.
        """
        event = Event()
        event.date_of_event="2023-12-25"
        event.start_time="09:00"
        event.location="The Moon"
        event.host_id= 1
        event.game_id= 1
        event.save()

        # DEFINE NEW PROPERTIES FOR EVENT
        data = {
            "date_of_event": "2023-12-26",
            "start_time": "10:00:00",
            "location": "The Sun",
            "game": 2
        }

        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET event again to verify changes were made
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["date_of_event"], "2023-12-26")
        self.assertEqual(json_response["start_time"], "10:00:00")
        self.assertEqual(json_response["location"], "The Sun")

    def test_delete_event(self):
        """
        Ensure we can delete an existing event.
        """
        event = Event()
        event.date_of_event="2023-10-25"
        event.start_time="09:00"
        event.location="The Stars"
        event.host_id= 1
        event.game_id= 1
        event.save()

        # DELETE the event you just created
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the event again to verify you get a 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_signup_leave_event(self):
        """
        Ensure we can add/remove an gamer from event attendees using signup and leave custom actions.
        """

        event = Event()
        event.date_of_event="2023-10-25"
        event.start_time="09:00"
        event.location="The Universe"
        event.host_id= 1
        event.event_id= 1
        event.save()

        gamer = 1

        event.attendees.add(gamer)

        # Initiate request and store response
        response = self.client.post(f"/events/{event.id}/signup")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the attendee was added to event
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["message"],"Gamer added")

        # DELETE the gamer sign up you just created
        response = self.client.delete(f"/events/{event.id}/leave")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)