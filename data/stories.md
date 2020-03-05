## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy
  
## introduce mama sara
* greet
  - utter_greet
  - utter_intro

## nutrition_information - Age needs to be asked for
* nutrition_information
    - nutrition_diagnostic_info_form
    - form{"name": "nutrition_diagnostic_info_form"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_nutrition_information
    
## sick
* sick_child
    - illness_diagnostic_info_form
    - form{"name": "illness_diagnostic_info_form"}
    - form{"name": null}
    - action_sick_child
    
* sick_child{"symptom": ["headache", "coughing"]}
    - illness_diagnostic_info_form
    - form{"name": "illness_diagnostic_info_form"}
    - slot{"symptom": ["headache", "coughing"]}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_sick_child

## how often to breastfeed
* how_often_to_breastfeed
  - action_breastfeeding_frequency
  - utter_more_information
* affirm
  - action_breastfeeding_frequency
  - utter_more_information

## how often to breastfeed - no more info
* how_often_to_breastfeed
  - action_breastfeeding_frequency
  - utter_more_information
* deny
  - action_chat_restart
  
## how to keep child healthy
* keep_child_healthy
  - action_keep_child_healthy
  - utter_more_information
* affirm
  - action_keep_child_healthy
  - utter_more_information

## how to keep child healthy - no more info
* keep_child_healthy
  - action_keep_child_healthy
  - utter_more_information
* deny
  - action_chat_restart