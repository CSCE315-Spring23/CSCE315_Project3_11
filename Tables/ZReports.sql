CREATE TABLE "ZReports" (
    "DateTimeGenerated" timestamp PRIMARY KEY,
    "Subtotal" numeric(28, 2),
    "Total" numeric(28, 2)
);

GRANT ALL PRIVILEGES ON "ZReports" TO csce315331_pusey;
GRANT ALL PRIVILEGES ON "ZReports" TO csce315331_noyes;
GRANT ALL PRIVILEGES ON "ZReports" TO csce315331_lee;
GRANT ALL PRIVILEGES ON "ZReports" TO csce315331_gonce;
GRANT ALL PRIVILEGES ON "ZReports" TO csce315331_fattig;