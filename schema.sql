-- ============================================================
-- clothing: core item catalog
-- ============================================================
CREATE TABLE clothing (
    clothing_id  INT           NOT NULL AUTO_INCREMENT,
    name         VARCHAR(100)  NOT NULL,
    category     VARCHAR(50)   NOT NULL,  -- e.g. 'tops', 'bottoms', 'outerwear'
    gender       ENUM('mens','womens','unisex') NOT NULL DEFAULT 'unisex',
    base_price   DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (clothing_id)
);

INSERT INTO clothing (name, category, gender, base_price) VALUES
('Classic Crewneck Tee',     'tops',       'unisex',  19.99),
('Slim Fit Chinos',          'bottoms',    'mens',    59.99),
('Oversized Hoodie',         'tops',       'unisex',  64.99),
('High-Waist Flare Jeans',   'bottoms',    'womens',  79.99),
('Puffer Vest',              'outerwear',  'unisex',  89.99),
('Linen Button-Down Shirt',  'tops',       'mens',    49.99),
('A-Line Midi Skirt',        'bottoms',    'womens',  44.99),
('Trench Coat',              'outerwear',  'unisex', 139.99);


-- ============================================================
-- attributes: color + material combinations
-- ============================================================
CREATE TABLE attributes (
    attribute_id  INT          NOT NULL AUTO_INCREMENT,
    color         VARCHAR(50)  NOT NULL,
    material      VARCHAR(100) NOT NULL,
    hex_code      CHAR(7)      NULL,      -- optional display color, e.g. '#1A1A2E'
    PRIMARY KEY (attribute_id)
);

INSERT INTO attributes (color, material, hex_code) VALUES
('Midnight Black',  '100% Cotton',             '#1A1A1A'),
('Heather Gray',    '80% Cotton / 20% Polyester','#9E9E9E'),
('Navy Blue',       '100% Cotton',             '#1F3A6E'),
('Bone White',      '100% Linen',              '#F5F0E8'),
('Forest Green',    '100% Cotton',             '#2D5016'),
('Dusty Rose',      '95% Cotton / 5% Elastane','#C9A0A0'),
('Camel',           '70% Wool / 30% Polyester','#C19A6B'),
('Slate Blue',      'Stretch Denim',           '#6A80A0'),
('Rust Orange',     '100% Cotton',             '#B84A2A'),
('Cream',           '100% Linen',              '#FFF8E7');


-- ============================================================
-- clothing_attributes: join table linking items to variants
-- ============================================================
CREATE TABLE clothing_attributes (
    id            INT         NOT NULL AUTO_INCREMENT,
    clothing_id   INT         NOT NULL,
    attribute_id  INT         NOT NULL,
    stock_qty     INT         NOT NULL DEFAULT 0,
    sku           VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (id),
    FOREIGN KEY (clothing_id)  REFERENCES clothing(clothing_id)   ON DELETE CASCADE,
    FOREIGN KEY (attribute_id) REFERENCES attributes(attribute_id) ON DELETE CASCADE
);

INSERT INTO clothing_attributes (clothing_id, attribute_id, stock_qty, sku) VALUES
(1, 1, 120, 'TEE-MBLK-COT'),     -- Classic Tee / Midnight Black / Cotton
(1, 2,  85, 'TEE-HGRY-CPO'),     -- Classic Tee / Heather Gray / Cotton-Poly
(1, 5,  60, 'TEE-FGRN-COT'),     -- Classic Tee / Forest Green / Cotton
(2, 3,  40, 'CHN-NAVY-COT'),     -- Slim Chinos / Navy Blue / Cotton
(2, 7,  30, 'CHN-CAML-WPO'),     -- Slim Chinos / Camel / Wool-Poly
(3, 1,  75, 'HOD-MBLK-CPO'),     -- Oversized Hoodie / Midnight Black / Cotton-Poly
(3, 9,  50, 'HOD-RUST-COT'),     -- Oversized Hoodie / Rust Orange / Cotton
(4, 8,  55, 'FLR-SLBL-DNM'),     -- Flare Jeans / Slate Blue / Denim
(5, 7,  25, 'VST-CAML-WPO'),     -- Puffer Vest / Camel / Wool-Poly
(6, 4,  45, 'BTN-BONE-LIN'),     -- Linen Shirt / Bone White / Linen
(6, 10, 30, 'BTN-CREM-LIN'),     -- Linen Shirt / Cream / Linen
(7, 6,  35, 'SKT-DRSE-COE'),     -- Midi Skirt / Dusty Rose / Cotton-Elastane
(8, 7,  18, 'TCH-CAML-WPO');     -- Trench Coat / Camel / Wool-Poly