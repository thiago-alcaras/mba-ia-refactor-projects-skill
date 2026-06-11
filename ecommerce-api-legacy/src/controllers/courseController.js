const courseModel = require('../models/courseModel');
const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');
const { getAll } = require('../models/database');
const logger = require('../middlewares/logger');

class CourseController {
    async getFinancialReport(req, res, next) {
        try {
            const courses = await courseModel.getAll();
            const report = [];

            for (const course of courses) {
                const courseData = { course: course.title, revenue: 0, students: [] };

                const enrollments = await enrollmentModel.findByCourse(course.id);

                for (const enrollment of enrollments) {
                    const details = await getAll(`
                        SELECT u.name, p.amount, p.status
                        FROM users u
                        LEFT JOIN payments p ON p.enrollment_id = ?
                        WHERE u.id = ?
                    `, [enrollment.id, enrollment.user_id]);

                    if (details.length > 0) {
                        const detail = details[0];
                        if (detail.status === 'PAID') {
                            courseData.revenue += detail.amount || 0;
                        }
                        courseData.students.push({
                            student: detail.name || 'Unknown',
                            paid: detail.amount || 0,
                        });
                    }
                }

                report.push(courseData);
            }

            res.json(report);
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new CourseController();
