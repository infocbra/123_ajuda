from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction



class ActionPegarNome(Action):
    def name(self) -> Text:
        return "action_pegar_nome"
    
    def run(self, dispatcher, tracker, domain):
        name = tracker.latest_message['text']
        mensagem = f"{name}, você sabia que a pandemia alterou de modo significativo a vida dos brasileiros. "\
        "De acordo com  a pesquisa 'Saúde mental em tempos de pandemia', realizada pela Fiocruz em parceria com a UFMG e a UFJF,"\
        "cerca de 40% dos brasileiros apresentaram sintomas de ansiedade e depressão durante a pandemia? E foi por"\
        "isso que nasci para ajudar profissionais de saúde a encontrarem atendimento e apoio emocional."
        dispatcher.utter_message(text=mensagem)
        return []
        

class ActionAskEstado(Action):
    def name(self) -> Text:
        return "utter_ask_estado"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_ask_estado")

        return []


class ActionAskCidade(Action):
    def name(self) -> Text:
        return "utter_ask_cidade"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_ask_cidade")

        return []


class ActionAskBairro(Action):
    def name(self) -> Text:
        return "utter_ask_bairro"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_ask_bairro")

        return []


class ActionEnviarEndereco(Action):
    def name(self) -> Text:
        return "action_enviar_endereco"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        estado = tracker.get_slot("estado")
        cidade = tracker.get_slot("cidade")
        bairro = tracker.get_slot("bairro")

        if estado and cidade and bairro:
            mensagem = "Endereço confirmado. Estado: {0}, Cidade: {1}, Bairro: {2}".format(estado, cidade, bairro)
            dispatcher.utter_message(text=mensagem)
        else:
            dispatcher.utter_message(template="utter_ask_missing_slot", slot_to_ask=tracker.get_slot_to_fill())

        return []

class ActionNotAllSlotsFilled(Action):
    def name(self) -> Text:
        return "action_not_all_slots_filled"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots_to_ask = []

        if tracker.slots.get("estado") is None:
            slots_to_ask.append("estado")

        if tracker.slots.get("cidade") is None:
            slots_to_ask.append("cidade")

        if tracker.slots.get("bairro") is None:
            slots_to_ask.append("bairro")

        if len(slots_to_ask) > 1:
            slots = "{} e {}".format(", ".join(slots_to_ask[:-1]), slots_to_ask[-1])
        else:
            slots = slots_to_ask[0]

        dispatcher.utter_message(template="utter_ask_missing_slot", slot_to_ask=slots)

        return [SlotSet("requested_slot", slots_to_ask[0])]