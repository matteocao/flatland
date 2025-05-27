import pytest
from objects import Player, Stone, Animal
from world import GameWorld
import pygame

@pytest.fixture
def dummy_screen():
    pygame.init()
    return pygame.display.set_mode((320, 320))

def test_player_creation():
    p = Player(x=1, y=2)
    assert p.x == 1 and p.y == 2

def test_stone_push(dummy_screen):
    world = GameWorld(dummy_screen)
    player = Player(1, 1)
    stone = Stone(2, 1)
    world.objects = [player, stone]

    keys = {pygame.K_RIGHT: True}
    for k in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT]:
        keys[k] = False

    player.handle_input(keys, world.width, world.height, world.objects)
    assert stone.x == 3

def test_animal_vision_chase():
    animal = Animal(x=1, y=1)
    player = Player(x=3, y=1)
    world = type("MockWorld", (), {"objects": [animal, player], "width": 10, "height": 10})
    animal.update(world)
    assert animal.x == 2

def test_npc_brain():
    from llm_stub import LLMNPCBrain
    brain = LLMNPCBrain("Bob", "friendly")
    for event in ["met player", "saw stone", "heard noise", "saw animal", "walked north", "talked to player"]:
        brain.observe(event)
    assert brain.decide_action() == "reflect"
    assert "Bob" in brain.speak()