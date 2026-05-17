"""
Firebase Authentication Service
Handles Firebase Admin SDK initialization and token verification
"""

import os
import json
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth
from pydantic import BaseModel, EmailStr

load_dotenv()


class FirebaseUser(BaseModel):
    """Firebase user model"""
    uid: str
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    email_verified: bool = False


class FirebaseService:
    """Service for Firebase authentication"""
    
    _initialized = False
    
    @classmethod
    def initialize(cls):
        """Initialize Firebase Admin SDK"""
        if cls._initialized:
            return
        
        try:
            # Try to get service account path from environment
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
            
            if service_account_path and os.path.exists(service_account_path):
                # Initialize with service account file
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
                print("[INFO] Firebase Admin SDK initialized with service account")
            else:
                # Try to initialize with environment variables
                service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON')
                
                if service_account_json:
                    # Parse JSON from environment variable
                    service_account_dict = json.loads(service_account_json)
                    cred = credentials.Certificate(service_account_dict)
                    firebase_admin.initialize_app(cred)
                    print("[INFO] Firebase Admin SDK initialized with environment JSON")
                else:
                    # Fallback for just token verification: initialize with project ID
                    project_id = os.getenv('FIREBASE_PROJECT_ID', 'graphmindai-573e7')
                    if project_id:
                        firebase_admin.initialize_app(options={'projectId': project_id})
                        print(f"[INFO] Firebase Admin SDK initialized with Project ID: {project_id} (Token verification only)")
                    else:
                        print("[WARNING] Firebase service account and project ID not configured")
                        print("          Set FIREBASE_SERVICE_ACCOUNT_PATH, FIREBASE_SERVICE_ACCOUNT_JSON, or FIREBASE_PROJECT_ID")
                        print("          Authentication will not work without Firebase configuration")
                        return
            
            cls._initialized = True
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize Firebase Admin SDK: {e}")
            print("        Authentication will not work without Firebase configuration")
    
    @staticmethod
    def verify_token(id_token: str) -> Optional[FirebaseUser]:
        """
        Verify Firebase ID token and return user info
        
        Args:
            id_token: Firebase ID token from client
            
        Returns:
            FirebaseUser if token is valid, None otherwise
        """
        if not FirebaseService._initialized:
            print("[ERROR] Firebase not initialized")
            return None
        
        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            
            # Extract user information
            return FirebaseUser(
                uid=decoded_token['uid'],
                email=decoded_token.get('email'),
                display_name=decoded_token.get('name'),
                email_verified=decoded_token.get('email_verified', False)
            )
            
        except auth.InvalidIdTokenError:
            print("[ERROR] Invalid Firebase ID token")
            return None
        except auth.ExpiredIdTokenError:
            print("[ERROR] Expired Firebase ID token")
            return None
        except Exception as e:
            print(f"[ERROR] Error verifying Firebase token: {e}")
            return None
    
    @staticmethod
    def get_user_by_uid(uid: str) -> Optional[Dict[str, Any]]:
        """
        Get user information by UID
        
        Args:
            uid: Firebase user UID
            
        Returns:
            User information dict or None
        """
        if not FirebaseService._initialized:
            return None
        
        try:
            user = auth.get_user(uid)
            return {
                'uid': user.uid,
                'email': user.email,
                'display_name': user.display_name,
                'email_verified': user.email_verified,
                'disabled': user.disabled,
                'created_at': user.user_metadata.creation_timestamp,
            }
        except Exception as e:
            print(f"[ERROR] Error getting user by UID: {e}")
            return None
    
    @staticmethod
    def create_custom_token(uid: str, additional_claims: Optional[Dict] = None) -> Optional[str]:
        """
        Create a custom token for a user
        
        Args:
            uid: Firebase user UID
            additional_claims: Optional additional claims to include
            
        Returns:
            Custom token string or None
        """
        if not FirebaseService._initialized:
            return None
        
        try:
            return auth.create_custom_token(uid, additional_claims)
        except Exception as e:
            print(f"[ERROR] Error creating custom token: {e}")
            return None


# Initialize Firebase on module import
FirebaseService.initialize()

# Made with Bob
