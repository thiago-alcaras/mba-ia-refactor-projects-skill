const userModel = require('../models/userModel');
const courseModel = require('../models/courseModel');
const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');
const auditModel = require('../models/auditModel');
const config = require('../config/settings');
const logger = require('../middlewares/logger');

class CheckoutController {
    async checkout(req, res, next) {
        try {
            const { username, email, password, course_id, card_number } = req.body;

            if (!username || !email || !course_id || !card_number) {
                return res.status(400).json({ error: "Missing required fields: username, email, course_id, card_number" });
            }

            // Find course
            const course = await courseModel.findActiveById(course_id);
            if (!course) {
                return res.status(404).json({ error: "Curso não encontrado" });
            }

            // Find or create user
            let user = await userModel.findByEmail(email);
            let userId;

            if (!user) {
                userId = await userModel.create(username, email, password || "default123");
            } else {
                userId = user.id;
            }

            // Process payment (simulated)
            const paymentStatus = card_number.startsWith("4") ? "PAID" : "DENIED";

            if (paymentStatus === "DENIED") {
                return res.status(400).json({ error: "Pagamento recusado" });
            }

            // Create enrollment
            const enrollmentId = await enrollmentModel.create(userId, course_id);

            // Record payment
            await paymentModel.create(enrollmentId, course.price, paymentStatus);

            // Audit log
            await auditModel.log(`Checkout curso ${course_id} por usuario ${userId}`);

            logger.info(`Checkout completed for user ${userId}, course ${course_id}`);

            res.status(200).json({
                msg: "Sucesso",
                enrollment_id: enrollmentId,
            });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new CheckoutController();
