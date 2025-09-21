from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch, MagicMock

from .models import WebsiteTest, PerformanceMetrics
from .services import WebsiteTestingService

User = get_user_model()


class WebsiteTestingModelTest(TestCase):
    """Test the website testing models"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )

    def test_website_test_creation(self):
        """Test creating a website test"""
        test = WebsiteTest.objects.create(
            url='https://example.com',
            tested_by=self.user
        )
        
        self.assertEqual(test.url, 'https://example.com')
        self.assertEqual(test.tested_by, self.user)
        self.assertEqual(test.status, 'pending')
        self.assertTrue(test.include_performance)
        self.assertTrue(test.include_accessibility)

    def test_website_test_str(self):
        """Test string representation of website test"""
        test = WebsiteTest.objects.create(
            url='https://example.com',
            tested_by=self.user
        )
        
        expected = f"Test for https://example.com by {self.user}"
        self.assertEqual(str(test), expected)


class WebsiteTestingServiceTest(TestCase):
    """Test the website testing service"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.service = WebsiteTestingService()

    def test_service_initialization(self):
        """Test service initializes correctly"""
        self.assertIsInstance(self.service, WebsiteTestingService)

    @patch('requests.get')
    def test_basic_performance_test(self, mock_get):
        """Test basic performance testing without Playwright"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<html><head><title>Test</title></head><body>Test</body></html>'
        mock_get.return_value = mock_response
        
        result = self.service._run_basic_performance_test('https://example.com')
        
        self.assertIn('loadTime', result)
        self.assertEqual(result['statusCode'], 200)

    @patch('requests.get')
    def test_fetch_page_content(self, mock_get):
        """Test fetching page content"""
        mock_response = MagicMock()
        mock_response.text = '<html><head><title>Test Page</title></head><body>Content</body></html>'
        mock_get.return_value = mock_response
        
        content = self.service._fetch_page_content('https://example.com')
        
        self.assertIn('Test Page', content)
        self.assertIn('Content', content)

    def test_mock_score_calculations(self):
        """Test mock Lighthouse score calculations"""
        # Create test objects
        test = WebsiteTest.objects.create(
            url='https://example.com',
            tested_by=self.user
        )
        performance = PerformanceMetrics.objects.create(
            test=test,
            total_load_time=2000.0,
            first_contentful_paint=1500.0
        )
        
        score = self.service._calculate_mock_performance_score(performance)
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)


class WebsiteTestingViewTest(TestCase):
    """Test the website testing views"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_dashboard_view(self):
        """Test the dashboard view"""
        url = reverse('website_testing:dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Website Testing Dashboard')

    def test_create_test_view_get(self):
        """Test GET request to create test view"""
        url = reverse('website_testing:create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create New Website Test')

    def test_create_test_view_post(self):
        """Test POST request to create test view"""
        url = reverse('website_testing:create')
        data = {
            'url': 'https://example.com',
            'include_performance': True,
            'include_accessibility': True,
            'include_seo': True,
            'include_security': True,
            'include_ux': True,
        }
        
        with patch('threading.Thread.start'):  # Mock the background thread
            response = self.client.post(url, data)
        
        # Should redirect to test detail
        self.assertEqual(response.status_code, 302)
        
        # Test should be created
        test = WebsiteTest.objects.filter(tested_by=self.user).first()
        self.assertIsNotNone(test)
        self.assertEqual(test.url, 'https://example.com')

    def test_test_detail_view(self):
        """Test the test detail view"""
        test = WebsiteTest.objects.create(
            url='https://example.com',
            tested_by=self.user,
            status='completed'
        )
        
        url = reverse('website_testing:detail', kwargs={'pk': test.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Results')
        self.assertContains(response, 'https://example.com')

    def test_test_status_api(self):
        """Test the test status API endpoint"""
        test = WebsiteTest.objects.create(
            url='https://example.com',
            tested_by=self.user,
            status='running'
        )
        
        url = reverse('website_testing:status', kwargs={'pk': test.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'running')

    def test_unauthorized_access(self):
        """Test that unauthorized users cannot access tests"""
        other_user = User.objects.create_user(
            email='other@example.com',
            first_name='Other',
            last_name='User'
        )
        
        test = WebsiteTest.objects.create(
            url='https://example.com',
            tested_by=other_user
        )
        
        url = reverse('website_testing:detail', kwargs={'pk': test.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)  # Should not find the test


class WebsiteTestingFormTest(TestCase):
    """Test the website testing forms"""

    def test_url_cleaning(self):
        """Test URL cleaning in the form"""
        from .forms import WebsiteTestForm
        
        # Test adding https:// prefix
        form_data = {'url': 'example.com'}
        form = WebsiteTestForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['url'], 'https://example.com')

    def test_invalid_url(self):
        """Test invalid URL handling"""
        from .forms import WebsiteTestForm
        
        form_data = {'url': 'not-a-valid-url'}
        form = WebsiteTestForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('url', form.errors)