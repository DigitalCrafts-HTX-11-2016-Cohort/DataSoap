/*** USE THIS TO LOAD THE NEUSTAR FILES ONCE DOWNLOADED ***/
SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;
LOAD DATA LOCAL INFILE 'X:/Vista Energy Marketing/Karissa/dnc_com/neustar/WIRELESS-TO-WIRELINE-NORANGE.TXT' REPLACE INTO TABLE wireless_convert (PhoneNumber) set source = 'WTL';
commit;
LOAD DATA LOCAL INFILE 'X:/Vista Energy Marketing/Karissa/dnc_com/neustar/WIRELINE-TO-WIRELESS-NORANGE.TXT' REPLACE INTO TABLE wireless_convert (PhoneNumber) set source = 'LTW';
SET FOREIGN_KEY_CHECKS = 1;
SET AUTOCOMMIT = 1;
insert ignore into master (PhoneNumber, wireless)
select PhoneNumber,1 from wireless_convert where source = 'LTW';
delete from master where wireless = 1 AND PhoneNumber IN (SELECT PhoneNumber from wireless_convert where source = 'WTL');


/*** USE THIS TO LOAD THE FEDERAL/STATE DNC DELTA FILE ONCE DOWNLOADED ***/
SET FOREIGN_KEY_CHECKS = 0;
-- SET UNIQUE_CHECKS = 0;
SET AUTOCOMMIT = 0;
LOAD DATA LOCAL INFILE 'X:/Vista Energy Marketing/Karissa/dnc_com/federal_downloads/delta_2017-08-01/B333794D-5F08-4718-86A3-ABD5D3D09F56.txt' REPLACE INTO TABLE dnc_delta
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
commit;
SET FOREIGN_KEY_CHECKS = 1;
SET AUTOCOMMIT = 1;


/*** USE THIS TO LOAD THE A VALUES ON FEDERAL/STATE DNC DELTA FILE ONCE DOWNLOADED ***/
insert ignore into master_noindex (PhoneNumber, dnc)
select PhoneNumber,1 from dnc_delta where changeType = 'A' AND changeDate >= '2017-07-29'  -- CHANGE DATE ACCORDINGLY


/*** USE THIS TO REMOVE THE D VALUES ON FEDERAL/STATE DNC DELTA FILE ONCE DOWNLOADED ***/
DROP PROCEDURE IF EXISTS deleteOneByOne

CREATE PROCEDURE deleteOneByOne (earliestChangeDate DATE)
  BEGIN

    DECLARE phoneToDelete BIGINT;
    REPEAT

      set @phoneToDelete =
      (select dnc_delta.PhoneNumber from dnc_delta
      inner join master_noindex mni on dnc_delta.PhoneNumber = mni.PhoneNumber
      where changeType = 'D' and changeDate >= earliestChangeDate and mni.dnc = 1 limit 1);

      DELETE master_noindex.* from master_noindex WHERE dnc = 1 and master_noindex.PhoneNumber = @phoneToDelete;
#     UNTIL 1=1 END REPEAT;
      UNTIL @phoneToDelete IS NULL END REPEAT;
  END;

CALL deleteOneByOne('2017-06-22')
