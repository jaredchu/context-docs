"""Controls for mixed native CLI stream events, including the observed failure."""
import unittest
from run_native import responding_models


class NativeStreamTests(unittest.TestCase):
    def test_mixed_messages_retain_model_identity(self):
        events = [
            {'type': 'assistant', 'message': {'model': 'claude-opus-5-5'}},
            {'type': 'system', 'message': 'A tool permission was denied.'},
            {'type': 'assistant', 'message': {'model': 'claude-opus-5-5'}},
            {'type': 'result', 'subtype': 'success'},
            {'type': 'system', 'message': None},
        ]
        self.assertEqual(responding_models(events), ['claude-opus-5-5'])

    def test_missing_model_does_not_invent_confirmation(self):
        self.assertEqual(responding_models([{'message': 'status'}, {'message': {}}]), [])


if __name__ == '__main__':
    unittest.main()
