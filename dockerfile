FROM python:3.12.7

WORKDIR /SPART

COPY requirements.txt /SPART/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /SPART/

# Coleta arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expor a porta 8000
EXPOSE 8000

CMD ["gunicorn", "Spart.wsgi:application", "--bind", "0.0.0.0:8000"]
