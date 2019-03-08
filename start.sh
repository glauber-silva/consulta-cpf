fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

sudo docker-compose -f docker-compose-dev.yml up -d --build
sudo docker-compose -f docker-compose-dev.yml up -d
sudo docker-compose -f docker-compose-dev.yml exec users python manage.py recreate_db
sudo docker-compose -f docker-compose-dev.yml exec users python manage.py seed_db
if [ -n "${fails}" ]; then
  echo "Start services failed: ${fails}"
  exit 1
else
  echo "Services running!"
  exit 0
fi