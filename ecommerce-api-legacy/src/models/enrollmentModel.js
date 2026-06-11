const { runQuery, getOne, getAll } = require('./database');

class EnrollmentModel {
    async create(userId, courseId) {
        const result = await runQuery(
            "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
            [userId, courseId]
        );
        return result.lastID;
    }

    async findByCourse(courseId) {
        return getAll("SELECT * FROM enrollments WHERE course_id = ?", [courseId]);
    }

    async getEnrollmentWithDetails(enrollmentId) {
        return getOne(`
            SELECT e.*, u.name as user_name, u.email as user_email, 
                   p.amount, p.status as payment_status
            FROM enrollments e
            LEFT JOIN users u ON u.id = e.user_id
            LEFT JOIN payments p ON p.enrollment_id = e.id
            WHERE e.id = ?
        `, [enrollmentId]);
    }
}

module.exports = new EnrollmentModel();
