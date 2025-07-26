import frappe
from frappe.website.path_resolver import resolve_path as original_resolve_path

def path_resolver(path: str):

    # TODO: not handling "/gin?q=abc"
    if frappe.db.exists("Short Link", {"short_link": path}):
        short_link = frappe.db.get_value(
            "Short Link", {"short_link": path}, ["destination_url", "name"], as_dict=True
        )

        click = frappe.new_doc("Short Link Click")

        request_headers = frappe.request.headers
        click.ip = request_headers.get("X-Real-Ip")
        click.user_agent = request_headers.get("User-Agent")
        click.referrer = request_headers.get("Referer")

        click.link = short_link.name
        click.insert().submit()
        frappe.db.commit() # to remove once MyISAM

        frappe.redirect(short_link.destination_url)

    return original_resolve_path(path)    
