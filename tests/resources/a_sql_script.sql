

select id, from_address, to_address
from mails
where author = 'test';

delete received
where open_date < '20211212';