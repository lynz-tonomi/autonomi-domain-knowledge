# SharePoint & OneDrive Reference — Autonomi Agents

## Table of Contents
1. [Site & Drive Discovery](#site--drive-discovery)
2. [File Operations](#file-operations)
3. [Large File Upload](#large-file-upload)
4. [SharePoint Lists](#sharepoint-lists)
5. [Folder Structure Management](#folder-structure-management)
6. [Sharing & Permissions](#sharing--permissions)

## Site & Drive Discovery

### Find the Autonomi SharePoint site

```python
# Search for site by name
sites = requests.get(
    "https://graph.microsoft.com/v1.0/sites?search=Autonomi",
    headers=headers
).json()["value"]

# Get site by hostname and path
site = requests.get(
    "https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/Autonomi",
    headers=headers
).json()
site_id = site["id"]

# Get the default document library drive
drive = requests.get(
    f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive",
    headers=headers
).json()
drive_id = drive["id"]
```

### List all document libraries on a site

```python
drives = requests.get(
    f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives",
    headers=headers
).json()["value"]
```

## File Operations

### Upload small file (<4MB)

```python
def upload_file(drive_id, folder_path, filename, content, headers):
    """Upload a file to SharePoint. For files <4MB."""
    url = (
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
        f"root:{folder_path}/{filename}:/content"
    )
    resp = requests.put(url, headers={**headers, "Content-Type": "application/octet-stream"}, data=content)
    resp.raise_for_status()
    return resp.json()
```

### Download file

```python
def download_file(drive_id, item_id, headers):
    """Download file content by item ID."""
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/content",
        headers=headers,
        allow_redirects=True
    )
    resp.raise_for_status()
    return resp.content
```

### List folder contents

```python
def list_folder(drive_id, folder_path, headers):
    """List files in a SharePoint folder."""
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:{folder_path}:/children"
    return get_all_pages(url, headers)
```

### Search for files

```python
# Search across the entire site
results = requests.get(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/search(q='COA batch 2847')",
    headers=headers
).json()
```

### Move / Copy files

```python
# Move file to a different folder
requests.patch(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}",
    headers=headers,
    json={"parentReference": {"id": target_folder_id}}
)

# Copy file
requests.post(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/copy",
    headers=headers,
    json={"parentReference": {"driveId": drive_id, "id": target_folder_id}, "name": "Copy of file.pdf"}
)
```

## Large File Upload

For files >4MB, use an upload session with chunked upload:

```python
def upload_large_file(drive_id, folder_path, filename, file_path, headers):
    """Upload file >4MB using chunked upload session."""
    import os

    file_size = os.path.getsize(file_path)

    # Create upload session
    session = requests.post(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
        f"root:{folder_path}/{filename}:/createUploadSession",
        headers=headers,
        json={"item": {"@microsoft.graph.conflictBehavior": "rename"}}
    ).json()
    upload_url = session["uploadUrl"]

    # Upload in 5MB chunks
    chunk_size = 5 * 1024 * 1024
    with open(file_path, "rb") as f:
        start = 0
        while start < file_size:
            end = min(start + chunk_size, file_size) - 1
            chunk = f.read(chunk_size)
            resp = requests.put(upload_url, data=chunk, headers={
                "Content-Length": str(len(chunk)),
                "Content-Range": f"bytes {start}-{end}/{file_size}",
            })
            resp.raise_for_status()
            start = end + 1

    return resp.json()
```

## SharePoint Lists

SharePoint Lists are useful for structured data that agents track (supplier contacts, batch log, etc.).

```python
# Get lists on a site
lists = requests.get(
    f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists",
    headers=headers
).json()["value"]

# Get items from a list
items = requests.get(
    f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items"
    "?expand=fields&$top=100",
    headers=headers
).json()

# Create list item
requests.post(
    f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items",
    headers=headers,
    json={"fields": {
        "Title": "Batch 2847",
        "Product": "Mango Puree",
        "Status": "QC Hold",
        "LotNumber": "Lot-2847"
    }}
)

# Update list item
requests.patch(
    f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}/fields",
    headers=headers,
    json={"Status": "QC Passed"}
)
```

## Folder Structure Management

### Create folder

```python
def create_folder(drive_id, parent_path, folder_name, headers):
    """Create a folder in SharePoint."""
    resp = requests.post(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:{parent_path}:/children",
        headers=headers,
        json={"name": folder_name, "folder": {}, "@microsoft.graph.conflictBehavior": "fail"}
    )
    if resp.status_code == 409:
        return None  # Folder already exists
    resp.raise_for_status()
    return resp.json()
```

### Initialize tenant folder structure

See `scripts/setup_tenant_workspace.py` for the full script that creates the standard Autonomi folder tree on a new tenant's SharePoint site.

## Sharing & Permissions

Agents should generally NOT modify sharing permissions (that's a tenant admin responsibility). However, agents may need to create sharing links for generated reports:

```python
# Create a read-only sharing link (for emailing report links)
link = requests.post(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/createLink",
    headers=headers,
    json={"type": "view", "scope": "organization"}  # Only people in the org can view
).json()
share_url = link["link"]["webUrl"]
```
