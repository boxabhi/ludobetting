sudo systemctl daemon-reload
sudo systemctl restart gunicorn
service nginx restart

sudo systemctl status gunicorn
service nginx status



daphne ludomission.asgi:application

systemctl daemon-reload
systemctl start daphne.service
systemctl status daphne.service


export DJANGO_SETTINGS_MODULE=ludomission.settings