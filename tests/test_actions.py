import os
import pygame
import pytest
from unittest.mock import MagicMock
from flatland.actions.actions import MovementMixin, SpeechMixin, LimbControlMixin
from flatland.consts import Direction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flatland.objects.base_objects import GameObject

os.environ["SDL_VIDEODRIVER"] = "dummy"  # Use a headless display

class Movement(MovementMixin):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = None

@pytest.mark.parametrize(
    "initial_x, initial_y, direction, expected_x, expected_y",
    [
        (0, 0, Direction.UP, 0, -1),
        (0, 0, Direction.DOWN, 0, 1),
        (0, 0, Direction.LEFT, -1, 0),
        (0, 0, Direction.RIGHT, 1, 0),
    ]
)

def test_movements(initial_x, initial_y, direction, expected_x, expected_y):
    mover = Movement(initial_x, initial_y)
    mover.move(direction)
    assert mover.x == expected_x
    assert mover.y == expected_y
    assert mover.direction == direction

class SpeechTest(SpeechMixin):
    def __init__(self, phrase):
        self.message = phrase

def test_speech_message():
    testphrase = "Hello world!"
    speecher = SpeechTest (testphrase)
    speecher.speak(testphrase)
    assert speecher.speech == testphrase

def test_speech_sound():
    class Dummy(SpeechMixin):
        pass

    obj = Dummy()

    # No make sound test
    obj.speak()
    assert not hasattr(obj, "speech")

    # With make sound
    obj.make_sound = MagicMock()
    obj.make_sound.play = MagicMock()
    obj.speak("Hello")

    assert obj.speech == "Hello"
    obj.make_sound.play.assert_called_once()

class LimbTest(LimbControlMixin):
    def __init__(self, vel):
        self.speed = vel

def test_limbtest():
    vel = 0
    while (vel < 8):
        obj = LimbTest(vel)
        obj.move_limbs(vel)
        assert obj.speed == vel
        vel += 3
