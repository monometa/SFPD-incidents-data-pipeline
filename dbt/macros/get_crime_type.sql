 {#
    This macro returns the type of crime in relation to person/property 
#}

{% macro get_crime_type(crime) -%}

    case {{ crime }}
        when Incident_Category = 'Larceny Theft' then 'Crime against property'
        when Incident_Category = 'Assault' then 'Crime against persons' -- Нападение
        when Incident_Category = 'Burglary' then 'Crime against property' -- Ограбление
        when Incident_Category = 'Motor Vehicle Theft' then 'Crime against property'
        when Incident_Category = 'Robbery' then 'Crime against property' -- Мошенничество 
    end

{%- endmacro %}
