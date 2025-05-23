# Riley AI - Modular Autonomous Intelligence Platform

Riley is a full-stack, production-grade AI assistant designed as a modular, voice-enabled, web-deployable intelligence engine inspired by J.A.R.V.I.S., with autonomous features, reasoning engines, and real-time web interaction.

## Project Structure

The project is divided into two main parts:

1. **Backend**: A Flask API with modular package structure
2. **Frontend**: A Next.js application with a modern UI

### Backend Structure

The backend is organized under the `/backend` directory with the following structure:

- `app.py`: Main Flask application
- `/riley`: Package containing all the AI modules
  - `/core`: Core modules
    - `reasoning.py`: Handles reasoning and response generation
    - `invention.py`: Generates original scientific or consumer invention concepts
    - `emotion.py`: Detects and generates emotional responses
    - `memory.py`: Stores and retrieves structured AI memory and facts
    - `self_editing.py`: Monitors and modifies faulty code autonomously
  - `/interfaces`: Interface modules
    - `web.py`: Web interface utilities
    - `voice.py`: Voice interface utilities
  - `/learning`: Learning modules
    - `wikipedia_search.py`: Pulls and summarizes real-time web/wikipedia info
    - `github_learning.py`: Clones public repos, learns patterns, evolves code

### Frontend Structure

The frontend is organized under the `/frontend` directory with the following structure:

- `/app`: Next.js app directory
  - `/page.tsx`: Home page
  - `/about/page.tsx`: About page
  - `/console/page.tsx`: Main console for interacting with Riley
  - `/settings/page.tsx`: Settings page
- `/components`: Reusable components
- `/hooks`: Custom React hooks

### Database Structure

The database is organized with the following schema:

- `riley.interactions`: Stores chat interactions
- `riley.memory`: Stores Riley's memory
- `riley.facts`: Stores learned facts
- `riley.user_settings`: Stores user settings
- `riley.inventions`: Stores generated inventions
- `riley.search_history`: Stores search results
- `riley.github_analysis`: Stores GitHub repository analyses
- `riley.code_repairs`: Stores code repair history
- `riley.scientific_formulas`: Stores scientific formulas
- `riley.self_edits`: Tracks autonomous code changes
- `riley.voice_sessions`: Stores voice session data
- `riley.knowledge_base`: Stores learned information

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn
- PostgreSQL database (Neon)

### Backend Setup

1. Navigate to the backend directory:
   \`\`\`
   cd backend
   \`\`\`

2. Create a virtual environment:
   \`\`\`
   python -m venv venv
   \`\`\`

3. Activate the virtual environment:
   - On Windows:
     \`\`\`
     venv\Scripts\activate
     \`\`\`
   - On macOS/Linux:
     \`\`\`
     source venv/bin/activate
     \`\`\`

4. Install dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

5. Create a `.env` file based on `.env.example`:
   \`\`\`
   cp .env.example .env
   \`\`\`

6. Edit the `.env` file with your API keys and configuration.

7. Run the Flask application:
   \`\`\`
   python app.py
   \`\`\`

### Frontend Setup

1. Navigate to the frontend directory:
   \`\`\`
   cd frontend
   \`\`\`

2. Install dependencies:
   \`\`\`
   npm install
   # or
   yarn install
   \`\`\`

3. Run the development server:
   \`\`\`
   npm run dev
   # or
   yarn dev
   \`\`\`

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Environment Variables

The following environment variables are required:

- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: PostgreSQL connection string (Neon)
- `RILEY_MODEL`: The OpenAI model to use (default: gpt-4o)
- `RILEY_MODE`: Default startup mode (e.g., "assistant", "genius", "inventor")
- `VOICE_ENABLED`: true/false toggle for audio I/O
- `ALLOW_SELF_EDITING`: Security toggle for autonomous code rewrite

## Deployment

### Vercel Deployment

The project is configured for deployment on Vercel:

1. Push your code to a GitHub repository
2. Connect the repository to Vercel
3. Configure the environment variables
4. Deploy

The `vercel.json` file includes the necessary configuration for deploying both the backend and frontend.

## Features

- **Modular Architecture**: Each capability is encapsulated in its own module
- **Voice Interaction**: Speak to Riley and receive spoken responses
- **Multiple Intelligence Modes**: Switch between different modes for different tasks
- **Invention Generation**: Create original scientific or consumer invention concepts
- **Emotion Detection**: Detect and respond to emotions in user messages
- **Web Research**: Search and summarize information from the web
- **GitHub Learning**: Analyze and learn from public repositories
- **Memory Storage**: Store and retrieve structured AI memory and facts
- **Autonomous Code Repair**: Automatically fix faulty code

## License

This project is licensed under the MIT License - see the LICENSE file for details.
