#!/bin/bash

# esto tiene que ser un script que primero inicia backend y dps frontend cuando inicio backend
python src/backend/run.py

npm start --prefix src/frontend
