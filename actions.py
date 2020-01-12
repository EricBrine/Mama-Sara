from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    Restarted,
    ConversationPaused,
    EventType,
)
from utils import word_to_digits
import json


# Currently just restarts conversation when unsure of input.
# Will need to provide more robust fallback response.
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:

        # Fallback caused by TwoStageFallbackPolicy
        if (
            len(tracker.events) >= 4
            and tracker.events[-4].get("name") == "action_default_ask_affirmation"
        ):

            dispatcher.utter_template("utter_restart_with_button", tracker)

            return [Restarted()]

        # Fallback caused by Core
        else:
            dispatcher.utter_template("utter_default", tracker)
            return [UserUtteranceReverted()]


# Responds with nutrition info based on age of child derived from "months_old" entity.
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


# Responds with treatment info based on diagnostic info for ill child.
class ActionSickChild(Action):
    def name(self):
        return "action_sick_child"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        # get age from slot and convert "eight" to 8
        months_old = int(word_to_digits(tracker.get_slot('months_old')))
        print(months_old)

        days_sick = int(word_to_digits(tracker.get_slot('days_sick')))
        print(days_sick)

        dispatcher.utter_message(
            text='treat your child'
        )
        return [Restarted()]


def read_responses():
    with open("responses/responses.json", 'r') as f:
        responses = json.load(f)
    return responses


class NutritionDiagnosticInfoForm(FormAction):
    """Form for resolving which response to return for a question about nutrition information"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "nutrition_diagnostic_info_form"

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
        dispatcher.utter_message(text="Thank you")
        return []


class IllnessDiagnosticInfoForm(FormAction):
    """Form for resolving which response to return for a question about nutrition information"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "illness_diagnostic_info_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
            "months_old",
            "days_sick",
            "headache",
            "sore_throat",
            "nausea"
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "months_old": self.from_entity(entity="months_old"),
            "days_sick": self.from_entity(entity="days_sick"),
            "headache": [
                self.from_entity(entity="headache"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "sore_throat": [
                self.from_entity(entity="sore_throat"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "nausea": [
                self.from_entity(entity="nausea"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
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
        dispatcher.utter_message(text="thank you")
        return []


# Part of two-stage fallback policy. Currently will just restart conversation.
# Working on improving fallback response.
class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import pandas as pd

        # NOT IMPLEMENTED. Working on a means to resolve ambiguous input.
        self.intent_mappings = pd.read_csv("intent_description_mapping.csv")
        self.intent_mappings.fillna("", inplace=True)
        print("action_default_ask_affirmation")

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:

        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        if len(intent_ranking) > 0:
            first_intent_names = intent_ranking[0].get("name", "")
        else:
            dispatcher.utter_message(text="let's restart.")
            dispatcher.utter_message(text="ask me a question.")
            return [Restarted()]

        print("ONE")
        # first_intent_names = [
        #     intent.get("name", "")
        #     for intent in intent_ranking
        #     if intent.get("name", "") != "out_of_scope"
        # ]

        # message_title = "Sorry, I'm not sure I've understood " "you correctly. Do you mean..."
        # print('TWO')
        # print(first_intent_names)
        # response = self.get_top_intent(first_intent_names)
        # dispatcher.utter_message(text=message_title)
        # print(response)
        # dispatcher.utter_message(text=response)

        message_title = "Could you repeat that?"
        dispatcher.utter_message(text=message_title)

        return [Restarted()]

    def get_top_intent(self, intent: Text) -> Text:
        utterance_query = self.intent_mappings.intent == intent

        utterances = self.intent_mappings[utterance_query].name[0]

        return utterances


# Not currently in use.
# Will return the previous action.
def get_last_utter_action(tracker):

    for event in reversed(tracker.events):

        if event.get('name') not in ['action_listen', None, 'utter_ask_continue']:
            last_utter_action = event.get('name')
            # print('found action', last_utter_action)
            return last_utter_action
        else :
            # print(event.get('name'))
            pass

    return 'error! no last action found'
