from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pygame
import pytest

from flatland.actions.actions import LimbControlMixin, MovementMixin, SpeechMixin
from flatland.consts import Direction
from flatland.game import Game
from flatland.objects.base_objects import GameObject
from flatland.world.world import world


class DummySound(SpeechMixin, GameObject):
    def __init__(self):
        super().__init__(0, 0, "blabla", 5)
        self.make_sound = None
        self.volume = 0.4


def test_speech_message(display) -> None:
    testphrase = "Hello world!"
    speecher = DummySound()
    game = Game(world, display)
    speecher.speak(game, testphrase)
    assert speecher.speech == testphrase


def test_speech_sound(display) -> None:
    obj = DummySound()
    game = Game(world, display)
    obj.make_sound = MagicMock()
    obj.make_sound.play = MagicMock()
    obj.speak(game, "Hello")
    assert obj.speech == "Hello"
    obj.make_sound.play.assert_called_once()
