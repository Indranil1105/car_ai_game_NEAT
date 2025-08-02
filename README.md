# 🧠 NEAT Car Racing AI 🚗

A self-learning car driving agent built using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. This project evolves a neural network from scratch to drive a car and dodge obstacles without any labeled data or pre-training — purely through trial, error, and evolution.

## 📂 Project Structure

car_race_AI/

├── assets/

│ ├── player_car.png

│ ├── enemy_car.png

│ └── track_bg.png

├── config-feedforward.txt # NEAT configuration

├── car_game.py # Human-playable version

├── car_game_ai.py # NEAT AI train & test mode

├── best_genome.pkl # Saved best AI brain (after training)

└── README.md

## 🚀 What This Project Does

This project simulates a 4-lane car racing game, where:

The player/AI must switch lanes to avoid crashing into enemy cars.
A neural network evolves using NEAT to learn survival strategies over generations.
Trained AI can consistently achieve scores above 500+, learning lane switching, reaction timing, and avoidance behavior.

## 🧠 Tech Stack

Component	Tech Used
Game Engine	Python + Pygame
AI Framework	NEAT-Python
Model Storage	Pickle
Visuals (WIP)	Matplotlib (fitness graph)
Inputs to Network	Lane position, distances to enemies, speed

## 📌 Features

✅ Simple and modular OOP-based code
✅ Train your own AI or test the saved one
✅ Dynamic enemy car spawning & difficulty scaling
✅ Support for saving the best genome
✅ Input features engineered for real-time decisions
✅ 100% offline — no datasets required

## 📥 Installation

git clone https://github.com/yourusername/neat-car-racing-ai.git
cd neat-car-racing-ai

pip install pygame neat-python

## 🎮 How to Play

➤ Human Mode:
Play manually using arrow keys.


python car_game.py
Move left/right with arrow keys

Try to survive as long as possible

## 🧪 How to Train the AI

Make sure RUN_MODE is set to 'train' in car_game_ai.py
python car_game_ai.py
This will:

Evolve 100+ genomes per generation

Save the best genome as best_genome.pkl once fitness threshold is met

## 🤖 How to Test the Trained AI bash

Make sure RUN_MODE is set to 'test' in car_game_ai.py
python car_game_ai.py
Watch the saved AI take full control of the car and dodge cars with precision!

## 🧬 What NEAT Does Internally

NEAT evolves neural networks by:

Starting with minimal networks (input → output)

Assigning fitness based on game survival

Performing selection, crossover, and mutation

Gradually increasing complexity and performance over generations

No labeled data, no backpropagation, no gradient descent — just raw evolution.

🎓 Credits:  Inspired by the Flappy Bird AI NEAT Tutorial by Tech With Tim — a huge thanks for that amazing starter.

