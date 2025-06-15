from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pygame
import pytest

from flatland.actions.actions import LimbControlMixin, MovementMixin, SpeechMixin
from flatland.consts import Direction
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
