CREATE TABLE "Orders" (
    "DateTimePlaced" timestamp PRIMARY KEY,
    "EmployeeID" int,
    "Items" jsonb DEFAULT '[]'::jsonb,
    "Subtotal" numeric(28, 2),
    "Total" numeric(28, 2),
    "MenuItemsInOrder" jsonb DEFAULT '[]'::jsonb
);

GRANT ALL PRIVILEGES ON "Orders" TO csce315331_pusey;
GRANT ALL PRIVILEGES ON "Orders" TO csce315331_noyes;
GRANT ALL PRIVILEGES ON "Orders" TO csce315331_lee;
GRANT ALL PRIVILEGES ON "Orders" TO csce315331_gonce;
GRANT ALL PRIVILEGES ON "Orders" TO csce315331_fattig;