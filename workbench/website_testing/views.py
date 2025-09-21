from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
import threading

from .models import WebsiteTest
from .forms import WebsiteTestForm, TestFilterForm
from .services import WebsiteTestingService


@login_required
def dashboard(request):
    """Main dashboard view showing test history and form to create new tests"""
    
    # Handle filtering
    filter_form = TestFilterForm(request.GET or None)
    tests = WebsiteTest.objects.filter(tested_by=request.user)
    
    if filter_form.is_valid():
        # Filter by status
        if filter_form.cleaned_data.get('status'):
            tests = tests.filter(status=filter_form.cleaned_data['status'])
        
        # Filter by period
        period = filter_form.cleaned_data.get('period')
        if period:
            now = timezone.now()
            if period == 'today':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'week':
                start_date = now - timedelta(days=7)
            elif period == 'month':
                start_date = now - timedelta(days=30)
            elif period == 'year':
                start_date = now - timedelta(days=365)
            else:
                start_date = None
            
            if start_date:
                tests = tests.filter(created_at__gte=start_date)
        
        # Filter by URL
        if filter_form.cleaned_data.get('url_contains'):
            tests = tests.filter(url__icontains=filter_form.cleaned_data['url_contains'])
    
    # Pagination
    paginator = Paginator(tests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total_tests': WebsiteTest.objects.filter(tested_by=request.user).count(),
        'completed_tests': WebsiteTest.objects.filter(tested_by=request.user, status='completed').count(),
        'failed_tests': WebsiteTest.objects.filter(tested_by=request.user, status='failed').count(),
        'pending_tests': WebsiteTest.objects.filter(tested_by=request.user, status__in=['pending', 'running']).count(),
    }
    
    return render(request, 'website_testing/dashboard.html', {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'stats': stats,
    })


@login_required
def create_test(request):
    """Create a new website test"""
    
    if request.method == 'POST':
        form = WebsiteTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.tested_by = request.user
            test.save()
            
            # Start the test in background
            service = WebsiteTestingService()
            thread = threading.Thread(target=service.run_test, args=(test.id,))
            thread.daemon = True
            thread.start()
            
            messages.success(request, f'Test started for {test.url}. Results will be available shortly.')
            return redirect('website_testing:detail', pk=test.pk)
    else:
        form = WebsiteTestForm()
    
    return render(request, 'website_testing/create_test.html', {
        'form': form,
    })


@login_required 
def test_detail(request, pk):
    """Show detailed test results"""
    
    test = get_object_or_404(WebsiteTest, pk=pk, tested_by=request.user)
    
    # Get all related metrics
    context = {
        'test': test,
        'performance': getattr(test, 'performance', None),
        'accessibility': getattr(test, 'accessibility', None),
        'seo': getattr(test, 'seo', None),
        'security': getattr(test, 'security', None),
        'ux': getattr(test, 'ux', None),
        'errors': getattr(test, 'errors', None),
    }
    
    return render(request, 'website_testing/test_detail.html', context)


@login_required
def test_status(request, pk):
    """API endpoint to check test status (for AJAX polling)"""
    
    test = get_object_or_404(WebsiteTest, pk=pk, tested_by=request.user)
    
    return JsonResponse({
        'status': test.status,
        'completed_at': test.completed_at.isoformat() if test.completed_at else None,
        'error_message': test.error_message,
    })


@login_required
def rerun_test(request, pk):
    """Rerun an existing test"""
    
    if request.method == 'POST':
        test = get_object_or_404(WebsiteTest, pk=pk, tested_by=request.user)
        
        # Reset test status
        test.status = 'pending'
        test.completed_at = None
        test.error_message = ''
        test.save()
        
        # Start the test in background
        service = WebsiteTestingService()
        thread = threading.Thread(target=service.run_test, args=(test.id,))
        thread.daemon = True
        thread.start()
        
        messages.success(request, f'Test restarted for {test.url}.')
        return redirect('website_testing:detail', pk=test.pk)
    
    return redirect('website_testing:dashboard')


@login_required
def delete_test(request, pk):
    """Delete a test and all its results"""
    
    if request.method == 'POST':
        test = get_object_or_404(WebsiteTest, pk=pk, tested_by=request.user)
        url = test.url
        test.delete()
        
        messages.success(request, f'Test for {url} has been deleted.')
        return redirect('website_testing:dashboard')
    
    return redirect('website_testing:dashboard')


@login_required
def compare_tests(request):
    """Compare multiple test results"""
    
    test_ids = request.GET.getlist('test_id')
    if not test_ids:
        messages.error(request, 'Please select tests to compare.')
        return redirect('website_testing:dashboard')
    
    tests = WebsiteTest.objects.filter(
        pk__in=test_ids,
        tested_by=request.user,
        status='completed'
    ).prefetch_related(
        'performance', 'accessibility', 'seo', 'security', 'ux', 'errors'
    )
    
    if len(tests) < 2:
        messages.error(request, 'Please select at least 2 completed tests to compare.')
        return redirect('website_testing:dashboard')
    
    return render(request, 'website_testing/compare_tests.html', {
        'tests': tests,
    })


def public_report(request, pk):
    """Public report view (no login required)"""
    
    test = get_object_or_404(WebsiteTest, pk=pk, status='completed')
    
    # Only show public report if test was successful
    if test.status != 'completed':
        return render(request, 'website_testing/report_not_available.html')
    
    context = {
        'test': test,
        'performance': getattr(test, 'performance', None),
        'accessibility': getattr(test, 'accessibility', None),
        'seo': getattr(test, 'seo', None),
        'security': getattr(test, 'security', None),
        'ux': getattr(test, 'ux', None),
        'errors': getattr(test, 'errors', None),
        'is_public_view': True,
    }
    
    return render(request, 'website_testing/public_report.html', context)