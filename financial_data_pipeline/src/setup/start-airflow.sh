airflow db migrate;
cp /src/config/airflow/airflow.cfg ~/airflow/airflow.cfg
airflow users create \
    --username admin \
    --firstname Palash \
    --lastname Jain \
    --role Admin \
    --email jpalash22@gmail.com \
    --password admin
echo "Airflow User Created";
nohup airflow webserver --port 8085 &
echo "Airflow Webserver Started";
nohup airflow scheduler &
echo "Airflow Setup done";