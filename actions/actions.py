import logging
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction

import requests 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher




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
    
class AddressFormValidation(FormValidationAction):
    def name(self) -> Text:
        return "validate_address_form"

    def validate_estado(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(text="Por favor, forneça o estado correto.")
            return {"estado": None}
        return {"estado": slot_value}

    def validate_cidade(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(text="Por favor, forneça a cidade correta.")
            return {"cidade": None}
        return {"cidade": slot_value}

    def validate_bairro(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(text="Por favor, forneça o bairro correto.")
            return {"bairro": None}
        return {"bairro": slot_value}


class ActionFiltrarEndereco(Action):
    def name(self) -> Text:
        return "action_filtrar_endereco"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Recupere as entidades necessárias do tracker
        estado = tracker.get_slot("estado")
        bairro = tracker.get_slot("bairro")

        # Faça a chamada à sua API passando as informações do endereço
        response = requests.get("http://localhost:5000/unidades_de_saude", params={"uf": estado, "bairro": bairro})

        # Analise a resposta da API e obtenha os resultados desejados
        if response.status_code == 200:
            data = response.json()

            if data:
                # Filtrar apenas os 3 primeiros endereços
                resultados_filtrados = data[:3]

                for endereco_filtrado in resultados_filtrados:
                    # Obtém as informações do endereço filtrado
                    nome = endereco_filtrado.get("nome")
                    endereco = endereco_filtrado.get("endereco")
                    bairro = endereco_filtrado.get("bairro")
                    estado = endereco_filtrado.get("estado")

                    # Envie a resposta para o usuário
                    mensagem = f"Unidade de Saude: {nome}\nEndereco: {endereco}\nBairro: {bairro}\nEstado: {estado}"
                    dispatcher.utter_message(text=mensagem)
            else:
                dispatcher.utter_message(text="Nenhum endereço encontrado.")
        else:
            dispatcher.utter_message(text="Erro ao consultar a API de filtragem de endereço.")

        return []

