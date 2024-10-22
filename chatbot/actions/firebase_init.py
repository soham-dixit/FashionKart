# import firebase_admin
# from firebase_admin import credentials

# firebase_initialized = False  # Flag to check if Firebase is already initialized

# def initialize_firebase(credential_path, storage_bucket):
#     global firebase_initialized
#     if not firebase_initialized:
#         cred = credentials.Certificate(credential_path)
#         firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket})
#         firebase_initialized = True