sudo systemctl daemon-reload
sudo systemctl restart gunicorn
service nginx restart

sudo systemctl status gunicorn
service nginx status


daphne -b 0.0.0.0 -p 8001 ludomission.asgi:application
daphne ludomission.asgi:application

sudo systemctl daemon-reload
sudo systemctl start daphne.service
sudo systemctl status daphne.service
sudo systemctl restart daphne.service


export DJANGO_SETTINGS_MODULE=ludomission.settings