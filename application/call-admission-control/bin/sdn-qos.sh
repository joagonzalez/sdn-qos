#!/bin/bash

# esto tiene que ser un script que primero inicia backend y dps frontend cuando inicio backend
python app/backend/run.py

npm start --prefix app/frontend
