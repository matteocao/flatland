# conftest.py

import os

import pygame
import pytest


@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    os.environ["SDL_VIDEODRIVER"] = "dummy"  # headless video
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        pygame.mixer.init()
    except pygame.error:
        # fallback: disable sound if mixer init fails (e.g., in CI)
        pygame.mixer = None
