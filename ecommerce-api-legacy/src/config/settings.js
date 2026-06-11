const config = {
    dbUser: process.env.DB_USER || "admin_dev",
    dbPass: process.env.DB_PASSWORD || "change-in-production",
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || "pk_test_placeholder",
    smtpUser: process.env.SMTP_USER || "no-reply@example.com",
    port: parseInt(process.env.PORT || "3000"),
    bcryptRounds: parseInt(process.env.BCRYPT_ROUNDS || "10"),
};

module.exports = config;
