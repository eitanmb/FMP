
TABLE_PROFILE_STRUCTURE = f'CREATE TABLE profile ( \
        `id` int(11) NOT NULL AUTO_INCREMENT, \
        `symbol` varchar(50) NOT NULL, \
        `price` varchar(50) DEFAULT NULL, \
        `beta`  varchar(50) DEFAULT NULL, \
        `volAvg` varchar(50) DEFAULT NULL, \
        `mktCap` varchar(50) DEFAULT NULL, \
        `lastDiv` varchar(50) DEFAULT NULL, \
        `range` varchar(250) DEFAULT NULL, \
        `changes` varchar(250) DEFAULT NULL, \
        `companyName` varchar(250) DEFAULT NULL, \
        `currency` text, \
        `cik` varchar(100) DEFAULT NULL, \
        `isin` text, \
        `cusip` text DEFAULT NULL, \
        `exchange` text, \
        `exchangeShortName` text, \
        `industry` varchar(250) DEFAULT NULL, \
        `website` varchar(250) DEFAULT NULL, \
        `description` text, \
        `ceo` text, \
        `sector` varchar(250) DEFAULT NULL, \
        `country` varchar(250) DEFAULT NULL, \
        `fullTimeEmployees` varchar(20) DEFAULT NULL, \
        `phone` varchar(100) DEFAULT NULL, \
        `address` text, \
        `city` varchar(250) DEFAULT NULL, \
        `state` varchar(250) DEFAULT NULL, \
        `zip` varchar(100) DEFAULT NULL, \
        `dcfDiff` varchar(50) DEFAULT NULL, \
        `dcf` varchar(50) DEFAULT NULL, \
        `image` text, \
        `ipoDate` text, \
        `defaultImage` tinyint(1) DEFAULT NULL, \
        `isEtf` tinyint(1) DEFAULT NULL, \
        `isActivelyTrading` tinyint(1) DEFAULT NULL, \
        `isAdr` tinyint(1) DEFAULT NULL, \
        `isFund` tinyint(1) DEFAULT NULL, \
        PRIMARY KEY (`id`) \
      ) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;'


PROFILE_INDEXES = f'ALTER TABLE `profile` \
                    ADD FULLTEXT INDEX `Search` (`description`) VISIBLE, \
                    ADD INDEX `ISector` (`sector` ASC) VISIBLE, \
                    ADD INDEX `ICountry` (`country` ASC) VISIBLE, \
                    ADD INDEX `IIndustry` (`industry` ASC) VISIBLE, \
                    ADD INDEX `ICompany` (`companyName` ASC) VISIBLE, \
                    ADD INDEX `ISecInd` (`sector` ASC, `industry` ASC) VISIBLE, \
                    ADD INDEX `ISecIndCtry` (`industry` ASC, `sector` ASC, `country` ASC) VISIBLE, \
                    ADD INDEX `ICompSect` (`companyName` ASC, `sector` ASC) VISIBLE, \
                    ADD INDEX `ICompInd` (`companyName` ASC, `industry` ASC) VISIBLE, \
                    ADD INDEX `ICompIndSec` (`companyName` ASC, `sector` ASC, `industry` ASC) VISIBLE;'


IS_INDEXES = f'ALTER TABLE `incomeStatement` \
              ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (`id`), \
              ADD INDEX `IRevenue` (`revenue` ASC) VISIBLE, \
              ADD INDEX `ICostOfRevenue` (`costOfRevenue` ASC) VISIBLE, \
              ADD INDEX `IOperatingExpenses` (`operatingExpenses` ASC) VISIBLE, \
              ADD INDEX `IRevCostExpDate` (`revenue` ASC, `costOfRevenue` ASC, `operatingExpenses` ASC, `calendarYear` ASC) VISIBLE, \
              ADD INDEX `IDate` (`calendarYear` ASC) VISIBLE, \
              CHANGE COLUMN `link` `linkIncomeStatement` TEXT NULL DEFAULT NULL , \
              CHANGE COLUMN `finalLink` `finalLinkIncomeStatement` TEXT NULL DEFAULT NULL ;'

BS_INDEXES = f'ALTER TABLE `balanceSheet` \
              ADD INDEX `IDate` (`calendarYear` ASC) VISIBLE, \
              ADD INDEX `IAssLiabInv` (`totalLiabilities` ASC, `totalAssets` ASC, `inventory` ASC) VISIBLE, \
              ADD INDEX `IAsstes` (`totalAssets` ASC) VISIBLE, \
              ADD INDEX `ILiab` (`totalLiabilities` ASC) VISIBLE, \
              ADD INDEX `IInventory` (`inventory` ASC) VISIBLE, \
              CHANGE COLUMN `link` `linkBalanceSheet` TEXT NULL DEFAULT NULL , \
              CHANGE COLUMN `finalLink` `finalLinkBalanceSheet` TEXT NULL DEFAULT NULL ;'

CF_INDEXES = f'ALTER TABLE cashFlow ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (`id`), \
              CHANGE COLUMN `link` `linkCashFlow` TEXT NULL DEFAULT NULL, \
              CHANGE COLUMN `finalLink` `finalLinkCashFlow` TEXT NULL DEFAULT NULL;'




