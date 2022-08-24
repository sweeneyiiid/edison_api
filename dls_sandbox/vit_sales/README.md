# Match up Vitalite sales between Lumeter and Payg

### Prod sales from Lumeter

```
select
      a.ext_key as shs_key
    , a.id_esp
    , a.dt_acquisition
    , b.name_product
    , b.id_tier
    , c.name_province
    , c.ext_key as cust_key
from shs_ess a
    left join product b
        on a.id_product = b.id
    left join party c
        on a.id_customer = c.id
where a.id_esp = 1
```

Exported as pipe-delimited to: `./data/vit_prod_sales_20210218.psv`

### Payg records from  historical dump

See `get_vit_sales` in this directory.

### Key mapping

Gonna do in excel first to make sure I have a feel for it, then move to python.

Based on mapping from Joram at Paygee: `vitalite_reeep_contact_meter_mapping.csv`

So plan is:

 - group records into three types
  - Both, use payg
  - payg only
  - lumeter only
 - then stack datasets
 
But while in excel, do some spot checks to make sure the mappings make sense on individual records.

***Hmm, having some trouble in excel with mappings of ESS ext_key, maybe try customer***

Ok, customer mapping works, and I spot-checked in excel, it's the same guy.

***So rely on customer mappings instead of system mappings.***

### Venn Diagram

 1. Among Lumeter (prod db) systems, how many:
   - Do not have a customer match in the mapping (186 systems, but they are SHS)
   - Duplicate customers are there (1441, a bit more than I would like but not terrible)

So I think we can ignore the no matches, and the duplicates aren't a big problem, but need to make sure we deduplicate.  But I think that's fine, maybe just take the system with the max tier level and assign it to all matches to be most generous to ESP.

 2. Among Lumeter systems with a customer match, how many records do not have paygee records, and what systems are they (2417, and they are SHS)

***So we need to decide whether to count all these as paid off, defaulted, or what***

***Also, what about payg without Lumeter, is that just recent sales, or does that include maybe some of the systems above, but with bad matches ***

***If numbers are similar with older systems in payg, may just drop non-matched lumeter systems ***
 
So the issues in (2) are not small enough to ignore, but we do have a large overlap.  Before we get to the overlap though, let's go back and look at 

 4. Among lumeter and payg overlap, 


