from flask import Flask, request, jsonify
import random

app = Flask(__name__)

ORDERS = [
    "Order 1001: Buyer=John Davis, Location=Columbus, OH, Total=$742.10, Items: laptop, hdmi cable",
    "Order 1002: Buyer=Sarah Liu, Location=Austin, TX, Total=$156.55, Items: headphones",
    "Order 1003: Buyer=Mike Turner, Location=Cleveland, OH, Total=$1299.99, Items: gaming pc, mouse",
    "Order 1004: Buyer=Rachel Kim, Location=Seattle, WA, Total=$89.50, Items: coffee maker",
    "Order 1005: Buyer=Chris Myers, Location=Cincinnati, OH, Total=$512.00, Items: monitor, desk lamp",
    "Order 1006: Buyer=Amanda Foster, Location=Denver, CO, Total=$340.75, Items: keyboard, mouse pad",
    "Order 1007: Buyer=James Nguyen, Location=Chicago, IL, Total=$875.00, Items: tablet, stylus",
    "Order 1008: Buyer=Lisa Patel, Location=Houston, TX, Total=$224.99, Items: air purifier",
    "Order 1009: Buyer=David Okafor, Location=Columbus, OH, Total=$649.00, Items: smart tv",
    "Order 1010: Buyer=Emily Zhao, Location=Portland, OR, Total=$112.40, Items: desk organizer, pens",
    "Order 1011: Buyer=Ryan Thompson, Location=Nashville, TN, Total=$1850.00, Items: macbook, usb hub",
    "Order 1012: Buyer=Megan Brooks, Location=Toledo, OH, Total=$430.60, Items: blender, toaster",
    "Order 1013: Buyer=Kevin Martinez, Location=Phoenix, AZ, Total=$275.00, Items: standing desk converter",
    "Order 1014: Buyer=Tiffany Johnson, Location=Atlanta, GA, Total=$990.00, Items: camera, tripod",
    "Order 1015: Buyer=Brian Scott, Location=Akron, OH, Total=$567.80, Items: soundbar, remote",
    "Order 1016: Buyer=Natalie Green, Location=San Diego, CA, Total=$73.25, Items: electric kettle",
    "Order 1017: Buyer=Marcus Williams, Location=Dallas, TX, Total=$1125.50, Items: gaming console, controller",
    "Order 1018: Buyer=Sandra Lee, Location=Dayton, OH, Total=$389.99, Items: webcam, ring light",
    "Order 1019: Buyer=Tyler Adams, Location=Las Vegas, NV, Total=$215.00, Items: robot vacuum",
    "Order 1020: Buyer=Jasmine Carter, Location=Miami, FL, Total=$644.00, Items: noise cancelling headphones",
    "Order 1021: Buyer=Patrick Wilson, Location=Cleveland, OH, Total=$910.00, Items: ultrawide monitor",
    "Order 1022: Buyer=Diana Cruz, Location=Albuquerque, NM, Total=$158.75, Items: chair mat, cable organizer",
    "Order 1023: Buyer=Andre Robinson, Location=Charlotte, NC, Total=$2100.00, Items: video editing pc, capture card",
    "Order 1024: Buyer=Heather Young, Location=Youngstown, OH, Total=$775.40, Items: laptop stand, keyboard, mouse",
    "Order 1025: Buyer=Carlos Mendez, Location=San Antonio, TX, Total=$490.00, Items: espresso machine",
]


@app.route("/api/orders", methods=["GET"])
def get_orders():
    limit = request.args.get("limit", default=len(ORDERS), type=int)
    sample = random.sample(ORDERS, min(limit, len(ORDERS)))
    return jsonify({"status": "ok", "raw_orders": sample})


@app.route("/api/order/<order_id>", methods=["GET"])
def get_order_by_id(order_id):
    for text in ORDERS:
        if order_id in text:
            return jsonify({"status": "ok", "raw_order": text})
    return jsonify({"status": "not_found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)