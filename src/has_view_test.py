import unittest
import has_view


class MyTestCase(unittest.TestCase):
    def test_module_view(self):
        instance_view1 = has_view.View(content="test", state=False, only_view_on_errors=False)
        instance_view2 = has_view.View(content="test", state=False, only_view_on_errors=True)
        instance_view3 = has_view.View(content="test", state=True, only_view_on_errors=False)
        instance_view4 = has_view.View(content="test", state=True, only_view_on_errors=True)

        self.assertEqual(instance_view1.user_view(), "test")
        self.assertEqual(instance_view2.user_view(), "test")
        self.assertEqual(instance_view3.user_view(), "test")
        self.assertIsNone(instance_view4.user_view())


if __name__ == '__main__':
    unittest.main()
