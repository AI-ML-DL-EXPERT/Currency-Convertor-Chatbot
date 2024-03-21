from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    data = request.get_json()
    source_currency = data["queryResult"]["parameters"]["unit-currency"]["currency"]
    amount = data["queryResult"]["parameters"]["unit-currency"]["amount"]
    target_currency = data["queryResult"]["parameters"]["currency-name"]

    # print(source_currency)
    # print(amount)
    # print(target_currency)

    cf = FetchConversionFactor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount, 2)
    response = {
        "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
    }

    # print(final_amount)
    return jsonify(response)


def FetchConversionFactor(source, target):
    url = f"https://free.currconv.com/api/v7/cpnvrt?q={source}_{target}&compact=ultra&apiKey=9aa0c54f5ad4c460c36d"

    response = requests.get(url)
    response = response.json()

    # print(response)
    return response[f"{source}_{target}"]


if __name__ == "__main__":
    app.run(debug=True)
