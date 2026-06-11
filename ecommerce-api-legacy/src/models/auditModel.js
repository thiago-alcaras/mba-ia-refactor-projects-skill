const { runQuery } = require('./database');

class AuditModel {
    async log(action) {
        await runQuery(
            "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
            [action]
        );
    }
}

module.exports = new AuditModel();
