/*
存储过程 dissmiss, 删除员工信息
输入参数：员工编号
输出参数：msg 0: 不存在该员工编号 1: 删除成功
*/

drop procedure if exists dismiss;

-- 存储过程
delimiter $$

create procedure dismiss (
	in emp_id char(8)
)
begin
    start transaction;
        -- 删除员工
        delete from employee
            where employee.E_ID = emp_id;
        
        if exists(
            select * from 
            Department
            where Department.Manager_ID = emp_id
        ) then
            rollback;
        end if;
    commit;
end $$
delimiter ;