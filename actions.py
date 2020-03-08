from rasa_actions import *
from rasa_forms import *

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