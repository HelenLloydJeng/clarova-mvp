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

### 4. Skeleton (Wireframes) (Text-Based)

### **Home**

```
 -----------------------------------------------------
| LOGO           | Home | Dashboard | Scenarios | Training | Login |
 -----------------------------------------------------
|                    HERO SECTION                     |
|  Headline: "AI Crisis Comms Training"               |
|  Subheading: "Respond quickly and responsibly"      |
|  [Start Learning]   [Try Scenarios]                 |
 -----------------------------------------------------
| Footer: Links, copyright                            |
 -----------------------------------------------------
```
---
### **Dashboard**
```
 -----------------------------------------------------
| LOGO | Home | Dashboard | Scenarios | Training | Logout |
 -----------------------------------------------------
|                DASHBOARD HERO                      |
|  Welcome, [username]                               |
|  Buttons: [Create Scenario] [Explore Training]     |
 -----------------------------------------------------
| STATUS BOXES                                       |
|  - Scenarios: [count]                              |
|  - Training modules owned: [count]                 |
 -----------------------------------------------------
```
---
### **Scenarios**

**List view**
```
 -----------------------------------------------------
| Scenario Title  | Created: Date | [View] [Edit] [Delete] |
| Scenario Title  | Created: Date | [View] [Edit] [Delete] |
 -----------------------------------------------------
[+ New Scenario]
```
**Detail view**

```
 -----------------------------------------------------
| Scenario Title                                     |
| Description...                                     |
 -----------------------------------------------------
[Edit]  [Delete]  [Back to List]
```

**Form view**
```
 -----------------------------------------------------
| New/Edit Scenario                                  |
 -----------------------------------------------------
| Title: [___________]                               |
| Description: [___________________________]         |
 -----------------------------------------------------
[Save]   [Cancel]
```

---
### **Training**

**List view**
```
 -----------------------------------------------------
| Module Card:                                       |
|  Title: Media Monitoring & Rapid Response          |
|  Short desc...                                     |
|  [Preview Lesson]   [Buy with Stripe]              |
 -----------------------------------------------------
| Module Card: (Owned)                               |
|  Title: Crisis Simulation Lab                      |
|  Short desc...                                     |
|  [View Lessons]                                    |
 -----------------------------------------------------
```
**Detail view**
```
 -----------------------------------------------------
| Module Title                                       |
| Description...                                     |
 -----------------------------------------------------
- Preview Lesson (if not purchased)                  |
- Full lessons list (if purchased)                   |
 -----------------------------------------------------
[Buy with Stripe] or [Owned]
```

**Success/Cancel**
```
SUCCESS: "Payment successful. Module unlocked."
CANCEL: "Payment cancelled. Try again later."
```
---
### **Auth (Login/Signup/Logout)**
```
 -----------------------------------------------------
| LOGIN                                              |
| Username/Email: [________]                         |
| Password:      [________]                          |
 -----------------------------------------------------
[Login]  [Back to Home]

 -----------------------------------------------------
| SIGN UP                                            |
| Username:  [________]                              |
| Email:     [________]                              |
| Password:  [________]                              |
| Confirm:   [________]                              |
 -----------------------------------------------------
[Create Account]   [Back to Home]

 -----------------------------------------------------
| LOGOUT                                             |
| "Are you sure you want to logout?"                 |
 -----------------------------------------------------
[Logout]   [Back to Home]
```
---
### **Error Pages**

```
403 Forbidden: "You don’t have permission." [Home]
404 Not Found: "Page not found." [Home]
500 Server Error: "Something went wrong." [Home]
```
---
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
## Code Structure & Logic

* **Accounts app**

* Extended Django Allauth with `Organisation` and `UserProfile` models.
* Used Django signals to automatically create a profile when a user registers.
* Custom view `/team/org` lets logged-in users create their Organisation, validated against duplicates.

* **Scenarios app**

* Implemented full CRUD with class-based views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`).
* Querysets filtered by `request.user` so each user only sees their own scenarios.
* `ScenarioForm` includes validation to enforce unique titles per user.

* **Training app**

* `Module` and `Lesson` models seeded with starter content.
* `Entitlement` model checks if a user owns a module (purchased via Stripe).
* Views control lesson access: preview lesson always available, full content only if Entitlement exists.

* **Stripe integration**

* `checkout_create` view creates a Stripe Checkout Session in test mode.
* On success return (`/training/success`), Entitlement is granted to the user.
* Cancel return (`/training/cancel`) shows preview state unchanged.

* **Core app**

* Simple `home` and `dashboard` views with hero CTAs.
* Dashboard personalised with user info and scenario/training stats.
---

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
### // Error: `NoReverseMatch` for `'core:dashboard'` in `base.html`
- **Problem**: Home raised 500: “Reverse for 'dashboard' not found”.
- **Cause**: `dashboard` URL name didn’t exist.
- **Solution**: Add `path("dashboard/", views.dashboard, name="dashboard")` in `core/urls.py` and ensure view exists.
- **Fix**: Home renders; Dashboard link works.

### // Error: `404 Not Found` for `/training/`
- **Problem**: `/training/` returned 404.
- **Cause**: Training URLconf not included at project level.
- **Solution**: Add `path("training/", include("training.urls"))` in `clarova/urls.py` and `app_name = "training"` in `training/urls.py`.
- **Fix**: Training list reachable.

### // Error: `TemplateSyntaxError` — Invalid block tag `'else'`
- **Problem**: `/training/<id>/` 500 with “Invalid block tag 'else'”.
- **Cause**: Used `{% else %}` where `{% empty %}` (for loops) or `endblock` (for blocks) was required.
- **Solution**: Replace `{% else %}` with `{% empty %}` in `templates/training/list.html` and remove stray block `else`.
- **Fix**: Templates render.

### // Error: `NoReverseMatch` for `training:buy` on Module detail
- **Problem**: Opening `/training/<id>/` raised “Reverse for 'buy' not found”.
- **Cause**: Missing/misnamed URL pattern.
- **Solution**: In `training/urls.py` add:
  - `path("buy/<int:pk>/", views.checkout_create, name="buy")`
  - Ensure template uses `{% url 'training:buy' module.pk %}` and `app_name = "training"`.
- **Fix**: Buy button routes to Stripe Checkout.

### // Error: 404 for `/static/app.css` and missing favicon
- **Problem**: Logs showed 404s for `/static/app.css` and `/static/favicon.ico`.
- **Cause**: Files referenced in `base.html` didn’t exist in `static/`.
- **Solution**: Add `static/app.css` and `static/favicon.ico`; redeploy so Whitenoise serves them.
- **Fix**: No more static 404s; base styles applied.

### // Error: Heroku CLI — “invalid. Must be in the format FOO=bar.”
- **Problem**: Failed to set Stripe keys via CLI.
- **Cause**: App name passed incorrectly; missing `-a` flag.
- **Solution**:
  ```bash
  heroku config:set STRIPE_SECRET_KEY=sk_test_... -a clarova-mvp-hlj
  heroku config:set STRIPE_PUBLISHABLE_KEY=pk_test_... -a clarova-mvp-hlj
  ---

## Bug log (ongoing)

### 2025-09-07 — `/training/` returned 404 (Not Found)
- **Symptoms:** Navigating to `/training/` showed “Not Found.”
- **Cause:** Project URLConf was missing the include for the `training` app.
- **Fix:** Added the route to the project urls.
  ```python
  # clarova/urls.py
  path('training/', include('training.urls')),


- Platform: Heroku
- Steps to clone, install, migrate, create superuser, runserver
- Steps to configure environment variables and deploy
- Add Heroku Postgres, run migrations, set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`


## Testing

### Manual testing plan (mapped to user stories)

| Test ID | Scenario | Steps | Expected | Actual | Result | Screenshot |
|---|---|---|---|---|---|---|
| T-001 | New user — sign up | Visit `/accounts/signup/`, submit valid data | Account created; redirect to Home |  |  | ![signup](static/images/signup_screenshot.jpeg) |
| T-002 | Returning user — login | Visit `/accounts/login/`, submit valid credentials | Redirect to Home; nav shows **Logout** |  |  | ![login]() |
| T-003 | Logout flow | Click **Logout** in nav | Redirect to Home; nav shows **Login/Sign up** |  |  | ![logout]() |
| T-004 | Navigation | Click Home, Login, Sign up, Logout | All links work; no 404s |  |  | ![nav](static/images/login_screenshot.jpeg) |
| T-005 | Templates loading | Load Home page | `core/home.html` rendered via `base.html` |  |  | ![home](static/images/homepage_screenshot.jpeg) |
| T-006 | 403 Forbidden page | Visit a restricted URL when not authorised | Custom **403** template renders; helpful message |  |  | ![403](static/images/403_screenshot.jpeg) |
| T-007 | 404 Not Found page | Visit a non-existent URL | Custom **404** template renders; link back to Home |  |  | ![404](static/images/404_screenshot.jpeg) |
| T-008 | 500 Server Error page | Trigger server error in dev (temporary view) | Custom **500** template renders; support message |  |  | ![500](static/images/500_screenshot.jpeg) |
| T-009 | Scenarios — list | Visit `/scenarios` | List shows only the logged-in user’s scenarios |  |  | ![scenarios list]() |
| T-010 | Scenarios — create | `/scenarios/create` submit valid form | Scenario saved; redirect to detail; success message |  |  |  |![scenario edit](static/images/new_scenario.jpeg) 
| T-011 | Scenarios — edit | Open a scenario; click **Edit**; submit changes | Changes saved; redirect to detail |  |  | ![scenario edit](static/images/screenshot-scenarios.png) |
| T-012 | Scenarios — delete | Open a scenario; **Delete**; confirm | Scenario removed; redirect to list |  |  | ![scenario delete](static/images/scenario_delete.jpeg) |
| T-013 | Training — list | Visit `/training` | Modules listed with **Buy** buttons for paid items |  |  | ![training list]() |
| T-014 | Stripe — checkout create | Click **Buy** on a paid training | Redirects to Stripe Checkout in test mode |  |  | ![stripe checkout](static/images/stripe_checkout_screenshot.jpeg) |
| T-015 | Stripe — success | Complete test payment | Redirect to `/training/success`; entitlement created |  |  | ![stripe success](static/images/stripe_dashboard.jpeg) |
| T-016 | Stripe — cancel | Cancel at Stripe | Redirect to `/training/cancel`; no entitlement |  |  | ![stripe cancel]() |
| T-017 | Access control | Visit `/scenarios/create` when logged out | Redirect to login; after login, return to create |  |  | ![login redirect]() |

### Validators and tools
- W3C HTML and CSS validators  
- Lighthouse (Performance, Best Practices, Accessibility)  
- Cross-browser and responsive checks (desktop, tablet, mobile)

- Manual testing plan mapped to the user stories above.
- HTML/CSS/JS validators and Lighthouse.
- Cross-browser and responsive checks.
git push origing main
-Unit tests for models or views.
### Bug log (ongoing)

- **Issue:** `allauth.account.middleware.AccountMiddleware` missing  
  **Fix:** Add `'allauth.account.middleware.AccountMiddleware'` after `'django.contrib.auth.middleware.AuthenticationMiddleware'` in `MIDDLEWARE`.

- **Issue:** Missing slash in accounts include caused `/accountslogin/`  
  **Fix:** Use `path('accounts/', include('allauth.urls'))` and update nav links to `{% url 'account_login' %}`, `{% url 'account_signup' %}`, `{% url 'account_logout' %}`.
  ---
  ## // Stripe (MVP)

### // How it works
- **Keys**: Reads `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` from environment (`.env` locally; Heroku Config Vars in production).
- **Flow**:
  1. Open Module detail (`/training/<id>/`).
  2. Click **Buy** → POST to `training:buy` → creates a **Stripe Checkout Session** and redirects to Stripe.
  3. Success returns to `training:success?session_id=...`; app verifies `payment_status == "paid"` and grants an **Entitlement**.
  4. Cancel returns to the Module page.

### // Routes
- `training:buy` → `/training/buy/<pk>/` (POST)  
- `training:success` → `/training/success/` (GET)  
- `training:cancel` → `/training/cancel/` (GET)

### // Test card
- **Card**: `4242 4242 4242 4242`  
- **Expiry**: any *future* month/year  
- **CVC**: any 3 digits  
- **Postcode**: any

### // Expected after success
- Redirect to **Success** page.  
- Module page shows **“You own this module.”** and full lessons list.  
- Training list shows **(Owned)** next to the purchased module.
---

## // QA: Stripe Checkout (Test Evidence)

### // Preconditions
- **Keys** set: `STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY` (test mode).
- **Module** exists with a non-zero `price_cents` (e.g., £15.00 → `1500`).
- **User** logged in and has an email on their profile (used by Stripe).
- **Routes** present:
  - `training:buy` → `/training/buy/<pk>/` (POST)
  - `training:success` → `/training/success/`
  - `training:cancel` → `/training/cancel/`

### // Happy path (purchase succeeds)
1. Visit **Training → Module detail** (`/training/<id>/`).
2. Click **Buy with Stripe** (POST to `training:buy`).
3. Browser redirects to **checkout.stripe.com** showing the module title and correct price.
4. Enter **test card** `4242 4242 4242 4242`, any **future** expiry, any **CVC**, any **postcode**.
5. Complete payment → redirected to **/training/success?session_id=...**.
6. App verifies `payment_status == "paid"` and **creates Entitlement** for the user.
7. Returning to the Module page shows **“You own this module.”** and **all lessons unlocked**.
8. Training list displays **(Owned)** for the purchased module.

### // Cancel path (no purchase)
- On Stripe Checkout, click **Cancel** / back.
- User is returned to module page; still **preview only**.
- **No Entitlement** is created.

### // Declined card (error path)
- Use Stripe decline test card `4000 0000 0000 0002`.
- Stripe shows **card declined**; payment not completed.
- Return to site: module remains **preview**; **no Entitlement**.

### // Verification steps
- **Admin check**: `Admin → Training → Entitlements` shows a new record for the user & module after a successful test payment.
- **UI check**:
  - Success page renders **“Payment success”**.
  - Module detail shows **Owned** state and **full lessons** list.
  - Training list shows **(Owned)** badge.
- **Logs** (optional):  
  `heroku logs --tail -a <app>` shows 302 to Stripe, then GET to `/training/success` without errors.

### // Notes
- This runs entirely in **Stripe test mode**; no real cards are charged.
- **MVP** verifies success on the return URL (no webhooks). For production, add a **Stripe webhook** to confirm payment server-side.
---

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

