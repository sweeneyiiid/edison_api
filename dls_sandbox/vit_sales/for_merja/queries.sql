
/*ECS Sales */
select a.dt_acquisition, b.name_product, b.id_tier, c.name_province, count(*) as cnt
from 
    shs_ess a
    left join product b
        on a.id_product = b.id
    left join party c
        on a.id_customer = c.id
where a.id_esp = 3
group by 1,2,3,4






/*ECS default */
set @run_as_of_date := '2018-01-01';

select  
    case 
        when dt_paid_off is not null or 
            datediff(asof_dt, latest_payment) < 90 or 
            id_esp = 1
            then 1
        else 0
        end as active
    , tier
    , @run_as_of_date as rundt
    , case id_esp
        when 2 then "Fenix"
        when 1 then "Vitalite"
        when 3 then "ECS"
        when 4 then "SMG"
        else "BAD_NAME"
    end as name_company
    , name_province
    , count(*) as cnt
from (
    select
        ess.id
        , ess.id_esp 
        , ess.dt_acquisition
        , year(dt_acquisition) as yr
        , month(dt_acquisition) as mo
        , ess.payment_type as paytyp
        , ess.dt_paid_off
        , ess.nbr_plan_duration
        , datediff( @run_as_of_date , ess.dt_acquisition) as prev_term_days
        , nbr_plan_duration - datediff( @run_as_of_date , ess.dt_acquisition) as rem_term_days
        , ess.nbr_down_payment_zmw
        , ess.amt_purchase_financed_zmw
        , pg.max_pmt_bfr
        , coalesce(pg.max_pmt_bfr, ess.dt_acquisition) as latest_payment
        , pg.ttl_amt_paid_bfr
        , prd.name_product
        , prd.ext_key
        , tr.nbr_tier_level
        , coalesce(tr.nbr_tier_level,0) as tier
        , prty.name_province
        , cast( '{st}'  as date) as asof_dt        
        , coalesce(prty.text_gender, 'X') as gender
    from  shs_ess as ess 
        left join product prd 
            on ess.id_product = prd.id
        left join tier tr 
            on prd.id_tier = tr.id
        left join party as prty
            on ess.id_customer = prty.id
        left join (
            select 
                id_shs_ess
                , max(payment_date) as max_pmt_bfr
                , sum(payment_amount_zmw) as ttl_amt_paid_bfr
            from payg 
            where payment_date <  @run_as_of_date  
            group by id_shs_ess
            ) as pg
            on pg.id_shs_ess = ess.id
    where ess.dt_acquisition <  @run_as_of_date  
      and ess.id_esp=3 ) as main 
group by 1,2,3,4,5