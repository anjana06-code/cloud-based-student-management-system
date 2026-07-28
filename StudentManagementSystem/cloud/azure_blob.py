import os
from werkzeug.utils import secure_filename

# Try to import Azure Blob Storage library
try:
    from azure.storage.blob import BlobServiceClient
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

# Local upload directory setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Read Azure configuration from environment variables
AZURE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', '')
CONTAINER_NAME = os.environ.get('AZURE_BLOB_CONTAINER_NAME', 'student-uploads')

def upload_file_to_storage(file_obj, student_id):
    """
    Uploads a file to Azure Blob Storage if configured, otherwise falls back to local disk storage.
    Returns a tuple of (saved_filename, file_path_or_url).
    """
    original_filename = secure_filename(file_obj.filename)
    if not original_filename:
        raise ValueError("Invalid file name")
        
    # Create unique filename by prepending student_id
    saved_filename = f"student_{student_id}_{original_filename}"
    
    # Check if Azure Blob Storage is configured
    if AZURE_AVAILABLE and AZURE_CONNECTION_STRING:
        try:
            print("Uploading file to Azure Blob Storage...")
            blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
            container_client = blob_service_client.get_container_client(CONTAINER_NAME)
            
            # Create container if it does not exist
            if not container_client.exists():
                container_client.create_container()
                
            blob_client = container_client.get_blob_client(saved_filename)
            blob_client.upload_blob(file_obj.read(), overwrite=True)
            
            file_url = blob_client.url
            print(f"Uploaded successfully to Azure Blob Storage: {file_url}")
            return saved_filename, file_url
        except Exception as e:
            print(f"Azure Blob Storage upload failed ({str(e)}). Falling back to local storage.")
            file_obj.seek(0)  # Reset file pointer after read attempt
            
    # Local Storage Fallback
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
    local_path = os.path.join(UPLOAD_FOLDER, saved_filename)
    file_obj.save(local_path)
    print(f"Saved file locally at: {local_path}")
    return saved_filename, local_path

def delete_file_from_storage(filename_or_path):
    """
    Deletes a file from Azure Blob Storage or local storage.
    """
    # Check if file is stored in Azure
    if AZURE_AVAILABLE and AZURE_CONNECTION_STRING and filename_or_path.startswith('http'):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
            container_client = blob_service_client.get_container_client(CONTAINER_NAME)
            # Extract filename from URL
            blob_name = filename_or_path.split('/')[-1]
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.delete_blob()
            print(f"Deleted blob from Azure: {blob_name}")
            return True
        except Exception as e:
            print(f"Failed to delete Azure blob: {str(e)}")
            return False
    else:
        # Local storage deletion
        target_path = filename_or_path if os.path.isabs(filename_or_path) else os.path.join(UPLOAD_FOLDER, filename_or_path)
        if os.path.exists(target_path):
            os.remove(target_path)
            print(f"Deleted local file: {target_path}")
            return True
    return False
