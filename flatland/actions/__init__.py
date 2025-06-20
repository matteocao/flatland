"""
The actions submodule described all the actions an object can make: from moving, to pushing to casting.
The actions follow the same mechanism as interactions.

Roughly, these are the steps:
1. The action is triggered, either by AI or by the user.
2. The action callable is stored in a list during the prepare phase by the Volition
3. The actions are executed in the update phase


Note that the prepare phase follows this chain: ``Level -> GameObject -> VolitionEngine``.

So, the volition engine is like the scheduler for Interactions: it takes care of storing and running the requested actions.
Actions run after the interactions.
"""

from . import actions, volition
