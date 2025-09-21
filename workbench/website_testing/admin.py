from django.contrib import admin
from .models import (
    WebsiteTest, PerformanceMetrics, AccessibilityMetrics,
    SEOMetrics, SecurityMetrics, UXMetrics, ErrorMetrics
)


@admin.register(WebsiteTest)
class WebsiteTestAdmin(admin.ModelAdmin):
    list_display = ['url', 'tested_by', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at', 'include_performance', 'include_accessibility', 'include_seo']
    search_fields = ['url', 'tested_by__email']
    readonly_fields = ['created_at', 'completed_at']


@admin.register(PerformanceMetrics)
class PerformanceMetricsAdmin(admin.ModelAdmin):
    list_display = ['test', 'lighthouse_performance_score', 'total_load_time', 'first_contentful_paint']
    readonly_fields = ['test']


@admin.register(AccessibilityMetrics)
class AccessibilityMetricsAdmin(admin.ModelAdmin):
    list_display = ['test', 'lighthouse_accessibility_score', 'wcag_aa_compliant', 'color_contrast_issues']
    readonly_fields = ['test']


@admin.register(SEOMetrics)
class SEOMetricsAdmin(admin.ModelAdmin):
    list_display = ['test', 'lighthouse_seo_score', 'has_title', 'has_meta_description']
    readonly_fields = ['test']


@admin.register(SecurityMetrics)
class SecurityMetricsAdmin(admin.ModelAdmin):
    list_display = ['test', 'uses_https', 'has_csp_header', 'has_x_frame_options']
    readonly_fields = ['test']


@admin.register(UXMetrics)
class UXMetricsAdmin(admin.ModelAdmin):
    list_display = ['test', 'lighthouse_best_practices_score', 'is_mobile_responsive', 'adequate_touch_targets']
    readonly_fields = ['test']


@admin.register(ErrorMetrics)
class ErrorMetricsAdmin(admin.ModelAdmin):
    list_display = ['test', 'js_errors_count', 'broken_links_count']
    readonly_fields = ['test']