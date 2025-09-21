from django.core.management.base import BaseCommand
from workbench.website_testing.models import WebsiteTest
from workbench.website_testing.services import WebsiteTestingService


class Command(BaseCommand):
    help = 'Run pending website tests'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-id',
            type=int,
            help='Run a specific test by ID',
        )
        parser.add_argument(
            '--max-tests',
            type=int,
            default=10,
            help='Maximum number of tests to run (default: 10)',
        )

    def handle(self, *args, **options):
        service = WebsiteTestingService()
        
        if options['test_id']:
            # Run specific test
            test_id = options['test_id']
            self.stdout.write(f'Running test {test_id}...')
            
            try:
                test = WebsiteTest.objects.get(id=test_id)
                success = service.run_test(test_id)
                
                if success:
                    self.stdout.write(
                        self.style.SUCCESS(f'Test {test_id} completed successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'Test {test_id} failed: {test.error_message}')
                    )
            except WebsiteTest.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Test {test_id} not found')
                )
        else:
            # Run pending tests
            pending_tests = WebsiteTest.objects.filter(
                status='pending'
            ).order_by('created_at')[:options['max_tests']]
            
            if not pending_tests:
                self.stdout.write('No pending tests found')
                return
            
            self.stdout.write(f'Found {len(pending_tests)} pending tests')
            
            for test in pending_tests:
                self.stdout.write(f'Running test {test.id} for {test.url}...')
                
                success = service.run_test(test.id)
                
                if success:
                    self.stdout.write(
                        self.style.SUCCESS(f'Test {test.id} completed successfully')
                    )
                else:
                    test.refresh_from_db()
                    self.stdout.write(
                        self.style.ERROR(f'Test {test.id} failed: {test.error_message}')
                    )