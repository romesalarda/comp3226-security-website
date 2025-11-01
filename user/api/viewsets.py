from rest_framework import decorators, request, response
from rest_framework.permissions import IsAuthenticated
from user.models import CustomUser

from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt

import opaquepy
import base64
import uuid
import os
import json

def get_server_setup():
    """
    Get or create a persistent OPAQUE server setup.
    The setup is stored in a file to survive server restarts.
    
    Keep in mind that changing the serverSetup will invalidate all existing password files.

    """
    setup_file = os.path.join(settings.BASE_DIR, 'opaque_server_setup.json')
    
    # Try to load existing setup
    if os.path.exists(setup_file):
        try:
            with open(setup_file, 'r') as f:
                setup_data = f.read()
                print(f"Loaded existing OPAQUE setup from {setup_file}")
                return setup_data
        except Exception as e:
            print(f"Error loading setup file: {e}")
    
    # Create new setup if none exists
    print("Creating new OPAQUE server setup...")
    setup = opaquepy.create_setup()
    
    # Save setup to file
    try:
        with open(setup_file, 'w') as f:
            f.write(setup)
        print(f"Saved OPAQUE setup to {setup_file}")
    except Exception as e:
        print(f"Warning: Could not save setup to file: {e}")
    
    return setup

# Initialize server setup once at module load
SERVER_SETUP = get_server_setup()

@decorators.api_view(["POST"])
def opaque_registration(req:request.HttpRequest):
    email = req.data.get("email")
    registration_request = req.data.get("registration_request")
    print("Registration request recieved from extension :" + str(registration_request))
    to_client = opaquepy.register(SERVER_SETUP, registration_request, email)
    print("Sending request back to client :" + str(to_client))
    return response.Response(to_client)

@decorators.api_view(["POST"])
def opaque_registration_finish(req:request.HttpRequest):
    
    email = req.data.get("email")
    client_request_finish = req.data.get("registration_record")
    
    envelope_to_be_saved = opaquepy.register_finish(client_request_finish)
    CustomUser.objects.create(email=email, opaque_envelope=bytes(envelope_to_be_saved, encoding="utf-8"))
    
    return response.Response({"statusText": "new user created!"})

@decorators.api_view(["POST"])
def opaque_login(req:request.HttpRequest):
    """
    OPAQUE Login Step 1: Start login process
    Stores login state in cache and returns server response + cache key to client
    """
    email = req.data.get("email")
    client_request = req.data.get("client_request")
    
    user = get_object_or_404(CustomUser, email=email)
    
    client_response, login_state = opaquepy.login(
        setup=SERVER_SETUP,
        password_file=user.opaque_envelope.decode("utf-8"),
        client_request=client_request,
        credential_id=email
    )
    
    cache_key = f"opaque_login_{uuid.uuid4().hex}"
    
    cache_data = {
        'login_state': login_state,
        'email': email,
        'user_id': user.id
    }
    cache.set(cache_key, cache_data, timeout=300)  # 5 minutes
    
    print(f"Login state cached with key: {cache_key}")
    
    return response.Response({
        "client_response": client_response,
        "cache_key": cache_key
    })

@decorators.api_view(["POST"])
def opaque_login_finish(req:request.HttpRequest):
    """
    OPAQUE Login Step 2: Finish login process
    Retrieves login state from cache and completes authentication
    """
    cache_key = req.data.get("cache_key")
    client_finish_request = req.data.get("client_finish_request")
    
    if not cache_key:
        return response.Response(
            {"error": "cache_key is required"},
            status=400
        )
    
    # Retrieve login state from cache
    cache_data = cache.get(cache_key)
    
    if not cache_data:
        return response.Response(
            {"error": "Login session expired or invalid cache key"},
            status=404
        )
    
    login_state = cache_data.get('login_state')
    email = cache_data.get('email')
    user_id = cache_data.get('user_id')
    
    session_key = opaquepy.login_finish(
        client_finish_request,
        login_state)
    
    
 
    cache.delete(cache_key)
    user = get_object_or_404(CustomUser, email=email)
    
    login(req, user)
    
    print(f"Login completed for user: {email}")
    print(f"Session key: {req.session.session_key}")
    print(f"User authenticated: {req.user.is_authenticated}")
    
    return response.Response({
        "statusText": "Login successful",
        "email": email,
        "user_id": user_id,
        "session_active": True
    })

@decorators.api_view(["GET"])
@decorators.permission_classes([IsAuthenticated])
def verify_session(req:request.HttpRequest):
    """
    Verify that the user's session is active and valid
    """
    return response.Response({
        "authenticated": True,
        "email": req.user.email,
        "user_id": req.user.id
    })

@decorators.api_view(["GET"])
def session_redirect(req:request.HttpRequest):
    """
    Redirect endpoint that transfers the session to browser context.
    Used after OPAQUE login to activate session in main browser.
    """
    from django.shortcuts import redirect
    
    if req.user.is_authenticated:
        # Session is valid, redirect to home
        return redirect('home')
    else:
        # No valid session, redirect to login
        return redirect('login')

@decorators.api_view(["POST"])
@decorators.permission_classes([IsAuthenticated])
def logout_session(req:request.HttpRequest):
    """
    Logout the user and invalidate the session
    """
    from django.contrib.auth import logout
    email = req.user.email
    logout(req)
    
    return response.Response({
        "statusText": "Logout successful",
        "email": email
    })