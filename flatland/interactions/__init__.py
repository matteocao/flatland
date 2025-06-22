"""
This submodule is about interactions.
Interactions work like so:
1. You attach a mixin class to the game object.
2. The mixin, during the prepare phase, prepares the interaction callables.
3. These callables are converted to a Command class.
4. The command is executed.

Note that the ``prepare`` phase, which is triggered following this cascade: ``Level -> GameObject -> Scheduler``,
counts the interactions twice: this is why it is important to define stable interactions, i.e. interactions that always converge.

After the interaction mixins, there are also the evolution mixins, whose goal is to bring certain parameters to convergence.
For example, the evolution of the temperature and its decay is governed by an evolutor. Same for inertia and its evolution damped by friction.
"""

from . import command, evolution, interactions, scheduler
