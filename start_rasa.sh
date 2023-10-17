#!/bin/bash

source venv/bin/activate  # Ative o ambiente virtual do seu projeto Rasa, se você estiver usando um

rasa run -m models --enable-api --endpoints endpoints.yml
