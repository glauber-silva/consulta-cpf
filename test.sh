#!/bin/bash


fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

# run unit and integration tests
sudo docker-compose -f docker-compose-dev.yml up -d --build
sudo docker-compose -f docker-compose-dev.yml exec users python manage.py test
inspect $? users
sudo docker-compose -f docker-compose-dev.yml exec users flake8 project
inspect $? users-lint
sudo docker-compose -f docker-compose-dev.yml exec cpf python manage.py test
inspect $? cpf
sudo docker-compose -f docker-compose-dev.yml exec cpf flake8 project
inspect $? cpf-lint
sudo docker-compose -f docker-compose-dev.yml down

# return proper code
if [ -n "${fails}" ]; then
  echo "Tests failed: ${fails}"
  exit 1
else
  echo "Tests passed!"
  exit 0
fi