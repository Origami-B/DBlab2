use bank;

drop table if exists User;

drop table if exists Account;

drop table if exists Apply;

drop table if exists Bank;

drop table if exists Credit_Account;

drop table if exists Client;

drop table if exists Checking;

drop table if exists Department;

drop table if exists Employee;

drop table if exists Loan;

drop table if exists Own;

drop table if exists Payment;

drop table if exists Saving_Account;


/* 
User: 用户表
      username: 用户名
      userkey: 密码
*/
create table User
(
      username varchar(50) not null,
      userkey varchar(50) not null,
      primary key (username)
);

/*
Bank: 支行表
      B_ID: 支行ID
      B_Name: 支行名
      City: 所在城市
      Assets: 资产

*/
create table Bank(
      B_ID			int not null,
      B_Name       varchar(50) not null,
      City         varchar(50) not null,
      Assets       float(15) not null,
      primary key (B_Name),
      unique key AK_B_ID (B_ID)
);

/*
Apartment: 部门表
      D_ID: 部门ID
      D_Name: 部门名
      Manager_ID: 部门经理ID

*/
create table Department
(
      D_ID         varchar(50) not null,
      D_Name       varchar(50) not null,
      D_Type       varchar(50),
      Manager_ID   varchar(50),
      primary key (D_ID)
);

/*
Employee: 员工表
      E_ID: 员工ID
      E_Name: 员工名
      B_Name: 支行名
      D_ID: 部门ID
      E_Tel: 电话
      E_Addr: 地址
      Work_Date: 入职日期
      E_Img: 头像
*/
create table Employee
(
      E_ID         varchar(50) not null,
      E_Name       varchar(50) not null,
      B_Name       varchar(50) not null,
      D_ID         varchar(50),
      E_Tel        int,
      E_Addr       varchar(50),
      Work_Date    date,
      E_Img        varchar(50),
      primary key (E_ID)
);

alter table Employee add constraint FK_Belong_To foreign key (D_ID)
      references Department (D_ID) on delete restrict on update restrict;

alter table Employee add constraint FK_Employ foreign key (B_Name)
      references Bank (B_Name) on delete restrict on update restrict;

/*
Client: 客户表
      C_ID: 客户ID
      C_Name: 客户名
      C_Tel: 电话
      C_Addr: 地址
*/
create table Client
(
      C_ID         varchar(50) not null,
      C_Name       varchar(50) not null,
      C_Tel        varchar(50),
      C_Addr       varchar(50),
      primary key (C_ID)
);

/*
Account: 账户表
      A_ID: 账户ID
      B_Name: 支行名
      Balance: 余额
      Opening_Date: 开户日期
*/
create table Account
(
      A_ID          varchar(50) not null,
      B_Name        varchar(50) not null,
      Balance       float(15),
      Opening_Date  date,
      C_ID          varchar(50),
      primary key (A_ID)
);

alter table Account add constraint FK_Open foreign key (B_Name)
      references Bank (B_Name) on delete restrict on update restrict;

alter table Account add constraint FK_Have_Account foreign key (C_ID)
      references Client (C_ID) on delete restrict on update restrict;

/*
Saving_Account: 储蓄账户表
      A_ID: 账户ID
      Interest_Rate: 利率
      Currency_Type: 货币类型
*/
create table Saving_Account
(
      A_ID           varchar(50) not null,
      Interest_Rate  float(15),
      Currency_Type  varchar(50),
      primary key (A_ID)
);

alter table Saving_Account add constraint FK_Account_Type2 foreign key (A_ID)
      references Account (A_ID) on delete restrict on update restrict;

/* TODO
Credit_Account: 信用账户表
      A_ID: 账户ID
      Overdraft: 透支额度

*/
create table Credit_Account
(
      A_ID         varchar(50) not null,
      Overdraft    float(15),
      primary key (A_ID)
);

alter table Credit_Account add constraint FK_Account_Type foreign key (A_ID)
      references Account (A_ID) on delete restrict on update restrict;

/*
Loan: 贷款表
      L_ID: 贷款ID
      B_Name: 支行名
      L_Amount: 贷款金额
      L_Status: 贷款状态
      P_already: 已还金额
*/
create table Loan
(
      L_ID         varchar(50) not null,
      B_Name       varchar(50) not null,
      L_Amount     float(15) not null,
      L_Status		int default 0 not null,
      P_already    float(15) not null,
      primary key (L_ID)
);

alter table Loan add constraint FK_Make_Loan foreign key (B_Name)
      references Bank (B_Name) on delete restrict on update restrict;

/*
Own: 拥有表
      C_ID: 客户ID
      A_ID: 账户ID
      Visited_Date: 拥有日期
*/
create table Own
(
      C_ID         varchar(50) not null,
      Visited_Date date,
      A_ID         varchar(50),
      primary key (C_ID, A_ID)
);

alter table Own add constraint FK_Own1 foreign key (C_ID)
      references Client (C_ID) on delete restrict on update restrict;

alter table Own add constraint FK_Own2 foreign key (A_ID)
      references Account (A_ID) on delete restrict on update restrict;

/*
Apply: 贷款发放表
      C_ID: 客户ID
      L_ID: 贷款ID
      P_ID: 支行ID
      P_Amount: 放款金额
      Pay_Date: 放款日期
*/
create table Apply
(
      C_ID         varchar(50) not null,
      L_ID         varchar(50) not null,
      P_ID         varchar(50) not null,
      P_Amount     float(15),
      Pay_Date     date,
      primary key (C_ID, L_ID, P_ID)
);

alter table Apply add constraint FK_Apply foreign key (C_ID)
      references Client (C_ID) on delete restrict on update restrict;

/*
Checking: 开户约束表
      C_ID: 客户ID
      B_Name: 支行名
      A_Type: 账户类型
      A_ID: 账户ID
*/
create table Checking
(
      C_ID         varchar(50) not null,
      B_Name       varchar(50) not null,
      A_Type       int not null,
      A_ID         varchar(50),
      primary key (C_ID, B_Name, A_Type)
);


alter table Checking add constraint FK_Checking1 foreign key (C_ID)
      references Client (C_ID) on delete restrict on update restrict;

alter table Checking add constraint FK_Checking2 foreign key (B_Name)
      references Bank (B_Name) on delete restrict on update restrict;

alter table Checking add constraint FK_Checking3 foreign key (A_ID)
      references Account (A_ID) on delete restrict on update restrict;