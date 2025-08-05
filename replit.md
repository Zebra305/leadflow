# Lead Outreach Manager

## Overview

This is a Flask-based lead outreach management system designed to automate and track email/messaging campaigns with leads. The application enforces a 2-day delay rule between messages to prevent spam-like behavior and manages multi-stage follow-up sequences. It provides a dashboard for managing outreach campaigns, tracking message status, and searching through leads.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework
- **Flask**: Chosen as the main web framework for its simplicity and flexibility in building a straightforward CRUD application
- **SQLAlchemy**: Used as the ORM for database interactions, providing a clean abstraction layer over raw SQL
- **Jinja2 Templates**: Standard Flask templating engine for server-side rendering

### Database Design
- **PostgreSQL**: Primary database for storing lead information and outreach tracking
- **Single Table Architecture**: The `Lead` model contains all necessary fields including contact info, outreach messages, and tracking status
- **Follow-up Sequence Management**: Uses numbered columns (follow_up_0 through follow_up_5) with corresponding sent/replied boolean flags

### Frontend Architecture
- **Server-Side Rendering**: Traditional multi-page application using Flask templates
- **Bootstrap 5**: CSS framework for responsive design and dark theme support
- **Font Awesome**: Icon library for consistent UI elements
- **Minimal JavaScript**: Basic client-side functionality for copy-to-clipboard and form interactions

### Business Logic
- **2-Day Rule Enforcement**: Prevents sending messages too frequently by checking time delays between outreach attempts
- **Multi-Stage Sequences**: Supports initial outreach plus 6 follow-up messages with individual tracking
- **Status Tracking**: Monitors sent/replied status for each message in the sequence

### Application Structure
- **Single Module Design**: Core functionality split across `app.py`, `models.py`, and `routes.py` for clear separation of concerns
- **Environment Configuration**: Database credentials and secrets managed through environment variables
- **Connection Pooling**: SQLAlchemy configured with connection recycling and health checks

## External Dependencies

### Database
- **PostgreSQL**: Remote database hosted at 69.62.114.108 with readonly user access
- Database name: `n8n_outreach`
- Connection pooling with 300-second recycle time

### Frontend Libraries
- **Bootstrap 5**: CSS framework via CDN (Replit agent dark theme)
- **Font Awesome 6**: Icon library via CDN
- **No JavaScript frameworks**: Vanilla JS for minimal client-side functionality

### Python Packages
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Werkzeug**: WSGI utilities and proxy fix middleware
- **Standard library**: datetime, logging, os for core functionality

### Development Environment
- **Replit hosting**: Configured to run on host 0.0.0.0:5000
- **Debug mode**: Enabled for development
- **Proxy middleware**: ProxyFix for handling headers in hosted environment