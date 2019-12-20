from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from rasa_sdk.events import Restarted
from utils import word_to_digits
import json


class MamaSaraAPI:
    def search(self, info):
        return "mama sara"


class ActionNutritionInformation(Action):
    def name(self):
        return "action_nutrition_information"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        # get age from slot and convert "eight" to 8
        months_old = int(word_to_digits(tracker.get_slot('months_old')))
        print(months_old)
        if months_old < 6:
            return_message = responses["nutrition_information"]['6']
        elif months_old < 9:
            return_message = responses["nutrition_information"]['9']
        elif months_old < 12:
            return_message = responses["nutrition_information"]['12']
        elif months_old < 24:
            return_message = responses["nutrition_information"]['24']

        dispatcher.utter_message(
            text=return_message
        )
        return [Restarted()]


# Ignore this
class ActionSupplyAge(Action):
    def name(self):
        return "action_query_age"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message(text="here's what I found:")
        age_in_months = tracker.get_slot('months_old')

        dispatcher.utter_message(
            text="thanks"
        )
        return []


def read_responses():
    with open("responses/responses.json", 'r') as f:
        responses = json.load(f)
    return responses


class DiagnosticInfoForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "diagnostic_info_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["months_old"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "months_old": self.from_entity(entity="months_old")
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(text="One second")
        return []

