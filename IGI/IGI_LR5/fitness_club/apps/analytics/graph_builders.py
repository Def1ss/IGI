import io
import base64

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def build_popularity_graph(workout_popularity):
    names = [item["name"] for item in workout_popularity]
    counts = [item["clients_count"] for item in workout_popularity]

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(names, counts)

    ax.set_title("Популярность видов тренировок")
    ax.set_xlabel("Тип тренировки")
    ax.set_ylabel("Количество клиентов")

    buffer = io.BytesIO()

    plt.tight_layout()
    plt.savefig(buffer, format="png")

    image = base64.b64encode(
        buffer.getvalue()
    ).decode()

    plt.close(fig)

    return image


def build_revenue_graph(monthly_revenue):
    months = [item["month"] for item in monthly_revenue]
    amounts = [float(item["amount"]) for item in monthly_revenue]

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(months, amounts, marker="o")

    ax.set_title("Динамика доходов по месяцам")
    ax.set_xlabel("Месяц")
    ax.set_ylabel("Доход (BYN)")

    buffer = io.BytesIO()

    plt.tight_layout()
    plt.savefig(buffer, format="png")

    image = base64.b64encode(
        buffer.getvalue()
    ).decode()

    plt.close(fig)

    return image