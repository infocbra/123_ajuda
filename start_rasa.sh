#!/bin/bash
source /home/ec2-user/projeto_123_ajuda/123_ajuda_bot/venv/bin/activate
cd /home/ec2-user/projeto_123_ajuda/123_ajuda_bot
echo "Iniciando Rasa..."
rasa run -m models --enable-api --endpoints endpoints.yml
echo "Rasa iniciado com sucesso!"
