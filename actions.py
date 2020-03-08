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

        symptoms = tracker.get_slot('symptom')
        print(symptoms)
        if type(symptoms) == list:
            return_message = ""
            for symptom in symptoms:
                return_message += responses["illness_information"][symptom] + " "
        else:
            return_message = responses["illness_information"][symptoms]

        dispatcher.utter_message(
            text=return_message
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
            "symptom"
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
            "symptom": self.from_entity(entity="symptom")
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


# Gives info on breastfeeding frequency
class ActionBreastfeedingFrequency(Action):
    def name(self):
        return "action_breastfeeding_frequency"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        curr_iteration = tracker.get_slot("iteration_num")

        if int(curr_iteration) >= 4:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        return_message = responses["breastfeeding_frequency"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )
        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]


# Gives info on breastfeeding frequency
class ActionKeepChildHealthy(Action):
    def name(self):
        return "action_keep_child_healthy"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        curr_iteration = tracker.get_slot("iteration_num")

        if int(curr_iteration) >= 6:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        return_message = responses["keep_child_healthy"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )
        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]


# Gives info on breastfeeding frequency
class ActionGetChildToEatMore(Action):
    def name(self):
        return "action_get_child_to_eat_more"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        curr_iteration = tracker.get_slot("iteration_num")

        if int(curr_iteration) >= 4:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        return_message = responses["get_child_to_eat_more"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )
        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]


# Gives info on breastfeeding frequency
class ActionWhatToFeedSickChild(Action):
    def name(self):
        return "action_what_to_feed_sick_child"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        curr_iteration = tracker.get_slot("iteration_num")

        if int(curr_iteration) >= 2:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        return_message = responses["what_to_feed_sick_child"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )
        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]


# Gives info on breastfeeding frequency
class ActionHowToKnowIfChildIsGrowingWell(Action):
    def name(self):
        return "action_how_to_know_if_child_is_growing_well"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        return_message = responses["how_to_know_if_child_is_growing_well"][0]

        dispatcher.utter_message(
            text=return_message
        )
        return [Restarted()]


# Gives info on breastfeeding frequency
class ActionFeedingForGrowth(Action):
    def name(self):
        return "action_feeding_child_for_growth"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        curr_iteration = tracker.get_slot("iteration_num")

        if int(curr_iteration) >= 4:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        return_message = responses["feeding_child_for_growth"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )
        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]


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

        fallback_stage = tracker.get_slot("fallback")

        if int(fallback_stage) >= 1:
            dispatcher.utter_message(text="Let's try again from the start.")
            return [Restarted()]

        dispatcher.utter_message(text="Could you please repeat that?")
        return [UserUtteranceReverted(), SlotSet("fallback", str(int(fallback_stage) + 1))]


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


class ActionRestarted(Action):
    """ This is for restarting the chat"""

    def name(self):
        return "action_chat_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]

class ActionGeneralHealth(Action):
    def name(self):
        return "action_general_health"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        months_old = int(word_to_digits(tracker.get_slot('months_old')))
        curr_iteration = tracker.get_slot("iteration_num")
        health = tracker.get_slot('health')

        if int(curr_iteration) > 2:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        if months_old < 15:
            return_message = responses["health_information"][health]["12"][int(curr_iteration)]
        else:
            return_message = responses["health_information"][health]["15"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )

        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]


class HealthDiagnosticInfoForm(FormAction):
    """Form for resolving which response to return for a question about nutrition information"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "health_diagnostic_info_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
            "months_old",
            "health"
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "months_old": self.from_entity(entity="months_old"),
            "health": self.from_entity(entity="health")
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