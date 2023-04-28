CREATE TABLE "MenuItems" (
    "ItemName" text PRIMARY KEY,
    "Price" numeric(28, 2),
    "DefiniteItems" jsonb DEFAULT '[]'::jsonb,
    "PossibleItems" jsonb DEFAULT '[]'::jsonb,
    "Image" bytea
);

GRANT ALL PRIVILEGES ON "MenuItems" TO csce315331_pusey;
GRANT ALL PRIVILEGES ON "MenuItems" TO csce315331_noyes;
GRANT ALL PRIVILEGES ON "MenuItems" TO csce315331_lee;
GRANT ALL PRIVILEGES ON "MenuItems" TO csce315331_gonce;
GRANT ALL PRIVILEGES ON "MenuItems" TO csce315331_fattig;