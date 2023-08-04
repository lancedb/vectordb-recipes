from datasets import load_dataset
from enum import Enum

dataset = load_dataset("CVdatasets/ImageNet15_animals_unbalanced_aug1", split="train")

class Animal(Enum):
    italian_greyhound = 0
    coyote = 1
    beagle = 2
    rottweiler = 3
    hyena = 4
    greater_swiss_mountain_dog = 5
    Triceratops = 6
    french_bulldog = 7
    red_wolf = 8
    egyption_cat = 9
    chihuahua = 10
    irish_terrier = 11
    tiger_cat = 12
    white_wolf = 13
    timber_wolf = 14

print(Animal(dataset[0]['labels']).name)