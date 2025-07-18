{{ config(
    materialized='incremental'
) }}

with clients as (
    select
        client_id,
        dob,
        gender,
        district_id
    from 
        {{ source('silver_zone', 'clients') }}
),

accounts as (
    select
        account_id,
        district_id,
        date as created_date
    from
        {{ source('silver_zone', 'accounts') }}
),

dispositions as (
    select
        client_id,
        account_id,
        type
    from 
        {{ source('silver_zone', 'disps') }}
),
districts as (
    select
        district_id,
        district_name,
        region
    from
        {{ source('silver_zone', 'districts') }}
)

SELECT
    c.client_id,
    a.account_id,
    a.created_date,
    c.gender,
    c.dob,
    dt.district_name,
    dt.region,
    dp.type as disposition_type
FROM
    clients c
        left join dispositions dp on c.client_id=dp.client_id
        left join accounts a on dp.account_id=a.account_id
        left join districts dt on c.district_id=dt.district_id  
	