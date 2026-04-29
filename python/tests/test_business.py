import unittest
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.business import Business


class TestBusiness(unittest.TestCase):

    def test_constructor(self):
        # Given
        business_name = "Acme Corp"

        # When
        business = Business(business_name)

        # Then
        self.assertIsNotNone(business)

    def test_get_business_name(self):
        # Given
        expected_business_name = "Tech Solutions Inc"
        business = Business(expected_business_name)

        # When
        actual_business_name = business.get_business_name()

        # Then
        self.assertEqual(expected_business_name, actual_business_name)

    def test_set_business_name(self):
        # Given
        business = Business("Acme Corp")
        new_business_name = "Global Industries"

        # When
        business.set_business_name(new_business_name)

        # Then
        self.assertEqual(new_business_name, business.get_business_name())


if __name__ == "__main__":
    unittest.main()
