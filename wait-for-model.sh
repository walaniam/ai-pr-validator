#!/bin/sh
model=$OLLAMA_MODEL
echo "Waiting for model: ${model}..."
while [ ! -f /root/.ollama/models/"$model" ]; do
  sleep 2
done
echo "Model found, starting server."
ollama serve
