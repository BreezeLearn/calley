
# calley is an AI Scheduling and calender management assistant that uses Google Gemini-pro language model for intelligent interaction. 

## Getting Started

```bash
git clone https://github.com/daviduche03/calley.git
cd calley

# setting up venv
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt



# Run the server
python main.py

# start your browser and open http://localhost:8000

# setting environment secrets
locate Agent/main.py and add 'GOOGLE_API_KEY' from google AI platform 

# next giving it acces to your calender
run 'python cal2.py' to authorize and save your auth key to local device

but a google cloud project OAuth 2.0 authorization file is needed, you can get it from google cloud console for desktop client. download file, rename to 'credentials.json' and move to calley folder

you can now run 'python main.py' and move on to the frontend UI

cd frontend/calley-ui
npm install
npm run dev

# open http://localhost:5173

# Routes to calley
'/' - calley home page
'/dashboard' - calley dashboard for chatting with your agent
'/login' - calley login page 'login details below'
'/create-agent' - calley create agent page

# login details
email: test_acc@gmail.com
password: test_acc

```

