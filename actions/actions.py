from typing import Any, Text, Dict, List

import arrow 
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker, FormValidationAction, Action

from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict



class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        num1=tracker.get_slot("first_name")
        num2=tracker.get_slot("last_name")
        operand=tracker.get_slot("operand") 
        if operand=="add":
            msg = f"sum {int(num1)+int(num2)}"
        elif operand=="sub":
            msg = f"sub {int(num1)-int(num2)}"
        elif operand=="multi":
            msg = f"multi {int(num1)*int(num2)}"
        elif operand=="divi":
            msg = f"div {int(num1)/int(num2)}"
      
        dispatcher.utter_message(text=msg)
        return{"first_name": None,"last_name": None,"operand":None}
        

class ActionOperation(Action):

    def name(self) -> Text:
        return "add_two"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        num1=next(tracker.get_latest_entity_values("number1"),None)
        num2=next(tracker.get_latest_entity_values("number2"),None)
        operator=next(tracker.get_latest_entity_values("variable"),None)
        if operator=="add" or operator=="addition":
            msg = f"sum {int(num1)+int(num2)}"
        elif operator=="sub" or operator=="subtraction":
            msg = f"sub {int(num1)-int(num2)}"
        elif operator=="multi" or operator=="multiplication":
            msg = f"multi {int(num1)*int(num2)}"
        elif operator=="div" or operator=="division":
            msg = f"div {int(num1)/int(num2)}"
        else:
            msg="invalid operation,try another option pls"
            
        dispatcher.utter_message(text=msg)
        

def clean_name(name):
    return "".join([c for c in name if c.isnumeric()])

class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        # If the name is super short, it might be wrong.
        name = clean_name(slot_value)
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"first_name": None}
        return {"first_name": name}

    def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `last_name` value."""

        # If the name is super short, it might be wrong.
        name = clean_name(slot_value)
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"last_name": None}
        return {"last_name": name}

class ResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("operand", None),SlotSet("first_name", None),SlotSet("last_name", None)]