drop trigger if exists delete_loan;

delimiter $$
	create trigger delete_loan after delete on loan
    for each row
    begin
        delete from apply where L_ID = old.L_ID;
    end $$
delimiter ;