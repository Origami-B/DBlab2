drop function if exists total_asset;

delimiter $$

create function total_asset () returns int
READS SQL DATA
begin
    declare total int;
    select sum(Assets) into total from Bank;
    return total;
end $$

delimiter ;