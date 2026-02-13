# Nojudge AI Companion - Complete File Walkthrough

This document explains every file created in the Nojudge project, why it exists, and what it does.

---

## 📋 Configuration Files (Root Level)

### [package.json](file:///Users/monk/Nojudge/package.json)
**Purpose**: Node.js project configuration
- Defines project metadata (name, version, description)
- Lists all frontend dependencies (React, TypeScript, GSAP, etc.)
- Contains npm scripts: `dev` (start dev server), `build` (production build), `preview` (preview build)
- **Why needed**: Required for any Node.js/React project to manage dependencies and scripts

### [requirements.txt](file:///Users/monk/Nojudge/requirements.txt)
**Purpose**: Python dependencies list
- Lists all backend packages: Flask, SQLAlchemy, JWT, bcrypt, SocketIO, etc.
- **Why needed**: Allows easy installation of all Python dependencies with `pip install -r requirements.txt`

### [vite.config.ts](file:///Users/monk/Nojudge/vite.config.ts)
**Purpose**: Vite build tool configuration
- Configures React plugin for JSX/TSX support
- Sets up path aliases (`@/` points to `src/front/`)
- Configures dev server on port 5173
- Sets up proxy to forward `/api` requests to backend (port 5001)
- **Why needed**: Vite needs configuration to know how to build and serve the React app

### [tsconfig.json](file:///Users/monk/Nojudge/tsconfig.json)
**Purpose**: TypeScript compiler configuration
- Sets TypeScript compilation options (strict mode, ES2020 target, etc.)
- Configures module resolution for imports
- Sets up path aliases for cleaner imports
- **Why needed**: TypeScript needs to know how to compile `.ts` and `.tsx` files

### [tsconfig.node.json](file:///Users/monk/Nojudge/tsconfig.node.json)
**Purpose**: TypeScript config specifically for Vite config file
- Separate config for Node.js environment (Vite runs in Node)
- **Why needed**: Vite config file needs different TypeScript settings than app code

### [.env](file:///Users/monk/Nojudge/.env)
**Purpose**: Environment variables for development
- `FLASK_ENV=development` - Sets Flask to development mode
- `SECRET_KEY` - Secret key for JWT token signing
- `DATABASE_URL` - SQLite database location
- **Why needed**: Keeps sensitive configuration out of code, allows different settings per environment
- **⚠️ NEVER commit to Git** - Contains secrets

### [.env.example](file:///Users/monk/Nojudge/.env.example)
**Purpose**: Template for environment variables
- Shows what environment variables are needed
- Safe to commit (no actual secrets)
- **Why needed**: Helps other developers know what to configure

### [.gitignore](file:///Users/monk/Nojudge/.gitignore)
**Purpose**: Tells Git which files to ignore
- Excludes: `venv/`, `node_modules/`, `*.db`, `.env`, `dist/`, etc.
- **Why needed**: Prevents committing dependencies, secrets, and build outputs to Git

### [index.html](file:///Users/monk/Nojudge/index.html)
**Purpose**: HTML entry point for React app
- Contains root `<div id="root">` where React mounts
- Loads the main TypeScript file (`main.tsx`)
- Sets page title and meta tags
- **Why needed**: Every web app needs an HTML file as the entry point

### [README.md](file:///Users/monk/Nojudge/README.md)
**Purpose**: Project documentation
- Explains what the project does
- Setup instructions for backend and frontend
- API endpoint documentation
- Tech stack overview
- **Why needed**: Helps anyone understand and run the project

---

## 🐍 Backend Files (src/back/)

### [app.py](file:///Users/monk/Nojudge/src/back/app.py)
**Purpose**: Main Flask application entry point
- Initializes Flask app and SocketIO
- Registers API route blueprints (auth, companion)
- Sets up CORS for frontend communication
- Initializes database on startup
- Defines WebSocket event handlers
- **Why needed**: This is the server that runs and handles all API requests

### [config.py](file:///Users/monk/Nojudge/src/back/config.py)
**Purpose**: Application configuration management
- Defines config classes for development and production
- Loads environment variables
- Sets JWT expiration time, database URL, etc.
- **Why needed**: Centralizes all configuration, makes it easy to switch environments

### [database.py](file:///Users/monk/Nojudge/src/back/database.py)
**Purpose**: Database setup and connection
- Creates SQLAlchemy engine and session factory
- Defines `Base` class for all models
- `init_db()` function creates all tables
- `get_db()` function provides database sessions
- **Why needed**: Manages database connections and provides ORM functionality

---

### Models (src/back/models/)

#### [__init__.py](file:///Users/monk/Nojudge/src/back/models/__init__.py)
**Purpose**: Makes `models` a Python package
- Empty file that allows importing from this directory
- **Why needed**: Python requirement for package imports

#### [user.py](file:///Users/monk/Nojudge/src/back/models/user.py)
**Purpose**: User database model
- Defines User table structure (id, email, password_hash, created_at)
- `set_password()` - Hashes passwords with bcrypt
- `check_password()` - Verifies passwords
- `to_dict()` - Converts user to JSON (excludes password)
- **Why needed**: Stores user accounts and handles authentication

#### [companion.py](file:///Users/monk/Nojudge/src/back/models/companion.py)
**Purpose**: Companion database model
- Defines Companion table (personality, activity, mood, energy, etc.)
- `update_mood()` / `update_energy()` - Manages state with bounds checking
- `start_activity()` - Changes activity and updates mood/energy
- `get_personality_traits()` - Returns personality description
- `to_dict()` - Converts to JSON
- **Why needed**: Stores each user's companion state and personality

#### [conversation.py](file:///Users/monk/Nojudge/src/back/models/conversation.py)
**Purpose**: Message database model
- Defines Message table (companion_id, is_user_message, content, created_at)
- Stores conversation history
- `to_dict()` - Converts to JSON
- **Why needed**: Persists chat messages between user and companion

---

### Routes (src/back/routes/)

#### [__init__.py](file:///Users/monk/Nojudge/src/back/routes/__init__.py)
**Purpose**: Makes `routes` a Python package

#### [auth.py](file:///Users/monk/Nojudge/src/back/routes/auth.py)
**Purpose**: Authentication API endpoints
- `POST /api/auth/signup` - Creates new user and companion
- `POST /api/auth/login` - Authenticates user, returns JWT token
- `GET /api/auth/me` - Returns current user info (protected route)
- Validates email format and password length
- **Why needed**: Handles user registration and login

#### [companion.py](file:///Users/monk/Nojudge/src/back/routes/companion.py)
**Purpose**: Companion interaction API endpoints
- `GET /api/companion/` - Gets companion state, checks for activity changes
- `POST /api/companion/message` - Sends message, gets AI response
- `GET /api/companion/history` - Retrieves conversation history
- `GET /api/companion/activity` - Gets current activity with announcements
- `POST /api/companion/trigger-activity` - Manually triggers activity (testing)
- **Why needed**: Provides all companion interaction functionality

---

### Services (src/back/services/)

#### [__init__.py](file:///Users/monk/Nojudge/src/back/services/__init__.py)
**Purpose**: Makes `services` a Python package

#### [companion_ai.py](file:///Users/monk/Nojudge/src/back/services/companion_ai.py)
**Purpose**: AI personality engine
- `generate_response()` - Creates personality-based responses
- Different response methods for greetings, questions, food talk, etc.
- Each personality has unique response patterns
- `get_activity_announcement()` - Announces activities in character
- **Why needed**: Makes the companion feel alive with distinct personalities

#### [activity_simulator.py](file:///Users/monk/Nojudge/src/back/services/activity_simulator.py)
**Purpose**: Autonomous activity system
- `should_start_new_activity()` - Determines if companion should change activity
- `select_activity()` - Chooses next activity based on time, personality, energy
- Time-based probabilities (morning, afternoon, evening, night)
- Personality influences (lazy = more idle, curious = more exploring)
- **Why needed**: Makes companion autonomous, not just reactive

---

### Utils (src/back/utils/)

#### [__init__.py](file:///Users/monk/Nojudge/src/back/utils/__init__.py)
**Purpose**: Makes `utils` a Python package

#### [auth.py](file:///Users/monk/Nojudge/src/back/utils/auth.py)
**Purpose**: Authentication utilities
- `generate_token()` - Creates JWT tokens with user ID
- `decode_token()` - Validates and decodes JWT tokens
- `@token_required` decorator - Protects routes, requires valid token
- **Why needed**: Handles JWT authentication logic

---

## ⚛️ Frontend Files (src/front/)

### [main.tsx](file:///Users/monk/Nojudge/src/front/main.tsx)
**Purpose**: React application entry point
- Renders the root `<App />` component
- Mounts React to the `#root` div in index.html
- Wraps app in `<React.StrictMode>` for development warnings
- **Why needed**: This is where React starts

### [App.tsx](file:///Users/monk/Nojudge/src/front/App.tsx)
**Purpose**: Main application component
- Sets up React Router with routes
- Defines protected routes (require login)
- Defines public routes (redirect if logged in)
- Routes: `/` (Home), `/login`, `/signup`
- **Why needed**: Manages navigation and route protection

### [vite-env.d.ts](file:///Users/monk/Nojudge/src/front/vite-env.d.ts)
**Purpose**: TypeScript type definitions for Vite
- Defines `ImportMetaEnv` interface for environment variables
- Fixes TypeScript errors for `import.meta.env`
- **Why needed**: TypeScript needs to know about Vite's special imports

---

### Components (src/front/components/)

#### Companion Components

##### [CompanionFigure.tsx](file:///Users/monk/Nojudge/src/front/components/Companion/CompanionFigure.tsx)
**Purpose**: Animated companion character
- Renders head and body divs with 3D-style gradients
- GSAP breathing animation (continuous scale pulse)
- Mouse parallax effect (follows cursor)
- Activity-specific animations (bouncing, swaying, etc.)
- Displays mood and energy bars
- **Why needed**: Visual representation of the companion

##### [CompanionChat.tsx](file:///Users/monk/Nojudge/src/front/components/Companion/CompanionChat.tsx)
**Purpose**: Chat interface component
- Displays message history with user/companion distinction
- Input field for typing messages
- Typing indicator animation while waiting for response
- Auto-scrolls to latest message
- **Why needed**: Allows user to communicate with companion

##### [CompanionChat.css](file:///Users/monk/Nojudge/src/front/components/Companion/CompanionChat.css)
**Purpose**: Chat component styles
- Message bubble styling (different for user vs companion)
- Typing indicator animation
- Scrollbar customization
- **Why needed**: Makes chat look good and professional

#### Auth Components

##### [Login.tsx](file:///Users/monk/Nojudge/src/front/components/Auth/Login.tsx)
**Purpose**: Login form component
- Email and password inputs
- Form validation
- Calls `/api/auth/login` endpoint
- Stores JWT token in localStorage
- Redirects to home on success
- **Why needed**: Allows users to log in

##### [Signup.tsx](file:///Users/monk/Nojudge/src/front/components/Auth/Signup.tsx)
**Purpose**: Registration form component
- Email, password, confirm password inputs
- Personality selection dropdown
- Password strength validation
- Calls `/api/auth/signup` endpoint
- **Why needed**: Allows new users to create accounts

##### [Auth.css](file:///Users/monk/Nojudge/src/front/components/Auth/Auth.css)
**Purpose**: Authentication component styles
- Glassmorphism card effect
- Form styling
- Error message styling
- **Why needed**: Makes auth pages look premium

---

### Pages (src/front/pages/)

#### [Home.tsx](file:///Users/monk/Nojudge/src/front/pages/Home.tsx)
**Purpose**: Main application page
- Combines CompanionFigure and CompanionChat
- Uses `useCompanion` hook for state management
- Header with logout button
- Grid layout (companion on left, chat on right)
- **Why needed**: Main interface where users interact with companion

#### [Home.css](file:///Users/monk/Nojudge/src/front/pages/Home.css)
**Purpose**: Home page styles
- Grid layout for desktop, stacked for mobile
- Header styling
- Responsive breakpoints
- **Why needed**: Makes home page layout work properly

---

### Hooks (src/front/hooks/)

#### [useCompanion.ts](file:///Users/monk/Nojudge/src/front/hooks/useCompanion.ts)
**Purpose**: Custom React hook for companion logic
- Manages companion state
- Fetches companion data from API
- Sends messages and receives responses
- WebSocket connection for real-time updates
- Polls for activity changes every 30 seconds
- **Why needed**: Centralizes all companion-related logic

---

### Utils (src/front/utils/)

#### [api.ts](file:///Users/monk/Nojudge/src/front/utils/api.ts)
**Purpose**: API client configuration
- Creates axios instance with base URL
- Request interceptor adds JWT token to headers
- Response interceptor handles 401 errors (logout)
- Exports typed API methods (authAPI, companionAPI)
- **Why needed**: Centralizes all API calls with authentication

---

### Styles (src/front/styles/)

#### [global.css](file:///Users/monk/Nojudge/src/front/styles/global.css)
**Purpose**: Global styles and design system
- CSS variables for colors, spacing, shadows, etc.
- Dark theme color palette
- Utility classes (flex, gap, text-center, etc.)
- Button and input base styles
- Animations (fadeIn, pulse, spin)
- **Why needed**: Provides consistent styling across entire app

#### [companion.css](file:///Users/monk/Nojudge/src/front/styles/companion.css)
**Purpose**: Companion-specific styles
- Figure styling (head, body with gradients)
- Activity-based glow effects
- Mood/energy progress bars with shimmer animation
- Responsive sizing for mobile
- **Why needed**: Makes companion look visually appealing

---

## 🗂️ Original Files (Preserved)

### [mode.html](file:///Users/monk/Nojudge/src/front/mode.html)
**Purpose**: Original vanilla JS prototype
- Simple HTML/CSS/JS version of companion
- Kept as reference/demo
- **Why needed**: Shows the original concept before React implementation

### [mode2.js](file:///Users/monk/Nojudge/src/front/mode2.js)
**Purpose**: Original GSAP animations
- Breathing and parallax effects
- **Why needed**: Original animation code that was adapted for React

### [login.html](file:///Users/monk/Nojudge/src/front/login.html)
**Purpose**: Original login page
- Basic HTML login form
- **Why needed**: Original design reference

---

## 📊 Summary

**Total Files Created**: ~40 files

**Files to NEVER commit to Git** (in .gitignore):
- `venv/` - Python virtual environment
- `node_modules/` - Node dependencies
- `.env` - Environment variables with secrets
- `*.db` - Database files
- `dist/` - Build outputs
- `__pycache__/` - Python cache

**Key Technologies**:
- **Backend**: Flask, SQLAlchemy, JWT, bcrypt, SocketIO
- **Frontend**: React, TypeScript, GSAP, Vite
- **Database**: SQLite
- **Styling**: CSS with custom design system

Each file serves a specific purpose in creating a complete, production-ready AI companion application!
