"""
Copyright (c) 2018, INRIA
Copyright (c) 2018, University of Lille
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import logging
import re
from functools import reduce

from powerapi.actor import Actor, SocketInterface
from powerapi.formula import FormulaActor, FormulaState, FormulaPoisonPillMessageHandler
from powerapi.handler import PoisonPillMessageHandler
from powerapi.message import PoisonPillMessage
from powerapi.report import HWPCReport
from rapl_formula.rapl_handlers import RAPLHandler


class RAPLFormulaState(FormulaState):
    """
    RAPLFormulaState
    """
    def __init__(self, actor, pushers, formula_id):
        """
        Initialize a new RAPLFormula actor state.
        :param actor: Actor linked to the state
        :param pushers: Pushers available for the actor
        :param formula_id: Formula id
        """
        super().__init__(actor, pushers)
        self.formula_id = formula_id


class RAPLFormulaActor(FormulaActor):
    """
    A formula to handle RAPL events.
    """

    def __init__(self, name, pusher_actors,
                 level_logger=logging.WARNING, timeout=None):
        """
        :param str name: Actor name
        :param powerapi.PusherActor pusher_actors: Pusher actors whom send results
        :param int level_logger: Define logger level
        :param bool timeout: Time in millisecond to wait for a message before called timeout_handler
        """
        FormulaActor.__init__(self, name, pusher_actors, level_logger, timeout)

        formula_id = reduce(lambda acc, x: acc + (re.search(r'^\(? ?\'(.*)\'\)?', x).group(1),), name.split(','), ())

        #: (powerapi.State): Basic state of the Formula.
        self.state = RAPLFormulaState(self, pusher_actors, formula_id)

    def setup(self):
        """
        Setup the RAPL formula.
        """
        FormulaActor.setup(self)
        self.add_handler(PoisonPillMessage, FormulaPoisonPillMessageHandler(self.state))
        self.add_handler(HWPCReport, RAPLHandler(self.state))
