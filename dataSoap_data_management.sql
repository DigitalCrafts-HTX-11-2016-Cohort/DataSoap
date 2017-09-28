/*** USE THIS TO LOAD THE NEUSTAR FILES ONCE DOWNLOADED ***/
SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;
LOAD DATA LOCAL INFILE 'X:/Vista Energy Marketing/Karissa/dnc_com/neustar/WIRELESS-TO-WIRELINE-NORANGE.TXT' REPLACE INTO TABLE wireless_convert (PhoneNumber) set source = 'WTL';
commit;
LOAD DATA LOCAL INFILE 'X:/Vista Energy Marketing/Karissa/dnc_com/neustar/WIRELINE-TO-WIRELESS-NORANGE.TXT' REPLACE INTO TABLE wireless_convert (PhoneNumber) set source = 'LTW';
commit;
SET FOREIGN_KEY_CHECKS = 1;
SET AUTOCOMMIT = 1;
insert ignore into master (PhoneNumber, wireless)
select PhoneNumber,1 from wireless_convert where source = 'LTW';
delete from master where wireless = 1 AND PhoneNumber IN (SELECT PhoneNumber from wireless_convert where source = 'WTL');


/*** USE THIS TO LOAD THE FEDERAL/STATE DNC DELTA FILE ONCE DOWNLOADED ***/
SET FOREIGN_KEY_CHECKS = 0;
-- SET UNIQUE_CHECKS = 0;
SET AUTOCOMMIT = 0;
LOAD DATA LOCAL INFILE 'X:/Vista Energy Marketing/Karissa/dnc_com/federal_downloads/delta_2017-09-13/BAE00F5E-4C3C-419E-B32A-2EB698981E45.txt' REPLACE INTO TABLE dnc_delta
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
commit;
SET FOREIGN_KEY_CHECKS = 1;
SET AUTOCOMMIT = 1;


/*** USE THIS TO LOAD THE A VALUES ON FEDERAL/STATE DNC DELTA FILE ONCE DOWNLOADED ***/
insert ignore into master_noindex (PhoneNumber, dnc)
select PhoneNumber,1 from dnc_delta where changeType = 'A' AND changeDate > '2017-08-24';  -- CHANGE DATE ACCORDINGLY


/*** USE THIS TO REMOVE THE D VALUES ON FEDERAL/STATE DNC DELTA FILE ONCE DOWNLOADED ***/
CREATE TEMPORARY TABLE phoneToDelete (PhoneNumber bigint(20));
    INSERT INTO phoneToDelete
      select dnc_delta.PhoneNumber from dnc_delta
      inner join master mni on dnc_delta.PhoneNumber = mni.PhoneNumber and mni.dnc = 1
      where dnc_delta.changeType = 'D'
      and dnc_delta.changeDate > '2017-08-24'
      order by PhoneNumber asc
    ;
    DELETE master.* from master WHERE dnc = 1 and master.PhoneNumber in (Select PhoneNumber from phoneToDelete);
DROP TABLE phoneToDelete;

/*** USE THIS TO UPDATE THE CARRIER PREFIXES ONCE DOWNLOADED ***/
CREATE TEMPORARY TABLE temporary_table LIKE carrierPrefixes;
ALTER TABLE temporary_table DROP COLUMN do_not_call;
ALTER TABLE temporary_table DROP COLUMN prefix;
LOAD DATA LOCAL INFILE 'X:/Vista Energy Marketing/Karissa/dnc_com/PrefixMasterListCarrier/PrefixMasterListCarrier.csv'
INTO TABLE  temporary_table
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';
SELECT * FROM temporary_table LIMIT 10;

SELECT * FROM temporary_table inner join carrierPrefixes on prefix = concat(temporary_table.areaCode,temporary_table.firstFour)
where temporary_table.source != carrierPrefixes.source
or temporary_table.dba != carrierPrefixes.dba
or temporary_table.lineType != carrierPrefixes.lineType;


/*** IF REPLACEMENT NEEDED, REDO BELOW VOIP EXCEPTIONS ***/
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Comcast';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'tw telecom';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Videotron Business Solutions';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Level 3';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Verizon Wireless';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Shaw Telecom';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'CenturyLink';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'AT&T Mobility';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Charter Fiberlink';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'YMax Communications';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Cox';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'T-Mobile';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Cablevision Lightpath';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'TELNYX';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Sprint';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'AT&T';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Peerless Network';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Verizon Communications';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'AT&T Internet Services';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Frontier';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'MEDIACOM';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'XO Communications';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Midcontinent Communications';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'AT&T Southwest';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Windstream';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'PAETEC';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'RCN Telecom';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'AT&T Southeast';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Bright House Networks';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'Knology';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'WOW! Business Solutions';
update carrierPrefixes set do_not_call = 0 where lineType = 'V' and dba = 'AT&T California';
