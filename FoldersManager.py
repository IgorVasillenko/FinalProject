import os

def ensureFolders():
    if not os.path.exists('static/images'):
        os.makedirs('static/images', exist_ok=True)


ensureFolders()