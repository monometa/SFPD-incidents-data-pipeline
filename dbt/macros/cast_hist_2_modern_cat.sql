 {#
    -- This macro returns the type of crime in relation to person/property 
#}

{% macro cast_hist_2_modern_cat(Category) -%}

    case {{ Category }}
        when Incident_Category = 'Larceny/Theft' then 'Larceny Theft' 
        when Incident_Category = 'Drug/Narcotic' then 'Drug Offense'
        when Incident_Category = 'Vehicle Theft' then 'Motor Vehicle Theft'
        ELSE Incident_Category
    end

{%- endmacro %}
