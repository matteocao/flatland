from enum import Enum, auto
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, Mock

import pygame
import pytest

from flatland.actions.actions import LimbControlMixin, MovementMixin, SpeechMixin
from flatland.actions.volition import VolitionEngine
from flatland.consts import Direction
from flatland.objects.items_registry import registry
from flatland.world.world import world

if TYPE_CHECKING:
    from flatland.objects.base_objects import GameObject


class SpeechTest(SpeechMixin):
    def __init__(self, phrase: str):
        self.message = phrase
        self.volume = 0.4


def test_speech_message() -> None:
    testphrase = "Hello world!"
    speecher = SpeechTest(testphrase)
    speecher.speak(testphrase)
    assert speecher.speech == testphrase


class DummySound(SpeechMixin):
    def __init__(self):
        self.make_sound = None
        self.volume = 0.4


def test_speech_sound() -> None:
    obj = DummySound()
    obj.make_sound = MagicMock()
    obj.make_sound.play = MagicMock()
    obj.speak("Hello")
    assert obj.speech == "Hello"
    obj.make_sound.play.assert_called_once()


class LimbTest(LimbControlMixin):
    def __init__(self, vel):
        self.speed = vel


def test_limbtest() -> None:
    vel = 0
    while vel < 8:
        obj = LimbTest(vel)
        obj.move_limbs(vel)
        assert obj.speed == vel
        vel += 3


class Player(LimbControlMixin):
    def __init__(self):
        self.x = 1
        self.y = 2
        self.direction = "UP"
        self.actions_per_second = 2
        self.z_level = 0.5
        self.children = []
        self.scheduler = type("Scheduler", (), {"interval": 0.25})()
        self.parent = None


class OtherObject:
    def __init__(self):
        self.is_grabbable = True
        self.render_on_top_of_parent = True
        self.scheduler = type("Scheduler", (), {"interval": 0.25})()
        self.parent = None
        self.x = 0
        self.y = 0
        self.direction = None
        self.actions_per_second = 0
        self.z_level = 0.0


def test_grab_obj():
    self_obj = Player()
    other = OtherObject()
    self_obj.grab(other)
    assert other in self_obj.children
    assert other.parent == self_obj
    assert other.x == self_obj.x
    assert other.y == self_obj.y
    assert other.direction == self_obj.direction
    assert other.actions_per_second == self_obj.actions_per_second
    assert other.scheduler.interval == self_obj.scheduler.interval
    assert other.z_level == self_obj.z_level + 1.0


def test_push():
    player = Player()

    class Other:
        def __init__(self):
            self.inertia = 0
            self.direction = None

    other = Other()
    player.push(other)
    assert other.inertia == 2
    assert other.direction == player.direction


class DummyPlayer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = Direction.UP
        self.is_accepting_keys = False
        self.cast_magic_called = False
        self.keys = {
            key: False
            for key in [
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_LEFT,
                pygame.K_RIGHT,
                pygame.K_e,
                pygame.K_q,
                pygame.K_SPACE,
            ]
        }
        self.keys[pygame.K_SPACE] = True

        self.internal_state = self.InternalState()
        self.volition = VolitionEngine(owner=self)

    def get_pressed_keys(self):
        return self.keys

    def cast_magic(self, game):
        self.cast_magic_called = True

    class InternalState:
        def __init__(self):
            self.time_history = []

        def latest_perception(self):
            return []


class DummyGame:
    pass


def test_volition_prepare():
    obj = DummyPlayer()
    game = DummyGame()
    obj.volition.prepare(game)
    assert len(obj.volition.list_of_actions) == 1
    func, kwargs = obj.volition.list_of_actions[0]
    assert func == obj.cast_magic
    assert kwargs == {"game": game}
    assert obj.is_accepting_keys is True
    assert obj.keys is None
