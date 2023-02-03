# Ticketing SQL Query
SELECT true_case_id,
    dates.date,
    tickets.status,
    tickets.sim_issue_alias,
    CONVERT_TIMEZONE('US/Pacific', tickets.create_date) AS create_date,
    tickets.impact,
    tickets.min_impact,
    CONVERT_TIMEZONE('US/Pacific', tickets.resolved_date) AS resolved_date,
    tickets.assigned_to_individual,
    tickets.root_cause,
    tickets.category,
    tickets.type,
    tickets.item,
    tickets.assigned_to_group,
    tickets.requester_login,
    tickets.resolved_by,
    tickets.item as classification
FROM aim.o_remedy_sim_tickets AS tickets
    LEFT JOIN booker.dates as dates ON dates.date >= trunc(tickets.create_date)
        AND dates.date <= CASE WHEN tickets.resolved_date IS NULL THEN trunc(current_date)
                        WHEN trunc(tickets.resolved_date) < trunc(current_date) THEN trunc(tickets.resolved_date)
                        ELSE trunc(tickets.resolved_date) END
        OR dates.date = CASE WHEN trunc(tickets.resolved_date) = trunc(tickets.create_date) THEN trunc(tickets.resolved_date)
                        END
    JOIN (
        SELECT DISTINCT CASE
                WHEN sim_migration_status = 1 THEN j.case_id
                WHEN sim_migration_status = 0 AND t.is_sim = 'FALSE' THEN j.sim_issue_guid
                ELSE t.case_id
            END AS true_case_id
        FROM aim.o_remedy_sim_tickets AS t
            LEFT JOIN booker.SIM_TT_ARCHIVE j ON (j.case_id = t.case_id)
        WHERE ((category = 'AWS-ACE-OpticsSupport' and type = 'Configuration'))
	        AND t.create_date >= '2021-01-01'
    ) trueid_table ON trueid_table.true_case_id = tickets.case_id