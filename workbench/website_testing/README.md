# Website Testing Dashboard

A comprehensive Django application for testing website performance, accessibility, SEO, security, and user experience metrics.

## Features

### 🎯 Comprehensive Testing Categories

- **Performance Metrics**: Core Web Vitals (LCP, FID, CLS), page load times, TTFB, resource analysis
- **Accessibility Testing**: WCAG compliance, color contrast, ARIA labels, screen reader compatibility
- **SEO Analysis**: Meta tags, structured data, sitemap/robots.txt validation
- **Security Checks**: HTTPS usage, security headers (CSP, X-Frame-Options, etc.)
- **User Experience**: Mobile responsiveness, touch targets, font readability
- **Error Detection**: JavaScript errors, console warnings, broken links

### 🚀 Key Capabilities

- **Real-time Testing**: Background test execution with live status updates
- **Historical Tracking**: Store and compare test results over time
- **Lighthouse Integration**: Ready for Lighthouse API integration
- **Playwright Support**: Full browser automation when dependencies are installed
- **Responsive Dashboard**: Clean, mobile-friendly interface
- **User Management**: User-specific tests with proper permissions

## Installation

### Prerequisites

- Django 3.1+
- Python 3.8+
- Optional: Playwright for advanced browser testing
- Optional: Node.js + Lighthouse for official performance scores

### Basic Setup

1. Add to your Django `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... other apps
    'workbench.website_testing',
]
```

2. Include URLs in your main `urls.py`:
```python
urlpatterns = [
    # ... other patterns
    path('website-testing/', include('workbench.website_testing.urls')),
]
```

3. Run migrations:
```bash
python manage.py makemigrations website_testing
python manage.py migrate
```

### Optional Dependencies

For enhanced testing capabilities:

```bash
# Install Playwright for real browser testing
pip install playwright
playwright install

# Install via npm for Lighthouse integration
npm install -g lighthouse

# Install axe-core for accessibility testing
npm install axe-core
```

## Usage

### Web Interface

1. **Dashboard**: Navigate to `/website-testing/` to view the main dashboard
2. **Create Test**: Click "New Test" to start testing a website
3. **Configure Test**: Select which metrics to test (performance, accessibility, etc.)
4. **View Results**: Monitor test progress and view detailed results

### Management Commands

Run tests from the command line:

```bash
# Run all pending tests
python manage.py run_website_tests

# Run a specific test
python manage.py run_website_tests --test-id 123

# Limit number of tests to run
python manage.py run_website_tests --max-tests 5
```

## Architecture

### Models

- **WebsiteTest**: Main test configuration and status
- **PerformanceMetrics**: Page load times, Core Web Vitals, resource analysis
- **AccessibilityMetrics**: WCAG compliance, ARIA issues, contrast problems
- **SEOMetrics**: Meta tags, structured data, technical SEO factors
- **SecurityMetrics**: HTTPS usage, security headers
- **UXMetrics**: Mobile responsiveness, touch targets, font readability
- **ErrorMetrics**: JavaScript errors, broken links

### Service Architecture

The `WebsiteTestingService` class orchestrates all testing:

1. **HTTP-based Testing**: Basic functionality using `requests` library
2. **Playwright Integration**: Advanced browser testing when available
3. **Lighthouse Integration**: Official performance/accessibility scores
4. **Background Processing**: Asynchronous test execution

### Testing Methods

#### Performance Testing
- Measures page load time, TTFB, FCP, LCP, TTI, DOM Content Loaded
- Analyzes resource sizes and compression
- Calculates Core Web Vitals scores
- Integrates with Lighthouse for official performance scores

#### Accessibility Testing
- Checks for WCAG AA compliance
- Identifies color contrast issues
- Finds missing alt text and ARIA labels
- Tests keyboard navigation
- Ready for axe-core integration

#### SEO Analysis
- Validates meta tags (title, description, canonical)
- Detects structured data and schema markup
- Checks for sitemap.xml and robots.txt
- Analyzes technical SEO factors

#### Security Assessment
- Verifies HTTPS usage and SSL certificates
- Checks security headers (CSP, X-Frame-Options, HSTS, etc.)
- Analyzes response headers for security best practices

#### User Experience Testing
- Tests mobile responsiveness
- Validates viewport meta tags
- Checks touch target sizes
- Analyzes font readability

#### Error Detection
- Captures JavaScript console errors and warnings
- Identifies broken links and HTTP errors
- Logs network issues and failed requests

## API Integration

### Lighthouse Integration

The dashboard is designed to integrate with Google Lighthouse:

```python
# Example Lighthouse integration (requires lighthouse npm package)
def run_lighthouse_audit(url):
    import subprocess
    import json
    
    result = subprocess.run([
        'lighthouse', url, 
        '--output=json', 
        '--chrome-flags=--headless'
    ], capture_output=True, text=True)
    
    return json.loads(result.stdout)
```

### Playwright Advanced Testing

For real browser automation:

```python
from playwright.sync_api import sync_playwright

def test_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Performance timing
        page.goto(url, wait_until='networkidle')
        metrics = page.evaluate('() => performance.getEntriesByType("navigation")[0]')
        
        # Accessibility testing with axe-core
        page.add_script_tag(path='node_modules/axe-core/axe.min.js')
        axe_results = page.evaluate('() => axe.run()')
        
        browser.close()
        return metrics, axe_results
```

## Dashboard Screenshots

### Main Dashboard
The dashboard provides an overview of all tests with filtering and statistics:

- **Statistics Cards**: Total, completed, pending, and failed tests
- **Test History Table**: Recent tests with status and actions
- **Filtering**: Filter by status, time period, and URL
- **Quick Actions**: View, rerun, or delete tests

### Test Creation
Simple form interface for creating new tests:

- **URL Input**: Enter website URL to test
- **Category Selection**: Choose which metrics to test
- **Background Execution**: Tests run asynchronously

### Results Display
Comprehensive results visualization:

- **Lighthouse-style Scores**: Performance, accessibility, SEO, best practices
- **Detailed Metrics**: All collected data organized by category
- **Visual Indicators**: Color-coded status badges and progress indicators
- **Historical Comparison**: Compare results across multiple tests

## Performance Considerations

- **Background Processing**: Tests run asynchronously to avoid blocking the UI
- **Database Optimization**: Efficient queries with proper indexing
- **Caching**: Ready for Redis/Memcached integration
- **Rate Limiting**: Built-in protections against excessive testing

## Security

- **User Isolation**: Tests are user-specific with proper permission controls
- **Input Validation**: URL validation and sanitization
- **CSRF Protection**: All forms protected against CSRF attacks
- **Admin Interface**: Full Django admin integration for management

## Monitoring and Analytics

The dashboard includes comprehensive tracking:

- **Test Success Rates**: Monitor testing reliability
- **Performance Trends**: Track website improvements over time
- **User Activity**: See which users are most active
- **Error Analysis**: Identify common testing issues

## Extensibility

The architecture supports easy extension:

- **Custom Metrics**: Add new metric categories
- **Third-party Integration**: Connect additional testing tools
- **API Endpoints**: JSON API for external integrations
- **Webhook Support**: Ready for notification systems

## Contributing

To extend the testing capabilities:

1. Add new models for additional metrics
2. Extend the `WebsiteTestingService` class
3. Update templates for new result displays
4. Add tests for new functionality

## License

This website testing dashboard is part of the Workbench project and follows the same licensing terms.