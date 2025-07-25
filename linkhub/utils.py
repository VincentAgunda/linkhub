import frappe
from frappe.website.path_resolver import resolve_path as original_resolve_path

def path_resolver(path: str):
    # Check if it's a known short link
    if frappe.db.exists("Short Link", {"short_link": path}):
        destination = frappe.db.get_value("Short Link", {"short_link": path}, "destination_url")

        # Set redirect location and raise redirect exception
        frappe.local.flags.redirect_location = destination
        raise frappe.Redirect

    # Fallback to original resolver for everything else
    return original_resolve_path(path)
