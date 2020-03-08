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
 
## get child to eat more
* get_child_to_eat_more
  - action_get_child_to_eat_more
  - utter_more_information
* affirm
  - action_get_child_to_eat_more
  - utter_more_information 
 
## get child to eat more - no more info
* get_child_to_eat_more
  - action_get_child_to_eat_more
  - utter_more_information
* deny
  - action_chat_restart
  
## what to feed sick child
* what_to_feed_sick_child
  - action_what_to_feed_sick_child
  - utter_more_information
* affirm
  - action_what_to_feed_sick_child
  - utter_more_information 
 
## what to feed sick child - no more info
* what_to_feed_sick_child
  - action_what_to_feed_sick_child
  - utter_more_information
* deny
  - action_chat_restart
 
## how do i know if my child is growing well - there is no more info
* how_to_know_if_child_is_growing_well
  - action_how_to_know_if_child_is_growing_well
  - action_chat_restart
  
## what to feed sick child
* feeding_child_for_growth
  - action_feeding_child_for_growth
  - utter_more_information
* affirm
  - action_feeding_child_for_growth
  - utter_more_information 
 
## what to feed sick child - no more info
* feeding_child_for_growth
  - action_feeding_child_for_growth
  - utter_more_information
* deny
  - action_chat_restart
  
## child development - give response based on age
* health_information{"health": ["child_development"]}
    - health_diagnostic_info_form
    - form{"name": "health_diagnostic_info_form"}
    - slot{"health": ["child_development"]}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_general_health
    - utter_more_information
* affirm
    - action_general_health
    - utter_more_information