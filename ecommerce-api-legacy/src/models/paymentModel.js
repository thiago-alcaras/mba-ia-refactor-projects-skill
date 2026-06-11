const { runQuery } = require('./database');

class PaymentModel {
    async create(enrollmentId, amount, status) {
        const result = await runQuery(
            "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
            [enrollmentId, amount, status]
        );
        return result.lastID;
    }

    async findByEnrollment(enrollmentId) {
        const { getOne } = require('./database');
        return getOne("SELECT * FROM payments WHERE enrollment_id = ?", [enrollmentId]);
    }
}

module.exports = new PaymentModel();
