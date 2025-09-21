from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


User = get_user_model()


class WebsiteTest(models.Model):
    """Model to store website test configurations and results"""
    url = models.URLField(max_length=2048, help_text="URL to test")
    tested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Test configuration
    include_performance = models.BooleanField(default=True)
    include_accessibility = models.BooleanField(default=True)
    include_seo = models.BooleanField(default=True)
    include_security = models.BooleanField(default=True)
    include_ux = models.BooleanField(default=True)
    
    # Overall status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Test for {self.url} by {self.tested_by}"
    
    def get_absolute_url(self):
        return reverse('website_testing:detail', kwargs={'pk': self.pk})


class PerformanceMetrics(models.Model):
    """Performance metrics from Lighthouse and Playwright"""
    test = models.OneToOneField(WebsiteTest, on_delete=models.CASCADE, related_name='performance')
    
    # Page load metrics (in milliseconds)
    total_load_time = models.FloatField(null=True, blank=True)
    time_to_first_byte = models.FloatField(null=True, blank=True)
    first_contentful_paint = models.FloatField(null=True, blank=True)
    largest_contentful_paint = models.FloatField(null=True, blank=True)
    time_to_interactive = models.FloatField(null=True, blank=True)
    dom_content_loaded = models.FloatField(null=True, blank=True)
    
    # Core Web Vitals
    cumulative_layout_shift = models.FloatField(null=True, blank=True)
    first_input_delay = models.FloatField(null=True, blank=True)
    
    # Resource metrics
    total_requests = models.IntegerField(null=True, blank=True)
    total_size_kb = models.FloatField(null=True, blank=True)
    image_size_kb = models.FloatField(null=True, blank=True)
    css_size_kb = models.FloatField(null=True, blank=True)
    js_size_kb = models.FloatField(null=True, blank=True)
    
    # Compression
    uses_gzip = models.BooleanField(null=True, blank=True)
    uses_brotli = models.BooleanField(null=True, blank=True)
    
    # Lighthouse performance score (0-100)
    lighthouse_performance_score = models.IntegerField(null=True, blank=True)


class AccessibilityMetrics(models.Model):
    """Accessibility metrics from axe-core and Lighthouse"""
    test = models.OneToOneField(WebsiteTest, on_delete=models.CASCADE, related_name='accessibility')
    
    # WCAG compliance
    wcag_aa_compliant = models.BooleanField(null=True, blank=True)
    color_contrast_issues = models.IntegerField(default=0)
    missing_alt_text_count = models.IntegerField(default=0)
    missing_aria_labels = models.IntegerField(default=0)
    keyboard_navigation_issues = models.IntegerField(default=0)
    
    # Screen reader compatibility
    screen_reader_compatible = models.BooleanField(null=True, blank=True)
    
    # Lighthouse accessibility score (0-100)
    lighthouse_accessibility_score = models.IntegerField(null=True, blank=True)
    
    # Detailed findings (JSON field for detailed results)
    axe_results = models.JSONField(default=dict, blank=True)


class SEOMetrics(models.Model):
    """SEO metrics and analysis"""
    test = models.OneToOneField(WebsiteTest, on_delete=models.CASCADE, related_name='seo')
    
    # Meta tags
    has_title = models.BooleanField(default=False)
    title_length = models.IntegerField(null=True, blank=True)
    has_meta_description = models.BooleanField(default=False)
    meta_description_length = models.IntegerField(null=True, blank=True)
    has_canonical_url = models.BooleanField(default=False)
    
    # Structured data
    has_structured_data = models.BooleanField(default=False)
    structured_data_types = models.JSONField(default=list, blank=True)
    
    # Technical SEO
    has_sitemap = models.BooleanField(null=True, blank=True)
    has_robots_txt = models.BooleanField(null=True, blank=True)
    
    # Lighthouse SEO score (0-100)
    lighthouse_seo_score = models.IntegerField(null=True, blank=True)


class SecurityMetrics(models.Model):
    """Security-related metrics"""
    test = models.OneToOneField(WebsiteTest, on_delete=models.CASCADE, related_name='security')
    
    # HTTPS
    uses_https = models.BooleanField(default=False)
    has_valid_ssl = models.BooleanField(null=True, blank=True)
    
    # Security headers
    has_csp_header = models.BooleanField(default=False)
    has_x_frame_options = models.BooleanField(default=False)
    has_x_content_type_options = models.BooleanField(default=False)
    has_strict_transport_security = models.BooleanField(default=False)
    
    # Security scan results
    security_headers = models.JSONField(default=dict, blank=True)


class UXMetrics(models.Model):
    """User Experience metrics"""
    test = models.OneToOneField(WebsiteTest, on_delete=models.CASCADE, related_name='ux')
    
    # Mobile responsiveness
    is_mobile_responsive = models.BooleanField(null=True, blank=True)
    viewport_meta_tag = models.BooleanField(default=False)
    
    # Touch targets
    adequate_touch_targets = models.BooleanField(null=True, blank=True)
    touch_target_issues = models.IntegerField(default=0)
    
    # Typography
    readable_font_sizes = models.BooleanField(null=True, blank=True)
    
    # Lighthouse best practices score (0-100)
    lighthouse_best_practices_score = models.IntegerField(null=True, blank=True)


class ErrorMetrics(models.Model):
    """Error and stability metrics"""
    test = models.OneToOneField(WebsiteTest, on_delete=models.CASCADE, related_name='errors')
    
    # JavaScript errors
    js_errors_count = models.IntegerField(default=0)
    js_warnings_count = models.IntegerField(default=0)
    console_errors = models.JSONField(default=list, blank=True)
    
    # Broken links
    broken_links_count = models.IntegerField(default=0)
    broken_links = models.JSONField(default=list, blank=True)
    
    # HTTP errors
    http_errors = models.JSONField(default=list, blank=True)