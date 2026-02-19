import numpy as np
from sklearn.linear_model import LinearRegression

# order totals in sequence from 1001 to 1025
ORDER_TOTALS = [
    742.10, 156.55, 1299.99, 89.50, 512.00,
    340.75, 875.00, 224.99, 649.00, 112.40,
    1850.00, 430.60, 275.00, 990.00, 567.80,
    73.25, 1125.50, 389.99, 215.00, 644.00,
    910.00, 158.75, 2100.00, 775.40, 490.00,
]


def train_and_predict() -> dict:
    X = np.array(range(1, len(ORDER_TOTALS) + 1)).reshape(-1, 1)
    y = np.array(ORDER_TOTALS)

    model = LinearRegression()
    model.fit(X, y)

    predicted = model.predict([[len(ORDER_TOTALS) + 1]])[0]
    predicted = max(0, predicted)  # totals can't be negative

    return {
        "predicted_next_order": round(predicted, 2),
        "trend": "upward 📈" if model.coef_[0] > 0 else "downward 📉",
        "average_order_total": round(float(np.mean(y)), 2),
        "r_squared": round(model.score(X, y), 3),
        "orders_analyzed": len(ORDER_TOTALS),
    }


if __name__ == "__main__":
    r = train_and_predict()
    print(f"Predicted next order: ${r['predicted_next_order']}")
    print(f"Trend: {r['trend']}")
    print(f"Average: ${r['average_order_total']}")
    print(f"R²: {r['r_squared']}")