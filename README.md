# Nojudge AI Companion

An AI companion application where users interact with a digital friend that has its own personality, activities, and autonomous behaviors.

## Features

- **Personality System**: Choose from 6 different personalities (intelligent, lazy, inquisitive, cheerful, grumpy, curious)
- **Autonomous Activities**: Your companion cooks, eats, sleeps, and explores on its own
- **Real-time Chat**: Have conversations with your companion based on its personality
- **GSAP Animations**: Smooth, interactive animations with mouse parallax effects
- **Mood & Energy System**: Companion's state changes based on activities and interactions
- **WebSocket Integration**: Real-time activity updates

## Tech Stack

### Backend
- Python 3.x
- Flask (Web framework)
- Flask-SocketIO (WebSocket support)
- SQLAlchemy (ORM)
- SQLite (Database)
- JWT (Authentication)
- bcrypt (Password hashing)

### Frontend
- React 18
- TypeScript
- Vite (Build tool)
- GSAP (Animations)
- React Router (Navigation)
- Axios (HTTP client)
- Socket.IO Client (WebSocket)

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
cd /Users/monk/Nojudge
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
cd src/back
python app.py
```

The backend will run on `http://localhost:5001`

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd /Users/monk/Nojudge
npm install
```

2. Run the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## Usage

1. Open `http://localhost:5173` in your browser
2. Sign up for a new account and choose your companion's personality
3. Start chatting with your companion!
4. Watch your companion perform autonomous activities
5. Observe mood and energy levels change based on interactions

## Project Structure

```
Nojudge/
├── src/
│   ├── back/              # Backend (Python/Flask)
│   │   ├── models/        # Database models
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── utils/         # Utilities
│   │   ├── app.py         # Main Flask app
│   │   ├── config.py      # Configuration
│   │   └── database.py    # Database setup
│   └── front/             # Frontend (React/TypeScript)
│       ├── components/    # React components
│       ├── hooks/         # Custom hooks
│       ├── pages/         # Page components
│       ├── styles/        # CSS files
│       ├── utils/         # Utilities
│       ├── App.tsx        # Main App component
│       └── main.tsx       # Entry point
├── package.json
├── requirements.txt
├── vite.config.ts
└── tsconfig.json
```

## API Endpoints

Base URL: `http://localhost:5001/api`

### Authentication
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Companion
- `GET /api/companion/` - Get companion state
- `POST /api/companion/message` - Send message to companion
- `GET /api/companion/history` - Get conversation history
- `GET /api/companion/activity` - Get current activity
- `POST /api/companion/trigger-activity` - Manually trigger activity (testing)

## Future Enhancements

- Companion friends (social interactions between companions)
- More personality types
- Advanced AI with LLM integration
- Voice interaction
- Mobile app
- Customizable companion appearance
- Achievement system
- Activity history and statistics

## License

MIT