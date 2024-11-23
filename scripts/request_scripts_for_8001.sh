#!/bin/bash

curl -X 'GET' \
  'http://localhost:8001/report_formats' \
  -H 'accept: application/json'

curl -X 'GET' \
  'http://localhost:8001/report/unit/JSON' \
  -H 'accept: application/json'

curl -X 'GET' \
  'http://localhost:8001/get_block_period' \
  -H 'accept: application/json'

curl -X 'POST' \
  'http://localhost:8001/filter/unit' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Грамм",
  "unique_code": "",
  "type": "LIKE"
}'