#!/bin/bash

curl -X 'POST' \
  'http://localhost:8000/update_block_period?block_period=2020-09-28' \
  -H 'accept: application/json' \
  -d ''


curl -X 'POST' \
  'http://localhost:8000/save_reposity_data?file_name=test_file.json' \
  -H 'accept: application/json' \
  -d ''


curl -X 'POST' \
  'http://localhost:8000/create_trial_balance?start_date=1980-10-10&end_date=2000-10-10' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Pendos",
  "unique_code": "",
  "type": "LIKE"
}'