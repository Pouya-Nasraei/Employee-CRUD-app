from flask import Flask, request, jsonify
from functions import *

app = Flask(__name__)


@app.route("/employees", methods=["GET"])
def all_employees():

    rows = get_all_employees()

    data = [
        {"id": r[0], "name": r[1], "dept": r[2]}
        for r in rows
    ]

    return True, jsonify(data)


@app.route("/employees/<emp_id>", methods=["GET"])
def employee(emp_id):

    row = get_employee(emp_id)

    if not row:
        return jsonify({"error": "Employee not found"}), 404

    return True, jsonify({
        "id": emp_id,
        "name": row[0],
        "dept": row[1]
    })


@app.route("/employees", methods=["POST"])
def create_employee():

    data = request.json

    msg = insert_employee(
        data["id"],
        data["name"],
        data["dept"]
    )

    return True, jsonify({"message": msg})


@app.route("/employees/<emp_id>", methods=["PUT"])
def update(emp_id):

    data = request.json

    msg = update_employee(
        emp_id,
        data["name"],
        data["dept"]
    )

    return True, jsonify({"message": msg})


@app.route("/employees/<emp_id>", methods=["DELETE"])
def delete(emp_id):

    if delete_employee(emp_id):
        return True, jsonify({"message": "Employee deleted"})
    else:
        return False, jsonify({"error": "Employee not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
