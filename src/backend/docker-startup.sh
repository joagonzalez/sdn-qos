cd /app/

./wait-for-it.sh asterisk:8088 -s -t 0
./wait-for-it.sh ryu:8080 -s  -t 0

sleep 5

python run.py
