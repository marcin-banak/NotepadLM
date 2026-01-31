import os
import json
import requests
import argparse
from typing import List, Dict, Optional


class NoteUploader:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.token: Optional[str] = None
    
    def login(self, username: str, password: str) -> bool:
        url = f"{self.base_url}/auth/login"
        payload = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.token = data.get("access_token")
            
            if self.token:
                print(f"✓ Successfully logged in as {username}")
                return True
            else:
                print("✗ Login failed: No token received")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Login failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"  Response: {e.response.text}")
            return False
    
    def create_note(self, title: str, content: str, group_id: Optional[int] = None) -> bool:
        if not self.token:
            print("✗ Not authenticated. Please login first.")
            return False
        
        url = f"{self.base_url}/notes"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "title": title,
            "content": content
        }
        if group_id is not None:
            payload["group_id"] = group_id
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to create note '{title}': {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"  Response: {e.response.text}")
            return False
    
    def bulk_create_notes(self, notes: List[Dict[str, str]]) -> Dict[str, any]:
        """Upload multiple notes using the bulk endpoint."""
        if not self.token:
            print("✗ Not authenticated. Please login first.")
            return {"success": 0, "failed": len(notes), "errors": []}
        
        url = f"{self.base_url}/notes/bulk"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Prepare notes payload
        notes_payload = []
        for note in notes:
            note_data = {
                "title": note.get("title", "Untitled Note"),
                "content": note.get("content", "")
            }
            # Include group_id if present
            if "group_id" in note:
                note_data["group_id"] = note["group_id"]
            notes_payload.append(note_data)
        
        payload = {"notes": notes_payload}
        
        try:
            print(f"\nUploading {len(notes)} notes via bulk endpoint...")
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            created_count = len(data.get("created", []))
            failed_count = len(data.get("failed", []))
            failed_notes = data.get("failed", [])
            
            if failed_notes:
                print("\nFailed notes:")
                for failed in failed_notes:
                    print(f"  ✗ [{failed.get('index', '?')}] {failed.get('title', 'Unknown')}: {failed.get('error', 'Unknown error')}")
            
            return {
                "success": created_count,
                "failed": failed_count,
                "errors": failed_notes
            }
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to bulk upload notes: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"  Response: {e.response.text}")
            return {"success": 0, "failed": len(notes), "errors": [{"error": str(e)}]}
    
    def upload_notes(self, notes: List[Dict[str, str]], use_bulk: bool = True) -> Dict[str, int]:
        """Upload notes, using bulk endpoint by default for better performance."""
        if use_bulk:
            result = self.bulk_create_notes(notes)
            return {
                "success": result["success"],
                "failed": result["failed"]
            }
        
        # Fallback to individual uploads if bulk is disabled
        if not self.token:
            print("✗ Not authenticated. Please login first.")
            return {"success": 0, "failed": len(notes)}
        
        results = {"success": 0, "failed": 0}
        
        print(f"\nUploading {len(notes)} notes...")
        for i, note in enumerate(notes, 1):
            title = note.get("title", "Untitled Note")
            content = note.get("content", "")
            topic = note.get("topic", "Unknown")
            
            print(f"[{i}/{len(notes)}] Uploading: {title} (topic: {topic})")
            
            if self.create_note(title, content):
                results["success"] += 1
                print(f"  ✓ Success")
            else:
                results["failed"] += 1
                print(f"  ✗ Failed")
        
        return results


def load_notes(file_path: str) -> List[Dict[str, str]]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Notes file not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        notes = json.load(f)
    
    if not isinstance(notes, list):
        raise ValueError("Notes file must contain a JSON array")
    
    print(f"✓ Loaded {len(notes)} notes from {file_path}")
    return notes


def main():
    parser = argparse.ArgumentParser(
        description="Upload notes to NotepadLM via API"
    )

    parser.add_argument(
        "username",
        help="API username"
    )

    parser.add_argument(
        "password",
        help="API password"
    )

    parser.add_argument(
        "notes_file_name",
        help="Note set in script's directory name"
    )

    args = parser.parse_args()

    try:
        notes_file = os.path.join(os.path.dirname(__file__), args.notes_file_name)
        api_base_url = "http://localhost:8000"

        notes = load_notes(notes_file)

        uploader = NoteUploader(base_url=api_base_url)

        if not uploader.login(args.username, args.password):
            print("Failed to login. Exiting.")
            exit(1)

        results = uploader.upload_notes(
            notes,
            use_bulk=True
        )

        print("\n" + "=" * 50)
        print("Upload Summary:")
        print(f"  Success: {results['success']}")
        print(f"  Failed:  {results['failed']}")
        print(f"  Total:   {len(notes)}")
        print("=" * 50)

    except Exception as e:
        print(f"✗ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()

