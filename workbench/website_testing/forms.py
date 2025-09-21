from django import forms
from .models import WebsiteTest


class WebsiteTestForm(forms.ModelForm):
    """Form for creating a new website test"""
    
    class Meta:
        model = WebsiteTest
        fields = [
            'url', 
            'include_performance', 
            'include_accessibility', 
            'include_seo', 
            'include_security', 
            'include_ux'
        ]
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
                'required': True
            }),
        }
        help_texts = {
            'url': 'Enter the complete URL including https:// or http://',
            'include_performance': 'Test Core Web Vitals, load times, and resource optimization',
            'include_accessibility': 'Check WCAG compliance, ARIA labels, and screen reader compatibility',
            'include_seo': 'Analyze meta tags, structured data, and technical SEO factors',
            'include_security': 'Verify HTTPS usage and security headers',
            'include_ux': 'Evaluate mobile responsiveness and user experience factors'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to checkboxes
        for field_name in ['include_performance', 'include_accessibility', 'include_seo', 
                          'include_security', 'include_ux']:
            self.fields[field_name].widget.attrs.update({'class': 'form-check-input'})

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            # Ensure URL has a scheme
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Basic URL validation
            if not any(tld in url for tld in ['.com', '.org', '.net', '.edu', '.gov', '.co', '.io', '.dev']):
                # Allow localhost and IP addresses for testing
                if 'localhost' not in url and not any(c.isdigit() for c in url.split('://')[1].split('/')[0]):
                    raise forms.ValidationError('Please enter a valid URL with a proper domain.')
        
        return url


class TestFilterForm(forms.Form):
    """Form for filtering test results in the dashboard"""
    
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    PERIOD_CHOICES = [
        ('', 'All Time'),
        ('today', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('year', 'This Year'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    period = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    url_contains = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by URL...'
        })
    )