CREATE TABLE "Employees" (
    "EmployeeID" int PRIMARY KEY,
    "LastName" text,
    "FirstName" text,
    "HireDate" date,
    "EmployeePIN" int,
    "PositionTitle" text,
    "HoursWorked" numeric(28, 2)
);

GRANT ALL PRIVILEGES ON "Employees" TO csce315331_pusey;
GRANT ALL PRIVILEGES ON "Employees" TO csce315331_noyes;
GRANT ALL PRIVILEGES ON "Employees" TO csce315331_lee;
GRANT ALL PRIVILEGES ON "Employees" TO csce315331_gonce;
GRANT ALL PRIVILEGES ON "Employees" TO csce315331_fattig;