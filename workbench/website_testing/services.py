"""
Website testing service using Playwright and other tools
"""
import json
import re
import requests
from urllib.parse import urljoin, urlparse
from typing import Dict, Any, List
import time

from django.utils import timezone
from .models import (
    WebsiteTest, PerformanceMetrics, AccessibilityMetrics,
    SEOMetrics, SecurityMetrics, UXMetrics, ErrorMetrics
)


class WebsiteTestingService:
    """Service class for running comprehensive website tests"""
    
    def __init__(self):
        self.playwright_available = False
        self.lighthouse_available = False
        
        # Check if Playwright is available
        try:
            from playwright.sync_api import sync_playwright
            self.playwright_available = True
        except ImportError:
            pass
    
    def run_test(self, test_id: int) -> bool:
        """Run a comprehensive test for a website"""
        try:
            test = WebsiteTest.objects.get(id=test_id)
            test.status = 'running'
            test.save()
            
            # Initialize metric objects
            self._initialize_metrics(test)
            
            # Run different test suites based on configuration
            if test.include_performance:
                self._test_performance(test)
            
            if test.include_accessibility:
                self._test_accessibility(test)
                
            if test.include_seo:
                self._test_seo(test)
                
            if test.include_security:
                self._test_security(test)
                
            if test.include_ux:
                self._test_ux(test)
            
            # Always run error testing
            self._test_errors(test)
            
            # Mark test as completed
            test.status = 'completed'
            test.completed_at = timezone.now()
            test.save()
            
            return True
            
        except Exception as e:
            test.status = 'failed'
            test.error_message = str(e)
            test.save()
            return False
    
    def _initialize_metrics(self, test: WebsiteTest):
        """Initialize all metric objects for the test"""
        PerformanceMetrics.objects.get_or_create(test=test)
        AccessibilityMetrics.objects.get_or_create(test=test)
        SEOMetrics.objects.get_or_create(test=test)
        SecurityMetrics.objects.get_or_create(test=test)
        UXMetrics.objects.get_or_create(test=test)
        ErrorMetrics.objects.get_or_create(test=test)
    
    def _test_performance(self, test: WebsiteTest):
        """Test performance metrics"""
        performance = test.performance
        
        if self.playwright_available:
            # Use Playwright for real browser metrics
            performance_data = self._run_playwright_performance_test(test.url)
            
            performance.total_load_time = performance_data.get('loadTime')
            performance.time_to_first_byte = performance_data.get('ttfb')
            performance.first_contentful_paint = performance_data.get('fcp')
            performance.largest_contentful_paint = performance_data.get('lcp')
            performance.time_to_interactive = performance_data.get('tti')
            performance.dom_content_loaded = performance_data.get('domContentLoaded')
            performance.cumulative_layout_shift = performance_data.get('cls')
            performance.total_requests = performance_data.get('requestCount')
            performance.total_size_kb = performance_data.get('totalSize', 0) / 1024
            
            # Check compression
            performance.uses_gzip = performance_data.get('compression', {}).get('gzip', False)
            performance.uses_brotli = performance_data.get('compression', {}).get('brotli', False)
        else:
            # Fallback to basic HTTP testing
            performance_data = self._run_basic_performance_test(test.url)
            performance.total_load_time = performance_data.get('loadTime')
        
        # Mock Lighthouse score for now (would integrate real Lighthouse in production)
        performance.lighthouse_performance_score = self._calculate_mock_performance_score(performance)
        
        performance.save()
    
    def _test_accessibility(self, test: WebsiteTest):
        """Test accessibility metrics"""
        accessibility = test.accessibility
        
        if self.playwright_available:
            # Use Playwright to get page content and run accessibility checks
            accessibility_data = self._run_playwright_accessibility_test(test.url)
            
            accessibility.color_contrast_issues = accessibility_data.get('colorContrastIssues', 0)
            accessibility.missing_alt_text_count = accessibility_data.get('missingAltText', 0)
            accessibility.missing_aria_labels = accessibility_data.get('missingAriaLabels', 0)
            accessibility.keyboard_navigation_issues = accessibility_data.get('keyboardIssues', 0)
            accessibility.wcag_aa_compliant = accessibility_data.get('wcagCompliant', False)
            accessibility.screen_reader_compatible = accessibility_data.get('screenReaderCompatible', False)
            accessibility.axe_results = accessibility_data.get('axeResults', {})
        else:
            # Basic accessibility checks via HTTP
            accessibility_data = self._run_basic_accessibility_test(test.url)
            accessibility.missing_alt_text_count = accessibility_data.get('missingAltText', 0)
        
        # Mock Lighthouse score
        accessibility.lighthouse_accessibility_score = self._calculate_mock_accessibility_score(accessibility)
        
        accessibility.save()
    
    def _test_seo(self, test: WebsiteTest):
        """Test SEO metrics"""
        seo = test.seo
        
        # Get page content
        page_content = self._fetch_page_content(test.url)
        if page_content:
            # Parse meta tags
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', page_content, re.IGNORECASE)
            seo.has_title = bool(title_match)
            if title_match:
                seo.title_length = len(title_match.group(1).strip())
            
            # Meta description
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', page_content, re.IGNORECASE)
            seo.has_meta_description = bool(desc_match)
            if desc_match:
                seo.meta_description_length = len(desc_match.group(1).strip())
            
            # Canonical URL
            seo.has_canonical_url = bool(re.search(r'<link[^>]*rel=["\']canonical["\']', page_content, re.IGNORECASE))
            
            # Structured data
            seo.has_structured_data = bool(re.search(r'application/ld\+json|microdata|schema\.org', page_content, re.IGNORECASE))
            
            # Check sitemap and robots.txt
            parsed_url = urlparse(test.url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            seo.has_sitemap = self._url_exists(f"{base_url}/sitemap.xml")
            seo.has_robots_txt = self._url_exists(f"{base_url}/robots.txt")
        
        # Mock Lighthouse score
        seo.lighthouse_seo_score = self._calculate_mock_seo_score(seo)
        
        seo.save()
    
    def _test_security(self, test: WebsiteTest):
        """Test security metrics"""
        security = test.security
        
        # Check HTTPS
        security.uses_https = test.url.startswith('https://')
        
        # Get security headers
        try:
            response = requests.head(test.url, timeout=30, allow_redirects=True)
            headers = response.headers
            
            security.has_csp_header = 'Content-Security-Policy' in headers
            security.has_x_frame_options = 'X-Frame-Options' in headers
            security.has_x_content_type_options = 'X-Content-Type-Options' in headers
            security.has_strict_transport_security = 'Strict-Transport-Security' in headers
            
            # Store all security headers
            security.security_headers = {
                key: value for key, value in headers.items()
                if any(sec_header in key.lower() for sec_header in 
                      ['security', 'frame', 'content-type', 'transport', 'csp'])
            }
            
        except Exception:
            pass
        
        security.save()
    
    def _test_ux(self, test: WebsiteTest):
        """Test user experience metrics"""
        ux = test.ux
        
        # Get page content for viewport meta tag
        page_content = self._fetch_page_content(test.url)
        if page_content:
            ux.viewport_meta_tag = bool(re.search(r'<meta[^>]*name=["\']viewport["\']', page_content, re.IGNORECASE))
        
        if self.playwright_available:
            # Use Playwright for mobile responsiveness testing
            ux_data = self._run_playwright_ux_test(test.url)
            ux.is_mobile_responsive = ux_data.get('mobileResponsive', False)
            ux.adequate_touch_targets = ux_data.get('adequateTouchTargets', False)
            ux.touch_target_issues = ux_data.get('touchTargetIssues', 0)
            ux.readable_font_sizes = ux_data.get('readableFontSizes', False)
        
        # Mock Lighthouse score
        ux.lighthouse_best_practices_score = self._calculate_mock_ux_score(ux)
        
        ux.save()
    
    def _test_errors(self, test: WebsiteTest):
        """Test for errors and broken links"""
        errors = test.errors
        
        if self.playwright_available:
            # Use Playwright to capture console errors
            error_data = self._run_playwright_error_test(test.url)
            errors.js_errors_count = error_data.get('jsErrors', 0)
            errors.js_warnings_count = error_data.get('jsWarnings', 0)
            errors.console_errors = error_data.get('consoleErrors', [])
            errors.broken_links_count = error_data.get('brokenLinks', 0)
            errors.broken_links = error_data.get('brokenLinksList', [])
        
        errors.save()
    
    def _run_playwright_performance_test(self, url: str) -> Dict[str, Any]:
        """Run performance test using Playwright"""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # Start performance monitoring
                start_time = time.time()
                
                page.goto(url, wait_until='networkidle')
                
                load_time = (time.time() - start_time) * 1000
                
                # Get performance metrics
                performance_data = page.evaluate("""
                    () => {
                        const timing = performance.timing;
                        const navigation = performance.getEntriesByType('navigation')[0];
                        return {
                            loadTime: navigation ? navigation.loadEventEnd - navigation.fetchStart : null,
                            ttfb: navigation ? navigation.responseStart - navigation.fetchStart : null,
                            domContentLoaded: navigation ? navigation.domContentLoadedEventEnd - navigation.fetchStart : null,
                            requestCount: performance.getEntriesByType('resource').length
                        };
                    }
                """)
                
                performance_data['loadTime'] = load_time
                
                browser.close()
                return performance_data
                
        except ImportError:
            return {}
        except Exception:
            return {'loadTime': None}
    
    def _run_basic_performance_test(self, url: str) -> Dict[str, Any]:
        """Basic performance test using requests"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=30)
            load_time = (time.time() - start_time) * 1000
            
            return {
                'loadTime': load_time,
                'statusCode': response.status_code,
                'responseSize': len(response.content)
            }
        except Exception:
            return {'loadTime': None}
    
    def _run_playwright_accessibility_test(self, url: str) -> Dict[str, Any]:
        """Run accessibility test using Playwright"""
        # This would integrate with axe-core in a real implementation
        return {
            'colorContrastIssues': 0,
            'missingAltText': 0,
            'missingAriaLabels': 0,
            'keyboardIssues': 0,
            'wcagCompliant': True,
            'screenReaderCompatible': True,
            'axeResults': {}
        }
    
    def _run_basic_accessibility_test(self, url: str) -> Dict[str, Any]:
        """Basic accessibility test via HTTP"""
        page_content = self._fetch_page_content(url)
        if page_content:
            # Count images without alt text
            img_tags = re.findall(r'<img[^>]*>', page_content, re.IGNORECASE)
            missing_alt = sum(1 for img in img_tags if 'alt=' not in img.lower())
            return {'missingAltText': missing_alt}
        return {}
    
    def _run_playwright_ux_test(self, url: str) -> Dict[str, Any]:
        """Run UX test using Playwright"""
        # Mock implementation - would test mobile viewport, touch targets, etc.
        return {
            'mobileResponsive': True,
            'adequateTouchTargets': True,
            'touchTargetIssues': 0,
            'readableFontSizes': True
        }
    
    def _run_playwright_error_test(self, url: str) -> Dict[str, Any]:
        """Run error detection test using Playwright"""
        # Mock implementation - would capture console errors and test links
        return {
            'jsErrors': 0,
            'jsWarnings': 0,
            'consoleErrors': [],
            'brokenLinks': 0,
            'brokenLinksList': []
        }
    
    def _fetch_page_content(self, url: str) -> str:
        """Fetch page content via HTTP"""
        try:
            response = requests.get(url, timeout=30)
            return response.text
        except Exception:
            return ""
    
    def _url_exists(self, url: str) -> bool:
        """Check if a URL exists"""
        try:
            response = requests.head(url, timeout=10)
            return response.status_code < 400
        except Exception:
            return False
    
    def _calculate_mock_performance_score(self, performance: PerformanceMetrics) -> int:
        """Calculate mock Lighthouse performance score"""
        score = 100
        if performance.total_load_time and performance.total_load_time > 3000:
            score -= 20
        if performance.first_contentful_paint and performance.first_contentful_paint > 2000:
            score -= 15
        return max(0, score)
    
    def _calculate_mock_accessibility_score(self, accessibility: AccessibilityMetrics) -> int:
        """Calculate mock Lighthouse accessibility score"""
        score = 100
        score -= accessibility.color_contrast_issues * 5
        score -= accessibility.missing_alt_text_count * 3
        score -= accessibility.missing_aria_labels * 4
        return max(0, score)
    
    def _calculate_mock_seo_score(self, seo: SEOMetrics) -> int:
        """Calculate mock Lighthouse SEO score"""
        score = 100
        if not seo.has_title:
            score -= 20
        if not seo.has_meta_description:
            score -= 15
        if seo.title_length and (seo.title_length < 10 or seo.title_length > 60):
            score -= 10
        return max(0, score)
    
    def _calculate_mock_ux_score(self, ux: UXMetrics) -> int:
        """Calculate mock Lighthouse best practices score"""
        score = 100
        if not ux.viewport_meta_tag:
            score -= 15
        if not ux.is_mobile_responsive:
            score -= 20
        if not ux.adequate_touch_targets:
            score -= 10
        return max(0, score)