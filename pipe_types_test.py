"""
to test module pipe_types , we make two scenarios for each rule type,
1) makes function "needs_action" return false and we name it "..._false{number_of_instance}"
2) makes function "needs_action" return true and we name it "..._true{number_of_instance}"
"""

import unittest
import pipe_types


class MyTestCase(unittest.TestCase):
    def test_any(self):
        instance_any_false1 = pipe_types.Any({})
        instance_any_true1 = pipe_types.Any({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"})
        self.assertFalse(instance_any_false1.needs_action())
        self.assertTrue(instance_any_true1.needs_action())

    def test_frequency(self):
        instance_freq_false1 = pipe_types.Frequency({}, 10, action_on_equals=False)
        instance_freq_false2 = pipe_types.Frequency({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, 10, action_on_equals=False)
        instance_freq_false3 = pipe_types.Frequency({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, 6, action_on_equals=False)
        instance_freq_true1 = pipe_types.Frequency({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, 1, action_on_equals=True)
        instance_freq_true2 = pipe_types.Frequency({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, 6, action_on_equals=True)

        self.assertTrue(instance_freq_true1.needs_action())
        self.assertTrue(instance_freq_true2.needs_action())
        self.assertFalse(instance_freq_false1.needs_action())
        self.assertFalse(instance_freq_false2.needs_action())
        self.assertFalse(instance_freq_false3.needs_action())

    def test_flatline(self):
        instance_flat_true1 = pipe_types.Flatline({}, 10, action_on_equals=False)
        instance_flat_true2 = pipe_types.Flatline({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, 10, action_on_equals=False)
        instance_flat_true3 = pipe_types.Flatline({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, 6, action_on_equals=True)
        instance_flat_false1 = pipe_types.Flatline({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, 6, action_on_equals=False)
        instance_flat_false2 = pipe_types.Flatline({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, 1, action_on_equals=True)

        self.assertTrue(instance_flat_true1.needs_action())
        self.assertTrue(instance_flat_true2.needs_action())
        self.assertTrue(instance_flat_true3.needs_action())
        self.assertFalse(instance_flat_false1.needs_action())
        self.assertFalse(instance_flat_false2.needs_action())

    def test_range(self):
        instance_range_false1 = pipe_types.Range({}, min_threshold=10, max_threshold=20, action_on_equals=False)
        instance_range_false2 = pipe_types.Range({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, min_threshold=10, max_threshold=20, action_on_equals=False)
        instance_range_false3 = pipe_types.Range({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, min_threshold=10, max_threshold=20, action_on_equals=True)
        instance_range_true1 = pipe_types.Range({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, min_threshold=1, max_threshold=20, action_on_equals=False)
        instance_range_true2 = pipe_types.Range({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, min_threshold=6, max_threshold=20, action_on_equals=True)
        instance_range_true3 = pipe_types.Range({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, min_threshold=1, max_threshold=6, action_on_equals=True)
        instance_range_false4 = pipe_types.Range({"k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4", "k5": "v5", "k6": "v6"}, min_threshold=1, max_threshold=6, action_on_equals=False)

        self.assertTrue(instance_range_true1.needs_action())
        self.assertTrue(instance_range_true2.needs_action())
        self.assertTrue(instance_range_true3.needs_action())
        self.assertFalse(instance_range_false1.needs_action())
        self.assertFalse(instance_range_false2.needs_action())
        self.assertFalse(instance_range_false3.needs_action())
        self.assertFalse(instance_range_false4.needs_action())

    def test_historical_range(self):
        instance_hrange_false1 = pipe_types.HistoricalRange({}, {}, 2, compare_type="up", action_on_equals=False)
        instance_hrange_false2 = pipe_types.HistoricalRange({}, {}, 2, compare_type="down", action_on_equals=False)
        instance_hrange_false3 = pipe_types.HistoricalRange({}, {}, 2, compare_type="both", action_on_equals=False)
        instance_hrange_false4 = pipe_types.HistoricalRange({"k1": "v1", "k2": "v2"}, {}, 3, compare_type="up", action_on_equals=False)
        instance_hrange_false5 = pipe_types.HistoricalRange({}, {"k1": "v1", "k2": "v2"}, 3, compare_type="down", action_on_equals=False)
        instance_hrange_true1 = pipe_types.HistoricalRange({}, {}, 2, compare_type="up", action_on_equals=True)
        instance_hrange_true2 = pipe_types.HistoricalRange({}, {"k1": "v1", "k2": "v2"}, 2, compare_type="up", action_on_equals=True)
        instance_hrange_true3 = pipe_types.HistoricalRange({"k1": "v1", "k2": "v2"}, {}, 2, compare_type="down", action_on_equals=True)
        instance_hrange_true4 = pipe_types.HistoricalRange({"k1": "v1", "k2": "v2"}, {}, 2, compare_type="both", action_on_equals=True)
        instance_hrange_true5 = pipe_types.HistoricalRange({}, {"k1": "v1", "k2": "v2"}, 2, compare_type="both", action_on_equals=True)
        instance_hrange_true6 = pipe_types.HistoricalRange({}, {}, 2, compare_type="up", action_on_equals=True)

        self.assertFalse(instance_hrange_false1.needs_action())
        self.assertFalse(instance_hrange_false2.needs_action())
        self.assertFalse(instance_hrange_false3.needs_action())
        self.assertFalse(instance_hrange_false4.needs_action())
        self.assertFalse(instance_hrange_false5.needs_action())
        self.assertTrue(instance_hrange_true1.needs_action())
        self.assertTrue(instance_hrange_true2.needs_action())
        self.assertTrue(instance_hrange_true3.needs_action())
        self.assertTrue(instance_hrange_true4.needs_action())
        self.assertTrue(instance_hrange_true5.needs_action())
        self.assertTrue(instance_hrange_true6.needs_action())


if __name__ == '__main__':
    unittest.main()
