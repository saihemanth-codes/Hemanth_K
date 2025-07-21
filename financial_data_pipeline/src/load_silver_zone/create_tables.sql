create table if not exist orders(
    order_id    int,
    account_id  int,
    bank_to     varchar,
    account_to  int,
    amount      decimal,
    k_symbol    varchar
);

create table if not exist cards(
    card_id int,
    disp_id int,
    type    varchar,
    issued  varchar
);


create table if not exist loans(
    loan_id    int,
    account_id int,
    date       int,
    amount     int,
    duration   int,
    payments   decimal,
    status     varchar
);


create table if not exist trans(
    trans_id   int,
    account_id int,
    date       int,
    type       varchar,
    operation  varchar,
    amount     decimal,
    balance    decimal.
    k_symbol   varchar,
    bank       varchar,
    account    decimal
);


create table if not exist districts(
    A1   int,
    A2   varchar,
    A3   varchar,
    A4   int,
    A5   int,
    A6   int,
    A7   int,
    A8   int,
    A9   int,
    A10  decimal,
    A11  int,
    A12  varchar,
    A13  decimal,
    A14  int,
    A15  varchar,
    A16  int
);


create table if not exist disps(
    disp_id    int,
    client_id  int,
    account_id int,
    type       varchar
);


create table if not exist accounts(
    account_id  int,
    district_id int,
    frequency   varchar,
    date        int
);


create table if not exist clients(
    client_id    int,
    birth_number int,
    district_id  int
);