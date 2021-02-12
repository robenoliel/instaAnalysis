select * from posts where date > 
	(select max(date) from 
		(select min(date) as date from 
			(select * from posts where username <> 'ieeeuerj'
			)  as wished group by username
        ) as minDates
	);

select min(date), username as date from posts group by username;