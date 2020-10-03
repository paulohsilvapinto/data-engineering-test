--Preparing tables
/*
CREATE TABLE PRICES (
	PRODUCT VARCHAR(12),
	PRICE_EFFECTIVE_DATE DATE,
	PRICE INTEGER
)
GO

CREATE TABLE SALES (
	PRODUCT VARCHAR(12),
	SALES_DATE DATE,
	QUANTITY INTEGER
)
GO

BEGIN
      SET NOCOUNT ON;
     
      SET DATEFORMAT DMY

      INSERT INTO prices VALUES 
		('product_1', '01/01/2018', 50),
		('product_2', '01/01/2018', 40),
		('product_1', '03/01/2018', 25),
		('product_2', '05/01/2018', 20),
		('product_1', '10/01/2018', 50),
		('product_2', '12/01/2018', 40);
     
	  INSERT INTO sales VALUES 
		('product_1', '01/01/2018', 10),
		('product_2', '02/01/2018', 12),
		('product_1', '04/01/2018', 50),
		('product_2', '06/01/2018', 70),
		('product_1', '12/01/2018', 8),
		('product_2', '15/01/2018', 9);
END
GO
*/


--Query
WITH ranked_prices AS (
	SELECT 
		product, 
		price_effective_date, 
		price,
		rownum = ROW_NUMBER() over (PARTITION BY product ORDER BY price_effective_date)
	FROM prices
),
prices_with_start_end AS (
	SELECT
	   product = rp_start.product,
	   price_effective_start_date = rp_start.price_effective_date,
	   price_effective_end_date = COALESCE(rp_end.price_effective_date, cast('9999-12-31' as date)),
	   price = rp_start.price
	FROM
	   ranked_prices AS rp_start
	   LEFT JOIN ranked_prices AS rp_end 
			ON rp_start.product = rp_end.product 
			AND rp_start.rownum+1 = rp_end.rownum
)

SELECT
  total_revenue = SUM(s.quantity * p.price)
FROM
  sales s
  INNER JOIN prices_with_start_end AS p 
	ON s.product = p.product
	   AND s.sales_date >= p.price_effective_start_date
	   AND s.sales_date < p.price_effective_end_date