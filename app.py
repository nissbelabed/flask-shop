from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# ===============================
# Supabase config
# ===============================
SUPABASE_URL = "https://psmpoqdhaekaubsrfmek.supabase.co"
API_KEY = "sb_publishable_aGuiUV1yowVGv1PfK8hf1g_rmUQ8Lwt"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}


# ===============================
# Login
# ===============================
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()

        url = f"{SUPABASE_URL}/rest/v1/Users?name=ilike.*{username}*&select=*"
        r = requests.get(url, headers=HEADERS)

        if r.status_code == 200 and len(r.json()) > 0:
            return redirect(url_for("categories"))
        else:
            message = "❌ Access denied"

    return render_template("login.html", message=message)


# ===============================
# Categories
# ===============================
@app.route("/categories")
def categories():
    url = f"{SUPABASE_URL}/rest/v1/categories?select=*"
    r = requests.get(url, headers=HEADERS)
    categories = r.json() if r.status_code == 200 else []

    return render_template("categories.html", categories=categories)


# ===============================
# Products by category
# ===============================
@app.route("/products/<int:category_id>")
def products(category_id):
    url = (
        f"{SUPABASE_URL}/rest/v1/products"
        f"?category_id=eq.{category_id}&select=*"
    )

    r = requests.get(url, headers=HEADERS)
    products = r.json() if r.status_code == 200 else []

    return render_template("products.html", products=products)


# ===============================
# Run app
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

