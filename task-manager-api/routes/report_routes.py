from flask import Blueprint, jsonify
from controllers.report_controller import ReportController

report_bp = Blueprint('reports', __name__)
report_controller = ReportController()


@report_bp.route('/reports/summary', methods=['GET'])
def summary_report():
    result, status = report_controller.get_summary()
    return jsonify(result), status
