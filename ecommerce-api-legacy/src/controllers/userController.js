const userModel = require('../models/userModel');
const logger = require('../middlewares/logger');

class UserController {
    async deleteUser(req, res, next) {
        try {
            const userId = req.params.id;
            await userModel.delete(userId);
            logger.info(`User ${userId} deleted with all related data`);
            res.json({ message: "Usuário e dados relacionados deletados com sucesso" });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new UserController();
