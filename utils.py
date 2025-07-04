def is_valid_url(url):
    if not isinstance(url, str) or not url.strip():
        return False  # Ensure `url` is a non-empty string
    return url.strip().startswith(("http://", "https://"))  # Handles both cases efficiently

