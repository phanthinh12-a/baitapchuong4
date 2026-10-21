from datetime import datetime
from flask import Flask, render_template, request, abort

app = Flask(__name__)

SHOP = {"name": "Cà phê Sông Hương",
        "address": "12 Lê Lợi, Huế",
        "phone": "0234 3888 999",
        "open": 7, "close": 22}

PROMOTIONS = ["Giảm 10% cho sinh viên",
              "Mua 2 tặng 1 vào Thứ Hai"]

MENU = [
    {"id": 1, "name": "cà phê đen",  "price": 20000, "image": "ca-phe-den.jpg"},
    {"id": 2, "name": "cà phê sữa",  "price": 25000, "image": "ca-phe-sua.jpg"},
    {"id": 3, "name": "bạc xỉu",     "price": 27000, "image": "bac-xiu.jpg"},
    {"id": 4, "name": "trà đào",     "price": 30000, "image": "tra-dao.jpg"},
    {"id": 5, "name": "trà sữa",     "price": 32000, "image": "tra-sua.jpg"},
    {"id": 6, "name": "nước cam",    "price": 28000, "image": "nuoc-cam.jpg"},
    {"id": 7, "name": "sinh tố bơ",  "price": 35000, "image": "sinh-to-bo.jpg"},
]

PER_PAGE = 3


@app.template_filter("vnd")
def vnd(value):
    """25000 -> '25.000 đ'"""
    return f"{value:,.0f}".replace(",", ".") + " đ"


@app.context_processor
def inject_shop():
    return {"shop": SHOP}


@app.get("/")
def index():
    hour = request.args.get("gio", type=int)
    if hour is None:
        hour = datetime.now().hour
    is_open = SHOP["open"] <= hour < SHOP["close"]
    return render_template("index.html", hour=hour, is_open=is_open,
                           promotions=PROMOTIONS)


@app.get("/menu")
def menu():
    # page=abc -> type=int thất bại -> dùng mặc định 1
    page = request.args.get("page", 1, type=int)
    total = len(MENU)
    pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)   # 7 món -> 3 trang

    if page < 1 or page > pages:
        abort(404)

    start = (page - 1) * PER_PAGE
    items = MENU[start:start + PER_PAGE]
    return render_template("menu.html", items=items, page=page,
                           pages=pages, total=total)


@app.get("/contact")
def contact():
    return render_template("contact.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)