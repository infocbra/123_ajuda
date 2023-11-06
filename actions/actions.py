import logging
from sanic import Sanic, Request, response
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction

import requests 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

app = Sanic("actions")


@app.route("/webhooks/rest/webhook", methods=["POST"])
async def webhook(request: Request):
    data = request.json
    tracker = Tracker(
        sender_id=data["sender"],
        slots=data["slots"],
        latest_message=data["latest_message"],
        events=data["events"],
        paused=data["paused"],
        followup_action=data["followup_action"],
        active_form=data["active_form"],
        latest_input_channel=data["latest_input_channel"],
        latest_action_name=data["latest_action_name"]
    )
    dispatcher = CollectingDispatcher.from_tracker(tracker)
    
    # Chame suas ações personalizadas com o tracker e dispatcher
    # Exemplo: dispatcher.utter_message(text="Olá, mundo!")
    
    responses = dispatcher.messages
    return response.json(responses)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055)


class ActionPegarNome(Action):
    def name(self) -> Text:
        return "action_pegar_nome"
    
    def validate_nome(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(text="Por favor, qual seu nome?")
            return {"nome": None}
        return {"nome": slot_value}
    
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
        # if slot_value.lower() not in ["df", "distrito federal"]:
        #     dispatcher.utter_message(text="Obrigado por entrar em contato com o 123 Ajuda. Atualmente, nossos serviços estão disponíveis apenas para residentes no Distrito Federal.")
        #     return {"estado": None}
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


class SetEstadoDFAction(Action):
    def name(self) -> str:
        return "action_set_estado_df"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, ddomain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("estado", "DF")]

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
        cidade = tracker.get_slot("cidade")
        latest_intent = tracker.latest_message["intent"]["name"]
        is_full_time = latest_intent == "emergencia"

        # Defina isFullTime como True se a intenção for "emergencia", caso contrário, False
        is_full_time_value = 1 if is_full_time else 0

        print(f"Estado: {estado}")
        print(f"Cidade: {cidade}")
        print(f"is_full_time_value: {is_full_time_value}")
        # Faça a chamada à sua API passando as informações do endereço
        url = f"https://123ajuda.tech/api/unidades_de_saude?abrangencia={cidade}&uf={estado}&isFulltime={is_full_time_value}"
        url_localhost = "http://127.0.0.1:5000/api/unidades_de_saude"
        params = {"abragencia": cidade, "uf": estado, }

        try:
            response = requests.get(url)

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
                        uf = endereco_filtrado.get("uf")
                        abrangencia = endereco_filtrado.get("abrangencia")
                        
                        horario_atendimento = "Horário Integral" if is_full_time_value else "Horário Parcial"


                        # Envie a resposta para o usuário
                        mensagem = f"\nAbrangencia: {abrangencia}\nHorário de Atendimento: {horario_atendimento}\nUnidade de Saude: {nome}\nEndereço: {endereco}\nBairro: {bairro}\nEstado: {uf}"
                        dispatcher.utter_message(text=mensagem)
                else:
                    dispatcher.utter_message(text="Nenhum endereço encontrado.")
            else:
                dispatcher.utter_message(text=f"Erro ao consultar a API de filtragem de endereço. Código de status: {response.status_code}")

        except requests.RequestException as e:
            dispatcher.utter_message(text=f"Erro ao consultar a API de filtragem de endereço: {e}")

        return []


