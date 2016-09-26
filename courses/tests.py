from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
# Create your tests here.
from .models import Course, Step

class CourseModelTests(TestCase):
	def test_course_creation(self):
		course = Course.objects.create(
			title="Python Regular Expressions",
			description="Learn to write redular expresions in python."
		)
		now = timezone.now()
		self.assertLess(course.created_at, now)

class StepModelTests(TestCase):
	def setUp(self):
		self.course = Course.objects.create(
			title="Python Testing",
			description="Learn to write tests in Python"
		)

	def test_step_creation(self):
		step = Step.objects.create(
			title = "Introduction to dectests",
			description = "learn to write tests in your docstrings",
			course = self.course
		)
		self.assertIn(step, self.course.step_set.all())


class CourseViewTests(TestCase):
	def setUp(self):
		self.course = Course.objects.create(
			title = "Python Testing",
			description = "Learn to write tests in python"
		)
		self.course2 = Course.objects.create(
			title = "New course",
			description = "A new course"
		)
		self.step = Step.objects.create(
			title = "Introduction to Doctests",
			description = "Learn to write tests in your docstrings.",
			course = self.course
		)

	def test_course_list_view(self):
		resp = self.client.get(reverse('course_list'))
		self.assertEqual(resp.status_code, 200)
		self.assertIn(self.course, resp.context['courses'])
		self.assertIn(self.course, resp.context['courses'])
		self.assertTemplateUsed(resp, 'courses/course_list.html')
		self.assertContains(resp, self.course.title)

	def test_course_detail_view(self):
		resp = self.client.get(reverse('course_detail',
										kwargs={'pk':self.course.pk}))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(self.course, resp.context['course'])

	def test_step_detail(self):
		resp = self.client.get(reverse('step_detail', kwargs={
					'course_pk':self.course.pk,
					'step_pk':self.step.pk}))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(self.step, resp.context['step'])



	