from django.test import TestCase
from .models import User

# Create your tests here.
class StudentAccountTestCase(TestCase):
    def testNonStudentEmail(self) -> None:
        result = User.objects.create(email="nonstudent@gmail.com",first_name="Test",last_name="Case")
        self.assertIsNone(result)
    def testStudentEmail(self):
        result = User.objects.create(email="nonstudent@tamu.edu",first_name="Test",last_name="Case")
        self.assertIsNotNone(result)
        