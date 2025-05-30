# conftest.py

import os
import warnings

import pygame
import pytest


@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    os.environ["SDL_VIDEODRIVER"] = "dummy"  # headless video
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        pygame.mixer.init()
    except pygame.error as e:
        # fallback: disable sound if mixer init fails (e.g., in CI)
        warnings.warn(f"Could not load mixer, {e}")
        pygame.mixer = None
