with base as (
select "Suburb" as suburbio,
		"Address" as direccion,
		"Rooms" as habitaciones,
		--"Bedroom2" as dormitorios_otras_fuentes,
		"Type" as tipo,
		"SellerG" as agente_inmobiliario,
		"Distance" as distancia_centro_km,
		cast("Postcode" as varchar) as codigo_postal,
		"Bathroom" as banios,
		case when "Bathroom" = 1 then '1'
			 when "Bathroom" = 2 then '2'
			 when "Bathroom" >= 3 then '+3' 
			 else 'desconocido' end as banios_cat,
		case when "Car" = 0 or "Car" is null then 'no tiene cochera'
			 when "Car" = 1 then '1'
			 when "Car" = 2 then '2'
			 when "Car" = 3 then '3'
			 when "Car" > 3 then '+4' end as cochera,
		case when "Landsize" = 0 then null else "Landsize" end as m2,
		"BuildingArea" as m2_construidos,
		"CouncilArea" as consejo_gob_area,
		coalesce("Lattitude", b.x) as x,
		coalesce("Longtitude", b.y) as y,
		"Regionname" as region,
		"Propertycount" as nro_prop_en_suburbio,
		--TO_CHAR(TO_DATE("Date", 'DD/MM/YYYY'), 'YYYYMM') AS fec_venta,
		--TO_CHAR(TO_DATE(cast("YearBuilt" as varchar), 'YYYY'), 'YYYY') as anio_construccion,
		COALESCE(EXTRACT(YEAR FROM TO_DATE("Date", 'DD/MM/YYYY'))::int - "YearBuilt", 0) AS dif_fechas,
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
  from melbourne a
  left join ubicaciones_scraping b on b.direccion_completa = a."Suburb"||', '||a."Address"||', '||cast(a."Postcode" as varchar)
 where 1 = 1
   and "Regionname" is not null
)
,	duplicados as (
select *, 
		suburbio ||  ', ' || direccion ||  ', ' || codigo_postal as direccion_completa,
		count(1) over(partition by direccion, suburbio) dir,
		count(x) over(partition by x, y) ubicacion
  from base
 where 1 = 1
   and x is not null
)
,	main as (
select *
  from duplicados
 where 1 = 1
   and ubicacion <= 1
   and dir = 1 
)
,	analisis_Banios_vs_Precios as (
select banios, avg(m2), count(1)
  from main
 where 1 = 1
 group by 1
HAVING COUNT(1) >= 40
 ORDER BY banios asc
)
,	filtro_banios as (
select suburbio, habitaciones, tipo, agente_inmobiliario,
		distancia_centro_km, codigo_postal, banios_cat, cochera, consejo_gob_area,
		region, nro_prop_en_suburbio, dif_fechas,metodo, x, y , m2, target
  from main
 where 1 = 1
   and (banios between 1 and 5)
    or banios is null
)
select *
  from filtro_banios
 where 1 = 1


 
