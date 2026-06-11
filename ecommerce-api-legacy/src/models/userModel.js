const { runQuery, getOne, getAll } = require('./database');
const bcrypt = require('bcrypt');
const config = require('../config/settings');

class UserModel {
    async findByEmail(email) {
        return getOne("SELECT * FROM users WHERE email = ?", [email]);
    }

    async findById(id) {
        return getOne("SELECT id, name, email FROM users WHERE id = ?", [id]);
    }

    async create(name, email, password) {
        const hash = await bcrypt.hash(password, config.bcryptRounds);
        const result = await runQuery(
            "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
            [name, email, hash]
        );
        return result.lastID;
    }

    async verifyPassword(password, hash) {
        return bcrypt.compare(password, hash);
    }

    async delete(id) {
        // Delete related data first to maintain referential integrity
        const enrollments = await getAll("SELECT id FROM enrollments WHERE user_id = ?", [id]);
        for (const enr of enrollments) {
            await runQuery("DELETE FROM payments WHERE enrollment_id = ?", [enr.id]);
        }
        await runQuery("DELETE FROM enrollments WHERE user_id = ?", [id]);
        await runQuery("DELETE FROM users WHERE id = ?", [id]);
        return true;
    }
}

module.exports = new UserModel();
