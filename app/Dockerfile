FROM wl_odc_chatbot_env

WORKDIR /usr/src/app

COPY . .
EXPOSE 5000
CMD [ "gunicorn", "--bind", "0.0.0.0:5000","wsgi:app" ]
