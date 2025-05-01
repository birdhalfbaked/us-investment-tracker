import json
from jinja2 import Template

import datetime

status_classes = {
    "Announced": "bg-secondary",
    "In Progress": "bg-primary",
    "Complete": "bg-success",
    "Pullback": "bg-warning",
    "Layoffs": "bg-danger",
}


def money_to_string(amount: float) -> str:
    qualifier = "Thousand"
    if amount >= 1e9:
        qualifier = "Trillion"
        amount /= 1e9
    elif amount >= 1e6:
        qualifier = "Billion"
        amount /= 1e6
    elif amount >= 1e3:
        qualifier = "Million"
        amount /= 1e3
    elif amount <= 0:
        qualifier = ""
    return f"${round(amount, 2)} {qualifier}"



def main():
    total_promised = 0
    total_progress = 0
    generated_date = datetime.datetime.now(tz=datetime.timezone.utc)
    data = []
    with open("./data.json") as f:
        for record in json.load(f):
            total_promised += record["investment"]
            total_progress += record["progress"]
            record["percent_complete"] = round(record["progress"] / record["investment"], 2)*100
            record["investment_string"] = money_to_string(record["investment"])
            record["progress_string"] = money_to_string(record["progress"])
            record["status_class"] = status_classes[record["status"]]
            data.append(record)
    render_data = {
        "total_percent_completed": round(total_progress / total_promised, 1),
        "total_progress": money_to_string(total_progress),
        "total_promised": money_to_string(total_promised),
        "generated_date": generated_date.strftime("%B %d, %Y"),
        "rows": data
    }
    template = None
    with open("./index.j2") as f:
        template = Template(f.read())
    with open("./static/index.html", "w") as f:
        f.write(template.render(**render_data))


if __name__ == "__main__":
    main()
