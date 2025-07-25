import frappe
from frappe.website.path_resolver import resolve_path as original_resolve_path
# TODO:

def path_resolver(path: str):
    print(f"--- Path Resolver: Starting for path: {path} ---")

    short_link_doc = frappe.db.get_value(
        "Short Link",
        {"short_link": path},
        ["destination_url", "name"],
        as_dict=True
    )

    print(f"DEBUG: short_link_doc found: {short_link_doc}")

    if short_link_doc:
        print(f"DEBUG: Short Link found. Name: {short_link_doc.name}, Destination: {short_link_doc.destination_url}")

        click = frappe.new_doc("Short Link Click")
        # --- FIX STARTS HERE ---
        # Access the request object via frappe.request
        if frappe.request: # Check if request object exists (e.g., in web context)
            click.ip = frappe.request.headers.get("X-Real-Ip")
            click.user_agent = frappe.request.headers.get("User-Agent")
            click.referer = frappe.request.headers.get("Referer")
        else:
            # Handle cases where frappe.request might not be available (e.g., CLI or background jobs)
            print("WARNING: frappe.request not available. IP, User-Agent, Referer will be empty.")
            click.ip = None
            click.user_agent = None
            click.referer = None
        # --- FIX ENDS HERE ---
        click.link = short_link_doc.name

        print(f"DEBUG: Creating Short Link Click for short_link (or link field): {click.link}")

        click.insert(ignore_permissions=True)
        frappe.db.commit() #to remove once MyISAM
        print("DEBUG: Short Link Click recorded and committed.")

        print(f"--- Path Resolver: Redirecting to: {short_link_doc.destination_url} ---")
        frappe.redirect(short_link_doc.destination_url)

    print(f"--- Path Resolver: No short link found for '{path}'. Falling back to original resolver. ---")
    return original_resolve_path(path)
