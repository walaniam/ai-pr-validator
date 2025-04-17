#!/bin/bash

echo "Starting Ollama server..."
ollama serve &  # Run in background

echo "Waiting 10s before proceed"
sleep 10         # Give it time to start

model=$OLLAMA_MODEL

ollama list | grep -q "$model"
if [ $? -ne 0 ]; then
  echo "Model $model not found. Pulling..."
  ollama pull "$model"
else
  echo "Model $model already exists. Skipping pull."
fi

wait