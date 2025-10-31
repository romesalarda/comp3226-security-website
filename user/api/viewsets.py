from rest_framework import decorators, request, response
import opaquepy
from user.models import CustomUser
from django.shortcuts import get_object_or_404
from django.core.cache import cache
import base64
import uuid

@decorators.api_view(["POST"])
def opaque_registration(req:request.HttpRequest):
    email = req.data.get("email")
    registration_request = req.data.get("registration_request")
    print("Registration request recieved from extension :" + str(registration_request))
    setup = opaquepy.create_setup()
    to_client = opaquepy.register(setup, registration_request, email)
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
    
    setup = opaquepy.create_setup()
    
    client_response, login_state = opaquepy.login(
        setup=setup,
        password_file=user.opaque_envelope,
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
 
    cache.delete(cache_key)
    
    print(f"Login completed for user: {email}")
    
    return response.Response({
        "statusText": "Login successful",
        "email": email,
        "user_id": user_id
    })