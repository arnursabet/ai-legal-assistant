Before you run the app, add a `.env` file to the `chainlit-backend` folder. Include the following information:
```toml
OPENAI_API_KEY="ADD_API_KEY_HERE"

CHAINLIT_CUSTOM_AUTH=true
CHAINLIT_AUTH_SECRET="NjL9OWxdJAIhf^=EfQ63MlNs/Ho%x?Faj98ZrGBT>%Mr%sN~/e_5kY_2a5-EpkIc"
```

To run the app, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/arnursabet/ai-legal-assistant.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ai-legal-assistant
   ```

3. Navigate to the backend directory:
   ```bash
   cd chainlit-backend
   ```
4. Create and activate a virtual environment
   ```bash
   python3 -m venv venv

   source venv/bin/activate
   ```

5. Install the dependencies from requirements.txt
   ```bash
   pip install -r requirements.txt
   ```
6. Start the backend server:
   ```bash
   chainlit run app.py -h -w -d
   ```
7. Open a new terminal window and navigate to the project directory again:
   ```bash
   cd ai-legal-assistant
   ```

8.  Install the dependencies for the frontend:
   ```bash
   cd frontend
   npm install
   ```

9.  Start the frontend development server:
   ```bash
   npm run dev
   ```

10. Open your web browser and visit `http://localhost:5173` to see the AI chatbot in action.