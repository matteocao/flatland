# Flatland

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

# Run the game
python3 -m flatland.main

# Run tests
make test
```
