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
- Platform: Heroku
- Steps to clone, install, migrate, create superuser, runserver
- Steps to configure environment variables and deploy
- Add Heroku Postgres, run migrations, set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`

_Detailed steps will be written during the build so assessors can reproduce deployment._

## Testing
- Manual testing plan mapped to the user stories above.
- HTML/CSS/JS validators and Lighthouse.
- Cross-browser and responsive checks.
- Bug log with reproduction steps and fixes.
- (Optional) Unit tests for models or views.

## Version Control
- Git and GitHub used from project start.
- Small, atomic commits with meaningful messages.

## Credits
- List and link to any code snippets, tutorials, images, or media used.
- Each image or media asset attributed to its specific owner.
