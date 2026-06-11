const { runQuery, getOne, getAll } = require('./database');

class CourseModel {
    async findActiveById(courseId) {
        return getOne("SELECT * FROM courses WHERE id = ? AND active = 1", [courseId]);
    }

    async getAll() {
        return getAll("SELECT * FROM courses");
    }
}

module.exports = new CourseModel();
