from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from faker import Faker
import random

from django.contrib.auth.models import User
from schools.models import School
from employers.models import Employer
from teachers.models import Teacher
from jobs.models import Job
from applications.models import Application
from main.models import Subject, County, Constituency, EmploymentType, Specialization, Language, createCountynConstituencies

fake = Faker()


class Command(BaseCommand):
    help = 'Populate DB with synthetic data (schools, employers, teachers, jobs, applications, saves)'

    def add_arguments(self, parser):
        parser.add_argument('--jobs', type=int, default=400)
        parser.add_argument('--employers', type=int, default=30)
        parser.add_argument('--teachers', type=int, default=500)
        parser.add_argument('--schools', type=int, default=200)
        parser.add_argument('--applications', type=int, default=500)
        parser.add_argument('--saves', type=int, default=500)
        parser.add_argument('--seed', type=int, default=42)
        parser.add_argument('--reset', action='store_true', help='Delete previously seeded objects (those with username starting with seed_)')
        parser.add_argument('--dry-run', action='store_true', help='Do not commit changes to DB')

    def handle(self, *args, **options):
        random.seed(options['seed'])
        Faker.seed(options['seed'])

        jobs_count = options['jobs']
        employers_count = options['employers']
        teachers_count = options['teachers']
        schools_count = options['schools']
        applications_count = options['applications']
        saves_count = options['saves']
        dry_run = options['dry_run']
        reset = options['reset']

        self.stdout.write(self.style.WARNING('Starting population script'))

        # Prepare supporting data
        createCountynConstituencies()

        # Ensure some base data exists
        self._ensure_base_main_data()

        if reset:
            self._reset_seeded_data()

        if dry_run:
            self.stdout.write(self.style.WARNING('Dry run mode: changes will not be saved to DB'))

        with transaction.atomic():
            schools = self._create_schools(schools_count)
            employers = self._create_employers(employers_count, schools)
            teachers = self._create_teachers(teachers_count)
            jobs = self._create_jobs(jobs_count, employers)
            self._create_applications(applications_count, jobs, teachers)
            self._create_saves(saves_count, jobs, teachers)

            if dry_run:
                # roll back by raising an exception to prevent commit
                raise Exception('Dry run - rolling back')

        self.stdout.write(self.style.SUCCESS('Population complete'))

    def _ensure_base_main_data(self):
        # Create some subjects, employment types, specializations, languages if missing
        subjects = ['Mathematics', 'English', 'Biology', 'Chemistry', 'Physics', 'History', 'Geography', 'Art']
        for s in subjects:
            Subject.objects.get_or_create(title=s)

        employments = ['Full Time', 'Contract', 'B.O.M', 'P.T.A', 'Substitute']
        for e in employments:
            EmploymentType.objects.get_or_create(title=e)

        specializations = ['Guidance', 'ICT', 'Science', 'Languages', 'Sports']
        for sp in specializations:
            Specialization.objects.get_or_create(title=sp)

        languages = ['English', 'Swahili']
        for lg in languages:
            Language.objects.get_or_create(title=lg)

    def _reset_seeded_data(self):
        self.stdout.write('Removing previously seeded users (username starts with seed_)')
        User.objects.filter(username__startswith='seed_').delete()
        School.objects.filter(name__startswith='Seed School').delete()
        self.stdout.write('Removed prior seeded schools and users')

    def _create_schools(self, count):
        created = []
        for i in range(count):
            name = f'Seed School {i+1} {fake.company()}'
            school = School.objects.create(name=name)
            created.append(school)
        self.stdout.write(self.style.SUCCESS(f'Created {len(created)} schools'))
        return created

    def _create_employers(self, count, schools):
        created = []
        counties = list(County.objects.all())
        for i in range(count):
            username = f'seed_employer_{i+1}_{int(random.random()*10000)}'
            email = f'{username}@example.com'
            user = User.objects.create_user(username=username, email=email, password='password')
            school = schools[i] if i < len(schools) else random.choice(schools)
            location = random.choice(counties)
            employer = Employer.objects.create(user=user, school=school, employer_location=location, verified=random.choice([True, False]))
            created.append(employer)
        self.stdout.write(self.style.SUCCESS(f'Created {len(created)} employers'))
        return created

    def _create_teachers(self, count):
        created = []
        subjects = list(Subject.objects.all())
        counties = list(County.objects.all())
        for i in range(count):
            username = f'seed_teacher_{i+1}_{int(random.random()*10000)}'
            email = f'{username}@example.com'
            user = User.objects.create_user(username=username, email=email, password='password')
            teacher = Teacher.objects.create(user=user, phone=fake.phone_number(), email=email, grade_levels='8-4-4')
            # assign subjects
            chosen = random.sample(subjects, k=min(3, len(subjects)))
            teacher.subjects_taught.set(chosen)
            teacher.teacher_subjects.set(chosen)
            # preferred locations
            chosen_counties = random.sample(counties, k=min(2, len(counties)))
            teacher.preferred_locations.set(chosen_counties)
            created.append(teacher)
        self.stdout.write(self.style.SUCCESS(f'Created {len(created)} teachers'))
        return created

    def _create_jobs(self, count, employers):
        created = []
        counties = list(County.objects.all())
        for i in range(count):
            employer = random.choice(employers)
            job_title = f'{fake.job()} - {fake.word().capitalize()} Teacher'
            description = fake.sentence(nb_words=20)
            county = random.choice(counties)
            # pick a constituency that belongs to this county if possible
            constituencies = list(Constituency.objects.filter(county=county))
            if constituencies:
                constituency = random.choice(constituencies)
            else:
                constituency = Constituency.objects.order_by('?').first()

            job = Job.objects.create(
                employer=employer,
                job_title=job_title,
                job_description=description,
                grade_level=random.choice(['Primary','J.S.S','High School']),
                min_experience=random.randint(0,5),
                tsc_required=random.choice([True, False]),
                salary_min=random.randint(20000,40000),
                salary_max=random.randint(50000,100000),
                location=fake.city(),
                county=county,
                constituency=constituency,
                application_deadline=timezone.now() + timezone.timedelta(days=random.randint(7,60))
            )
            # set many2many subjects
            subjects = list(Subject.objects.all())
            chosen = random.sample(subjects, k=min(3, len(subjects)))
            job.subjects_required.set(chosen)
            # random booleans
            job.is_active = True
            job.save()
            created.append(job)
        self.stdout.write(self.style.SUCCESS(f'Created {len(created)} jobs'))
        return created

    def _create_applications(self, count, jobs, teachers):
        created = []
        for i in range(count):
            job = random.choice(jobs)
            teacher = random.choice(teachers)
            approver = job.employer
            # avoid duplicate application by same teacher-job
            if Application.objects.filter(job=job, teacher=teacher).exists():
                continue
            app = Application.objects.create(job=job, teacher=teacher, approver=approver, status=random.choice(['Applied','Shortlisted','Interview','Rejected']))
            # update job counters
            job.total_applications = Application.objects.filter(job=job).count()
            job.save()
            # also add to teacher.applied_jobs M2M for consistency
            teacher.applied_jobs.add(job)
            created.append(app)
        self.stdout.write(self.style.SUCCESS(f'Created {len(created)} applications'))
        return created

    def _create_saves(self, count, jobs, teachers):
        created = 0
        for i in range(count):
            job = random.choice(jobs)
            teacher = random.choice(teachers)
            if teacher.saved_jobs.filter(id=job.id).exists():
                continue
            teacher.saved_jobs.add(job)
            job.saves = teacher.saved_jobs.filter(id=job.id).count() if False else job.saves + 1
            job.save()
            created += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created} saves'))
        return created
