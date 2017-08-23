#!/usr/bin/env bash


curl -d "email=efimok@gmail.com&phone=+79267933419&text=DaftPunk" http://localhost:8000
curl -d "email=efimok@123.ru&phone=+7 926 793 34 19" http://localhost:8000
curl -d "date=efimok@gmail.com&email=+79267933419" http://localhost:8000
curl -d "date=25-01-1989&email=efimok@gmail.com" http://localhost:8000
