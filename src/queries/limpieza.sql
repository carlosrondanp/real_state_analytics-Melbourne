select * from melbourne_price_less limit 100 ;
select * from melbourne limit 100 ;
select "CouncilArea", count(1)
  from melbourne_price_less 
 group by 1 
 order by 2 desc
 ;

with base as (
select *,
		TO_CHAR(TO_DATE("Date", 'DD/MM/YYYY'), 'YYYYMM') AS fec_venta,
		TO_CHAR(TO_DATE(cast("YearBuilt" as varchar), 'YYYY'), 'YYYY') as anio_construccion,
		case when trim("Method") = 'S' then 'prop_vendida'
			 when trim("Method") = 'SP' then 'prop_vendida_prev'
			 when trim("Method") = 'PI' then 'prop_transferida'
			 when trim("Method") = 'PN' then 'vendida_prev_no_divulgada'
			 when trim("Method") = 'SN' then 'vendida_no_divulgada'
			 when trim("Method") = 'VB' then 'puja_del_vendedor'
			 when trim("Method") = 'W' then 'retirada_antes_subasta'
			 when trim("Method") = 'SA' then 'vendida_despues_subasta'
			 when trim("Method") = 'SS' then 'vendida_despues_subasta_no_divulgada'
			 else 'otro' end as metodo,
		"Price" as target
  from melbourne
 where 1 = 1
   and "Price" is not null
   and "Regionname" is not null
),
	medianas_precios as (
select  metodo,
		percentile_disc(0.25) WITHIN GROUP (ORDER BY "Price" ) percentile_25,
		percentile_disc(0.5) WITHIN GROUP (ORDER BY "Price" ) percentile_50,
		percentile_disc(0.75) WITHIN GROUP (ORDER BY "Price" ) percentile_75,
		percentile_disc(0.90) WITHIN GROUP (ORDER BY "Price" ) percentile_90,
		count(1) cantidad
  from base
 group by 1
),
	media_precios as (
select anio_construccion, cast(avg("Price") as decimal(18,0)) precio_promedio , count(1) cantidad
  from base
 group by 1
 order by 1 asc
)
select *
  from base
 where 1 = 1
   and "Bathroom" is null
   and "Landsize" is null

   
-- 27,244
-- area construida nula : 16,588
-- area construida no bula : 10,656


 
