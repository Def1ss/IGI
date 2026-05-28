from statistics import mean, median, mode


def build_statistics(
    avg_age,
    clients,
    workout_popularity,
    workout_profit,
    monthly_revenue,
):
    sales_values = [
        client["total_paid"]
        for client in clients
    ]

    return {
        "avg_age": avg_age,
        "median_age": median(
            [client["age"] for client in clients]
        ) if clients else 0,

        "total_sales": sum(sales_values),
        "avg_sales": mean(sales_values) if sales_values else 0,
        "mode_sales": mode(sales_values) if sales_values else 0,
        "median_sales": median(sales_values) if sales_values else 0,

        "clients": clients,
        "workout_popularity": workout_popularity,
        "workout_profit": workout_profit,
        "monthly_revenue": monthly_revenue,

        "total_profit": sum(
            item["profit"]
            for item in workout_profit
        )
    }