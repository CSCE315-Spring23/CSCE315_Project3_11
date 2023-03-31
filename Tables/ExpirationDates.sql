CREATE TABLE "ExpirationDates" (
    "UniqueID" int PRIMARY KEY,
    "ItemName" text,
    "ExpirationDate" timestamp,
    "RemainingServings" int
);

GRANT ALL PRIVILEGES ON "ExpirationDates" TO csce315331_pusey;
GRANT ALL PRIVILEGES ON "ExpirationDates" TO csce315331_noyes;
GRANT ALL PRIVILEGES ON "ExpirationDates" TO csce315331_lee;
GRANT ALL PRIVILEGES ON "ExpirationDates" TO csce315331_gonce;
GRANT ALL PRIVILEGES ON "ExpirationDates" TO csce315331_fattig;