#!/bin/bash

model=$OLLAMA_MODEL
count=$(ollama ls |grep "$model" |wc -l)
echo "Running models count: $count"

if [ "$count" -ge 1 ]; then
  exit 0
else
  exit 1
fi