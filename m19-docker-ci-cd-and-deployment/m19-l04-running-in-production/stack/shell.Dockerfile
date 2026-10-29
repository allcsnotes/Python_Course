FROM m19l04-allcs:1
CMD gunicorn app.main:app -c gunicorn.conf.py
