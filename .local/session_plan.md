# Objective
Add React JSX frontend + Django REST API to Kenya Teaching Vacancies project.

# Tasks

### T001: Build Django REST API endpoints
- **Blocked By**: []
- **Details**:
  - Create serializers for Job, Teacher, School, Application, User
  - Build ViewSets/APIViews: auth (login/logout/register/me), jobs (list/detail/save/apply/trending), applications, teacher profile, schools
  - Wire up api/urls.py with all routes
  - Enable CORS for localhost:5000
  - Files: api/serializers.py, api/views.py, api/urls.py, kenya_teaching_vacancies/settings.py

### T002: Scaffold React + Vite frontend
- **Blocked By**: []
- **Details**:
  - Create frontend/ directory with Vite React JSX project
  - Install react-router-dom, axios
  - Configure Vite proxy to Django at :8000
  - Set up folder structure: components/, pages/, hooks/, utils/
  - Files: frontend/package.json, frontend/vite.config.js, frontend/src/

### T003: Build React pages and components
- **Blocked By**: [T002]
- **Details**:
  - Login, Signup, JobFeed, JobDetail, TeacherProfile, MyApplications, SavedJobs, Schools, PostJob pages
  - NavBar, JobCard, SideBar, Trending components
  - CSS/styling matching existing macglass theme
  - Files: frontend/src/pages/, frontend/src/components/

### T004: Connect frontend to API and configure workflows
- **Blocked By**: [T001, T003]
- **Details**:
  - Wire all pages to real API endpoints
  - Configure "Start application" workflow to run React at :5000
  - Add "Django API" workflow at :8000
  - Test full integration
