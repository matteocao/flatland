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

def test_move_up():
    mover = Movement (0, 0)
    mover.move(Direction.UP)
    assert mover.x == 0
    assert mover.y == -1
    assert mover.direction == Direction.UP

def test_move_down():
    mover = Movement (0, 0)
    mover.move(Direction.DOWN)
    assert mover.x == 0
    assert mover.y == 1
    assert mover.direction == Direction.DOWN

def test_move_left():
    mover = Movement (0, 0)
    mover.move(Direction.LEFT)
    assert mover.x == -1
    assert mover.y == 0
    assert mover.direction == Direction.LEFT

def test_move_right():
    mover = Movement (0, 0)
    mover.move(Direction.RIGHT)
    assert mover.x == +1
    assert mover.y == 0
    assert mover.direction == Direction.RIGHT

class SpeechTest(SpeechMixin):
    def __init__(self, phrase):
        self.message = phrase

def test_speech_message():
    TestPhrase = "Hello world!"
    speecher = SpeechTest (TestPhrase)
    speecher.speak(TestPhrase)
    assert speecher.speech == TestPhrase

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
