import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.person import Person


class TestPerson(unittest.TestCase):

    def test_constructor(self):
        # Given
        first_name = "John"
        last_name = "Doe"
        email = "john.doe@example.com"
        phone_number = "555-1234"

        # When
        person = Person(first_name, last_name, email, phone_number)

        # Then
        self.assertIsNotNone(person)

    def test_get_first_name(self):
        # Given
        expected_first_name = "Jane"
        person = Person(expected_first_name, "Smith", "jane@example.com", "555-5678")

        # When
        actual_first_name = person.get_first_name()

        # Then
        self.assertEqual(expected_first_name, actual_first_name)

    def test_get_last_name(self):
        # Given
        expected_last_name = "Smith"
        person = Person("Jane", expected_last_name, "jane@example.com", "555-5678")

        # When
        actual_last_name = person.get_last_name()

        # Then
        self.assertEqual(expected_last_name, actual_last_name)

    def test_get_email(self):
        # Given
        expected_email = "jane@example.com"
        person = Person("Jane", "Smith", expected_email, "555-5678")

        # When
        actual_email = person.get_email()

        # Then
        self.assertEqual(expected_email, actual_email)

    def test_get_phone_number(self):
        # Given
        expected_phone_number = "555-5678"
        person = Person("Jane", "Smith", "jane@example.com", expected_phone_number)

        # When
        actual_phone_number = person.get_phone_number()

        # Then
        self.assertEqual(expected_phone_number, actual_phone_number)

    def test_set_first_name(self):
        # Given
        person = Person("Jane", "Smith", "jane@example.com", "555-5678")
        new_first_name = "Janet"

        # When
        person.set_first_name(new_first_name)

        # Then
        self.assertEqual(new_first_name, person.get_first_name())

    def test_set_last_name(self):
        # Given
        person = Person("Jane", "Smith", "jane@example.com", "555-5678")
        new_last_name = "Johnson"

        # When
        person.set_last_name(new_last_name)

        # Then
        self.assertEqual(new_last_name, person.get_last_name())

    def test_set_email(self):
        # Given
        person = Person("Jane", "Smith", "jane@example.com", "555-5678")
        new_email = "janet.johnson@example.com"

        # When
        person.set_email(new_email)

        # Then
        self.assertEqual(new_email, person.get_email())

    def test_set_phone_number(self):
        # Given
        person = Person("Jane", "Smith", "jane@example.com", "555-5678")
        new_phone_number = "555-9999"

        # When
        person.set_phone_number(new_phone_number)

        # Then
        self.assertEqual(new_phone_number, person.get_phone_number())


if __name__ == "__main__":
    unittest.main()
