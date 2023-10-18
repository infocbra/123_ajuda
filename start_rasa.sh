#!/bin/bash

source venv/bin/activate  # Ative o ambiente virtual do seu projeto Rasa, se você estiver usando um

rasa run -m models --endpoints endpoints.yml --port 5005 --credentials credentials.yml --cors "*" --debug 

 

