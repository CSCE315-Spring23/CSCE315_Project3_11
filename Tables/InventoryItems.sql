CREATE TABLE "InventoryItems" (
    "Name" text PRIMARY KEY,
    "Stock" int,
    "NumberNeeded" int,
    "OrderChance" numeric(28, 2),
    "Units" text,
    "Category" text,
    "Servings" int,
    "RestockCost" int,
    "Image" bytea
);

GRANT ALL PRIVILEGES ON "InventoryItems" TO csce315331_pusey;
GRANT ALL PRIVILEGES ON "InventoryItems" TO csce315331_noyes;
GRANT ALL PRIVILEGES ON "InventoryItems" TO csce315331_lee;
GRANT ALL PRIVILEGES ON "InventoryItems" TO csce315331_gonce;
GRANT ALL PRIVILEGES ON "InventoryItems" TO csce315331_fattig;