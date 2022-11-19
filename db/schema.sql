CREATE DATABASE claims_db;

USE claims_db

CREATE TABLE claims (
    uid varchar(255) NOT NULL PRIMARY KEY,
    service_date varchar(255),
    submitted_procedure varchar(255),
    quadrant varchar(255) NULL,
    plan_or_group_no varchar(255),
    subscriber_no varchar(255),
    provider_npi varchar(255),
    provider_fees float,
    allowed_fees float,
    member_coinsurance float,
    member_copay float
);

-- TODO: I'm risking trimming some values above - solve this in the future