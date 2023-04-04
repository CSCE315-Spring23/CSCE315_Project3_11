CREATE TABLE "RestockOrders" (
    "DateOrdered" date PRIMARY KEY,
    "DateReceived" date,
    "Items" jsonb DEFAULT '[]'::jsonb,
    "Cost" numeric(28, 2)
);

GRANT ALL PRIVILEGES ON "RestockOrders" TO csce315331_pusey;
GRANT ALL PRIVILEGES ON "RestockOrders" TO csce315331_noyes;
GRANT ALL PRIVILEGES ON "RestockOrders" TO csce315331_lee;
GRANT ALL PRIVILEGES ON "RestockOrders" TO csce315331_gonce;
GRANT ALL PRIVILEGES ON "RestockOrders" TO csce315331_fattig;