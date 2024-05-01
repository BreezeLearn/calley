from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError

# app = FastAPI()
# app.add_middleware(SessionMiddleware, secret_key="add any string...")

router = APIRouter()

GOOGLE_CLIENT_ID = '81095960993-gn2vbd6al778otnkpi2hfjn0ek6qk6a6.apps.googleusercontent.com'
CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URI = 'https://localhost:8000/login/callback'

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_uri': 'https://localhost:8000/login/callback'
    }
)

@router.get("/")
def index(request: Request):
    user = request.session.get('user')
    if user:
        return RedirectResponse('/welcome')
    return '<a href="/google_login">Login with Google</a>'

@router.get('/welcome')
def welcome(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')
    return {"user": user}

@router.get("/google_login")
async def login(request: Request):
    auth_url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20email%20profile"
    return {"auth_url": auth_url}
@router.get('/login/callback')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return RedirectResponse('/')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse('/welcome')

@router.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse('/')


