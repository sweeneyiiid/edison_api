# Get vitalite products from historical dump

 - get list and check
 - compare against earlier work on [ROCKS](https://rocks.reeep.org/display/NERD/Vitalite+Products)
 - load to DB (should be able to do from DBVisualizer)
 
### Vitalite products in historical dump

From `get_vit_products.py`

```
{
 'LG K10 System', 
 'Samsung Galaxy J7 Neo',
 'Lighting Plus BCU',
 'Spark20 BCU',
 'Solo Aspire 4 System',
 'fosera legacy system',
 'Entertainment Plus BCU',
 'Samsung Galaxy Grand Prime+ System',
 'Basic Entertainment BCU'
}
```

### inserting rows into product table

See [Vitalite integration ROCKS page](https://rocks.reeep.org/display/NERD/Vitalite+Products) for determining how to set up rows.

```
INSERT INTO 
	product(ext_id, id_tier, name_product, nbr_lights, nbr_wh_max, nbr_wh_min, nbr_wt_peak, product_type, id_esp, ext_key, verified)
VALUES
    ('vit_man_add_1', 1, 'Lighting Plus BCU', 3, 26, 0, 6, 'SHS', 3,'Lighting Plus BCU', TRUE),
    ('vit_man_add_2', 2, 'Basic Entertainment BCU', 3, 84, 0, 20, 'SHS', 3,'Basic Entertainment BCU', TRUE),
    ('vit_man_add_3', 3, 'Entertainment Plus BCU', 4, 205, 0, 50, 'SHS', 3,'Entertainment Plus BCU', TRUE),
    ('vit_man_add_4', 1, 'fosera legacy system', 3, 26, 0, 6, 'SHS', 3,'fosera legacy system', TRUE),
    ('vit_man_add_5', 1, 'Spark20 BCU', 2, 26, 0, 6, 'SHS', 3,'Spark20 BCU', TRUE)
```


