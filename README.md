# Clarova Crisis Comms & AI Training Platform (MVP)

## Overview
Clarova is a Django-based SaaS platform that helps public sector and charity communications teams respond quickly and responsibly in a crisis, and provides embedded AI governance training. The MVP is designed to meet the Code Institute Full Stack assessment criteria.

## Project Goals
- Enable teams to prepare crisis scenarios, generate drafts from templates, and route items for approval with an audit trail.
- Provide role-based access and training modules on AI governance and crisis communications.
- Use Stripe (test mode) to unlock premium features and training content.

## User Experience (UX)
Documented using the 5 planes. Include your reasoning and design choices at each stage.

### 1. Strategy (User and Business Goals)
**Target users:** public sector and charity comms teams; approvers; executives; learners.  
**Business goals:** recurring subscription income, trusted training resource, governance-ready workflows.

### 2. Scope (User Stories)
- As a new user, I want to register an account for my organisation so that my team can access the platform securely.
- As a new user, I want to create my first crisis scenario so I can prepare for incidents.
- As a new user, I want to access a free training module so I can understand the basics before upgrading.
- As a new user, I want to pay via Stripe to unlock AI drafting and the full training library.

- As a returning user, I want to see my active crisis scenarios so I can continue my work.
- As a returning user, I want to edit a template to reflect new policy changes.
- As a returning user, I want to complete a training quiz to test my knowledge.
- As a returning user, I want to see approval requests for my sign-off.

- As a frequent user, I want to duplicate a previous scenario to save time.
- As a frequent user, I want to track approval history for compliance.
- As a frequent user, I want to update my subscription or payment details via Stripe.

### 3. Structure (Information Architecture)
- Global navigation: Home, Scenarios, Templates, Drafts, Approvals, Training, Billing, Account.
- Breadcrumbs inside Scenarios and Training.
- Entitlements used to gate paid features after Stripe success.

### 4. Skeleton (Wireframes)
Provide links or embedded images for mobile, tablet, and desktop for each major page:
- Home/Dashboard
- Scenarios (list/detail)
- Templates (list/detail/edit)
- Draft editor and submit for approval
- Approvals (review/decision)
- Training (module list, lesson, quiz)
- Billing (checkout status)

### 5. Surface (UI Design)
- Clean, accessible layout using modern HTML and CSS (validator friendly).
- Avoid trailing slashes in URLs.
- Colour and typography selected for clarity and accessibility.

## Features
- Registration and login (django-allauth).  
- Scenario builder, Templates, Drafts with submit for approval.  
- Approval workflow with decisions and comments.  
- Training modules with lessons and a quiz that persists results.  
- Stripe test checkout and webhooks that unlock entitlements.  
- Light custom JavaScript for the Draft editor and Scenario builder.

### Future Enhancements
- AI-assisted drafting integration.
- Performance analytics and exportable audit logs.
- Team notifications and activity feed.

## Data Model Overview
Core models (subject to refinement during build):
- Organisation, UserProfile, Subscription, Entitlement
- Scenario, Template, Draft, Approval, ResponseLog
- TrainingModule, Lesson, Quiz, QuizResult

_A diagram will be added here in the README once finalised._

## Technologies
- HTML, CSS, JavaScript, Python, Django
- PostgreSQL (local and Heroku)
- Stripe (test mode)
- Bootstrap or Tailwind for layout

## Libraries and APIs
- django-allauth (authentication)
- dj-database-url, gunicorn, whitenoise (deployment)
- stripe (server-side SDK)
- (Optional) OpenAI API for AI-assisted drafting (can be stubbed)

## Security
- Environment variables for secrets. No keys in repo.
- DEBUG=False in production. Secure cookies and SSL redirect.
- CSRF protections and role-based permissions.

## Deployment

# from project root
source .venv/Scripts/activate            # Windows Git Bash (PowerShell: .\.venv\Scripts\Activate.ps1)
python manage.py migrate
python manage.py runserver
# open http://127.0.0.1:8000

## Development Log

### Environment setup
- Created `.venv` and installed dependencies: Django 3.2.25, django-allauth 0.63.6, dj-database-url, whitenoise, stripe, python-dotenv.
- Generated `requirements.txt`.

### Django skeleton
- Project package: `clarova`.
- App: `core`.
- Template structure: project-level `templates/` with `base.html`, `account/login.html`, `account/signup.html`, `core/home.html`.
- `TEMPLATES` configured with `DIRS = [BASE_DIR / 'templates']` and `APP_DIRS = True`.

### Authentication (django-allauth)
- Installed and configured `allauth` with `SITE_ID = 1`.
- URL include at `/accounts/`.
- Base navigation uses `{% url 'account_login' %}`, `{% url 'account_signup' %}`, `{% url 'account_logout' %}`.

### Errors encountered and fixes
- **Issue:** `ImproperlyConfigured: allauth.account.middleware.AccountMiddleware must be added`  
  **Fix:** Added `'allauth.account.middleware.AccountMiddleware'` after `'django.contrib.auth.middleware.AuthenticationMiddleware'` in `MIDDLEWARE`.

- **Issue:** Route showed `/accountslogin/` due to missing slash in include prefix  
  **Fix:** Used `path('accounts/', include('allauth.urls'))` and updated nav links to `{% url 'account_login' %}`, `{% url 'account_signup' %}`, `{% url 'account_logout' %}`.


### Error : Admin 500 Error after `DEBUG=False`
- **Problem**: Admin page (`/admin/`) returned a 500 error when `DEBUG` was set to `False`. Logs showed `No directory at: /app/staticfiles/`.
- **Cause**: Static files (including Django admin CSS/JS) were not being collected or served in production.
- **Solution**:  
  - Verified `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` included the Heroku domains.  
  - Ran `heroku run python manage.py collectstatic --noinput` to ensure admin static files were copied to `/app/staticfiles`.  
  - Confirmed `WhiteNoise` was enabled with `STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"`.  
  - Triggered a rebuild with `git commit --allow-empty -m "Trigger Heroku rebuild for collectstatic"` followed by `git push heroku main`.  
- **Fix**: Admin now loads correctly with static files served by WhiteNoise.

---

### Error : `Nonexistent flag: --noinput` on Heroku release
- **Problem**: Deployment failed with `Error: Nonexistent flag: --noinput`.
- **Cause**: The `--noinput` flag was mistakenly placed in the Procfile under the `release:` command. This flag is only valid for `manage.py` commands, not `heroku release`.
- **Solution**: Removed the incorrect flag from the Procfile. Left `--noinput` only in the `collectstatic` step where it belongs.  
- **Fix**: Release phase runs cleanly without crashing dynos.

---

### Error : Static Files Not Found at Runtime
- **Problem**: Even after running collectstatic, hitting URLs like `/static/admin/css/base.css` returned 404 errors.
- **Cause**: The Heroku config var `DISABLE_COLLECTSTATIC` was set (from earlier debugging), which stopped Django from collecting static files during build.
- **Solution**:  
  - Checked config with `heroku config:get DISABLE_COLLECTSTATIC`.  
  - Unset the variable using `heroku config:unset DISABLE_COLLECTSTATIC -a clarova-mvp-hlj`.  
  - Re-ran deployment to ensure `collectstatic` executed automatically.  
- **Fix**: Admin static files now available at `/static/admin/...`.

---

### Error: Heroku Deployment Not Updating
- **Problem**: Changes pushed locally were not reflected on Heroku.
- **Cause**: Heroku app was linked to GitHub auto-deploys, but manual `git push heroku main` was not updating due to stale cache and mixed remote usage.
- **Solution**:  
  - Verified remotes with `git remote -v`.  
  - Re-pushed directly to Heroku using `git push heroku main`.  
  - Confirmed new slug build appeared in Heroku dashboard.  
- **Fix**: Latest code and static assets deployed successfully.

---

- Platform: Heroku
- Steps to clone, install, migrate, create superuser, runserver
- Steps to configure environment variables and deploy
- Add Heroku Postgres, run migrations, set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`

_Detailed steps will be written during the build so assessors can reproduce deployment._

## Testing

### Manual testing plan (mapped to user stories)

For each test, record **Steps**, **Expected**, **Actual**, **Result** (Pass/Fail), and attach a **Screenshot**.

| Test ID | Scenario | Steps | Expected | Actual | Result | Screenshot |
|---|---|---|---|---|---|---|
| T-001 | New user — sign up | Visit `/accounts/signup/`, submit form with valid data | Account created; redirect to Home |  |  |  |
| T-002 | Returning user — login | Visit `/accounts/login/`, submit valid credentials | Redirect to Home; nav shows **Logout** |  |  |  |
| T-003 | Navigation | Click Home, Login, Sign up, Logout | All links work; no 404s or broken links |  |  |  |
| T-004 | Templates loading | Load Home page | `core/home.html` rendered via `base.html` |  |  |  |

### Validators and tools
- W3C HTML and CSS validators  
- Lighthouse (Performance, Best Practices, Accessibility)  
- Cross-browser and responsive checks (desktop, tablet, mobile)

- Manual testing plan mapped to the user stories above.
- HTML/CSS/JS validators and Lighthouse.
- Cross-browser and responsive checks.

- (Optional) Unit tests for models or views.
### Bug log (ongoing)

- **Issue:** `allauth.account.middleware.AccountMiddleware` missing  
  **Fix:** Add `'allauth.account.middleware.AccountMiddleware'` after `'django.contrib.auth.middleware.AuthenticationMiddleware'` in `MIDDLEWARE`.

- **Issue:** Missing slash in accounts include caused `/accountslogin/`  
  **Fix:** Use `path('accounts/', include('allauth.urls'))` and update nav links to `{% url 'account_login' %}`, `{% url 'account_signup' %}`, `{% url 'account_logout' %}`.


## Version Control
- Git and GitHub used from project start.
- Small, atomic commits with meaningful messages.

## Credits
- List and link to any code snippets, tutorials, images, or media used.
- Each image or media asset attributed to its specific owner.

## Roadmap
- [x] Set up Django project & apps  
- [x ] Configure PostgreSQL locally and on Heroku  
- [ ] Implement authentication (django-allauth) with roles  
- [ ] Build Scenario, Template, Draft models & CRUD  
- [ ] Add approval workflow with audit logs  
- [ ] Implement Training modules & quiz system  
- [ ] Integrate Stripe checkout & entitlements  
- [ ] Add custom JavaScript features  
- [ ] Complete README with deployment and testing sections  
- [ ] Final Heroku deploy with security settings  

## Screenshots to Capture for README
- Registration and login pages  
- Dashboard or home page after login  
- Create Scenario form  
- Template list & edit screen  
- Draft editor showing AI-assisted content (or placeholder)  
- Approval page with decision form  
- Training module list & lesson view  
- Stripe checkout page (test mode)  
- Stripe payment success screen  
- Any custom JavaScript feature in action  
- Mobile, tablet, and desktop views (for responsiveness section)  

