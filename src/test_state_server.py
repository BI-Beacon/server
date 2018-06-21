import unittest
from state_server import StateServer


class TestStateServerGetBehaviour(unittest.TestCase):

    def test_get_returns_stored_state(self):
        db = {'hej': {'color': '#ff00ff'}}
        state_server = StateServer(db)
        self.assertEqual({'color': '#ff00ff'}, state_server['hej'])
