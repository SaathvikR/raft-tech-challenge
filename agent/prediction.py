import numpy as np
from sklearn.linear_model import LinearRegression

# All 25 order totals in sequence (order 1001 -> 1025)
ORDER_TOTALS = [
    742.10, 156.55, 1299.99, 89.50, 512.00,
    340.75, 875.00, 224.99, 649.00, 112.40,
    1850.00, 430.60, 275.00, 990.00, 567.80,
    73.25, 1125.50, 389.99, 215.00, 644.00,
    910.00, 158.75, 2100.00, 775.40, 490.00,
]


def train_and_predict() -> dict:
    """
    Train a linear regression model on order totals over time
    and predict the next order value.
    """
    X = np.array(range(1, len(ORDER_TOTALS) + 1)).reshape(-1, 1)
    y = np.array(ORDER_TOTALS)

    model = LinearRegression()
    model.fit(X, y)

    next_order_num = len(ORDER_TOTALS) + 1
    predicted = model.predict([[next_order_num]])[0]
    predicted = max(0, predicted)

    r_squared = model.score(X, y)
    avg = float(np.mean(y))
    trend = "upward 📈" if model.coef_[0] > 0 else "downward 📉"

    return {
        "predicted_next_order": round(predicted, 2),
        "trend": trend,
        "average_order_total": round(avg, 2),
        "r_squared": round(r_squared, 3),
        "orders_analyzed": len(ORDER_TOTALS),
    }


if __name__ == "__main__":
    result = train_and_predict()
    print(f"Predicted next order value: ${result['predicted_next_order']}")
    print(f"Trend: {result['trend']}")
    print(f"Average order total: ${result['average_order_total']}")
    print(f"R² score: {result['r_squared']}")