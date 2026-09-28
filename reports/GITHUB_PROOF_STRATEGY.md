# GitHub Upload Strategy & Proof-Building Plan

## Repository
- **Name:** `Cloud-Based-Assignment-Submission-Portal`
- **Description:** "Cloud-based student assignment submission and feedback
  platform featuring role-based authentication, cloud database
  integration, object storage, assignment management, secure file
  submission, grading, and feedback workflows."
- **Topics:** cloud-computing, edtech, python, flask, fastapi, react,
  cloud-storage, firebase, database, rest-api, full-stack, authentication

## Git Commands
```bash
cd Cloud-Assignment-Submission-Portal
git init
git add .
git commit -m "Initialize cloud assignment portal"
git branch -M main
git remote add origin https://github.com/<your-username>/Cloud-Based-Assignment-Submission-Portal.git
git push -u origin main
```

## Recommended Commit History (one per development session)
1. `Initialize cloud assignment portal`
2. `Create frontend and backend architecture`
3. `Implement authentication and role management`
4. `Add assignment management module`
5. `Integrate cloud database`
6. `Implement cloud file storage`
7. `Add student assignment submission workflow`
8. `Implement deadline validation`
9. `Add teacher grading and feedback`
10. `Build student and teacher dashboards`
11. `Add security and authorization`
12. `Add automated tests`
13. `Deploy application to cloud`
14. `Complete README and documentation`

## 13-Day Proof-Building Plan
| Day | Focus | Files touched | Screenshot to capture |
|---|---|---|---|
| 1 | Architecture + repo init | `README.md`, folder structure | Folder structure, architecture diagram |
| 2 | Authentication | `auth_routes.py`, `auth_utils.py` | Login page, register page |
| 3 | Role-based access | `role_required()` usage across routes | Authorization error demo (403) |
| 4 | Assignment management | `assignment_routes.py`, `assignments.html` | Assignment creation form, assignment list |
| 5 | Cloud database | `models.py`, `database.py` | Database record via a DB browser |
| 6 | Cloud object storage | `storage_service.py` | Local storage folder structure |
| 7 | Student submission | `submission_routes.py` (submit), upload UI | Successful upload confirmation |
| 8 | Deadline logic | Deadline comparison code | On-time vs late submission demo |
| 9 | Teacher feedback/grading | Grade endpoint, `submissions.html` | Marks + feedback screen |
| 10 | Dashboards | `dashboard_routes.py`, dashboard pages | Student dashboard, teacher dashboard |
| 11 | Testing & security | `tests/`, `docs/SECURITY.md` | Automated tests passing (terminal output) |
| 12 | Cloud deployment | `docs/DEPLOYMENT.md`, live deploy | Live application URL |
| 13 | README/documentation | `README.md`, `docs/`, `reports/` | README preview on GitHub |

## Screenshot Checklist (suggested filenames)
```
01_project_folder_structure.png
02_architecture_diagram.png
03_login_page.png
04_student_registration.png
05_teacher_dashboard.png
06_assignment_creation.png
07_student_dashboard.png
08_assignment_list.png
09_assignment_details.png
10_file_selection_screen.png
11_successful_upload.png
12_cloud_storage_file.png
13_database_submission_record.png
14_on_time_submission_status.png
15_late_submission_demo.png
16_teacher_submission_list.png
17_teacher_reviewing_file.png
18_marks_and_feedback.png
19_student_feedback_page.png
20_authorization_error_demo.png
21_api_response_sample.png
22_automated_tests_passing.png
23_cloud_deployment_dashboard.png
24_live_application.png
25_github_commits.png
26_github_repository.png
27_readme_preview.png
```
