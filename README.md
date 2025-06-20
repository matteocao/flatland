# Flatland

[![Python CI](https://github.com/matteocao/flatland/actions/workflows/ci.yml/badge.svg)](https://github.com/matteocao/flatland/actions/workflows/ci.yml)

A 2D tile-based role-playing game built with `pygame` and powered by AI-controlled entities.

## Features

- Object-oriented entity system with animated/inanimate NPCs
- Registry-based extensibility for new game objects
- Interaction Moderator for entity collision and effects
- Modular tile-based map system
- Simple LLM stub simulating character memory and decisions
- Unit tests included with pytest
- Ready for CI/CD via GitHub Actions

## Development

```bash
# Install dependencies
make install

# Run the game in single player
make run

# Run tests
make test
```

### Multiplayer

To run the game in multiplayer, simply do:

```
# on the server
make server

# on each client
python3 -m flatland.multiplayer --ip x.x.x.x --port xxxxx

```

## Documentation

You can find the online documentation [here](https://matteocao.github.io/flatland/flatland.html).

## Asset resources

I would like to signal this beautiful free website: https://opengameart.org/. It contains a lot of beautiful and well done 2D sprites that are perfect for our game.
