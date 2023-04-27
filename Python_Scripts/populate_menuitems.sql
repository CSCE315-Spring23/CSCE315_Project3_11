INSERT INTO "MenuItems" ("ItemName", "Price", "DefiniteItems", "PossibleItems") 
VALUES ('Gyro', 8.09, to_jsonb(ARRAY['Bowl']), to_jsonb(ARRAY['Shredded Lettuce', 'Spinach', 'Brown Rice', 'White Rice', 'Chicken', 'Lamb', 'Beef', 'Pork', 'Couscous', 'Onions', 'Big Tomatoes', 'Vegetable Medley', 'Olives', 'Pickled Onions', 'Cucumbers', 'Cauliflower', 'Peppers', 'Red Cabbage Coleslaw', 'Garlic Fries', 'Jalapeno Feta', 'Tzatziki', 'Greek Vinaigrette', 'Harrisa Yogurt', 'Dill Yogurt', 'Tahini']));
INSERT INTO "MenuItems" ("ItemName", "Price", "DefiniteItems", "PossibleItems") 
VALUES ('Bowl', 8.09, to_jsonb(ARRAY['Bowl', 'Bowl Lid', 'Utensil Pack']), to_jsonb(ARRAY['Shredded Lettuce', 'Spinach', 'Brown Rice', 'White Rice', 'Chicken', 'Lamb', 'Beef', 'Pork', 'Couscous', 'Onions', 'Big Tomatoes', 'Vegetable Medley', 'Olives', 'Pickled Onions', 'Cucumbers', 'Cauliflower', 'Peppers', 'Red Cabbage Coleslaw', 'Garlic Fries', 'Jalapeno Feta', 'Tzatziki', 'Greek Vinaigrette', 'Harrisa Yogurt', 'Dill Yogurt', 'Tahini']));
INSERT INTO "MenuItems" ("ItemName", "Price", "DefiniteItems", "PossibleItems") 
VALUES ('Hummus & Pita', 3.49, to_jsonb(ARRAY['Bowl', 'Pita Chips']), to_jsonb(ARRAY['Hummus', 'Spicy Hummus']));
INSERT INTO "MenuItems" ("ItemName", "Price", "DefiniteItems") 
VALUES ('Falafels', 3.49, to_jsonb(ARRAY['Bowl', 'Falafel']));
INSERT INTO "MenuItems" ("ItemName", "Price", "PossibleItems") 
VALUES ('Extra Protein', 2.49, to_jsonb(ARRAY['Chicken', 'Lamb', 'Beef', 'Pork']));
INSERT INTO "MenuItems" ("ItemName", "Price", "PossibleItems") 
VALUES ('Extra Dressing', 0.39, to_jsonb(ARRAY['Jalapeno Feta', 'Tzatziki', 'Greek Vinaigrette', 'Harrisa Yogurt', 'Dill Yogurt', 'Tahini']));
INSERT INTO "MenuItems" ("ItemName", "Price", "DefiniteItems", "PossibleItems") 
VALUES ('Fountain Drink', 2.45, to_jsonb(ARRAY['Cup Drink', 'Cup Lid', 'Straw']), to_jsonb(ARRAY['Pepsi', 'Sierra Mist', 'Brisk', 'Pepsi Zero', 'Diet Pepsi', 'Gatorade', 'Mtn Dew', 'Dr. Pepper']));