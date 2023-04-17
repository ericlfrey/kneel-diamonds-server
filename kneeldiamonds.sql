CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Orders` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal_id` INTEGER NOT NULL,
    `size_id` INTEGER NOT NULL, 
    `style_id`INTEGER NOT NULL,
    `jewelry_id` INTEGER NOT NULL,
    `timestamp` INTEGER NOT NULL,
    FOREIGN KEY(`metal_id`) REFERENCES `Metals`(`id`),
    FOREIGN KEY(`size_id`) REFERENCES `Sizes`(`id`),
    FOREIGN KEY(`style_id`) REFERENCES `Styles`(`id`)
);

CREATE TABLE `Sizes` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` INTEGER NOT NULL,
    `price` INTEGER NOT NULL
);

CREATE TABLE `Styles` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style` TEXT NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

INSERT INTO `Metals`VALUES (null, "Sterling Silver", 12.42);
INSERT INTO `Metals`VALUES (null, "14K Gold", 736.4);
INSERT INTO `Metals`VALUES (null, "24K Gold", 1258.9);
INSERT INTO `Metals`VALUES (null, "Platinum", 795.45);
INSERT INTO `Metals`VALUES (null, "Palladium", 1241);

INSERT INTO `Sizes` VALUES (null, 0.5, 405);
INSERT INTO `Sizes` VALUES (null, 0.75, 782);
INSERT INTO `Sizes` VALUES (null, 1, 1470);
INSERT INTO `Sizes` VALUES (null, 1.5, 1997);
INSERT INTO `Sizes` VALUES (null, 2, 3638);

INSERT INTO `Styles` VALUES (null, "Classic", 500);
INSERT INTO `Styles` VALUES (null, "Modern", 710);
INSERT INTO `Styles` VALUES (null, "Vintage", 965);

INSERT INTO `Orders` VALUES (null, 1, 1, 1, 1, 11111);
INSERT INTO `Orders` VALUES (null, 2, 2, 2, 2, 22222);
INSERT INTO `Orders` VALUES (null, 3, 3, 3, 3, 33333);
INSERT INTO `Orders` VALUES (null, 4, 4, 1, 4, 44444);
INSERT INTO `Orders` VALUES (null, 5, 5, 2, 5, 55555);

SELECT
    o.id,
    o.metal_id,
    o.size_id,
    o.style_id,
    o.jewelry_id,
    o.timestamp
FROM orders o 
WHERE o.id = 2

SELECT * FROM Orders

SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.jewelry_id,
            o.timestamp,
            m.metal metal_name,
            m.price metal_price,
            sz.carets size_carets,
            sz.price size_price,
            st.style style_name,
            st.price style_price
        FROM Orders o
        JOIN Metals m
            ON m.id = o.metal_id
        JOIN Sizes sz
            ON sz.id = o.size_id
        JOIN Styles st
            ON st.id = o.style_id
