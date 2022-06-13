PROFILE_DROP_TABLE = f"DROP TABLE IF EXISTS profile"
PROFILE_CREATE_TABLE = f'CREATE TABLE profile ( \
                        `symbol` varchar(25) NOT NULL, \
                        `price` varchar(50) DEFAULT NULL, \
                        `beta`  varchar(50) DEFAULT NULL, \
                        `volAvg` varchar(50) DEFAULT NULL, \
                        `mktCap` varchar(50) DEFAULT NULL, \
                        `lastDiv` varchar(50) DEFAULT NULL, \
                        `range` varchar(250) DEFAULT NULL, \
                        `changes` varchar(250) DEFAULT NULL, \
                        `companyName` varchar(250) DEFAULT NULL, \
                        `currency` varchar(15), \
                        `cik` varchar(200) DEFAULT NULL, \
                        `isin` varchar(200), \
                        `cusip` varchar(100) DEFAULT NULL, \
                        `exchange` varchar(200), \
                        `exchangeShortName` varchar(100), \
                        `industry` varchar(250) DEFAULT NULL, \
                        `website` varchar(250) DEFAULT NULL, \
                        `description` text, \
                        `ceo` varchar(200), \
                        `sector` varchar(250) DEFAULT NULL, \
                        `country` varchar(250) DEFAULT NULL, \
                        `fullTimeEmployees` varchar(20) DEFAULT NULL, \
                        `phone` varchar(100) DEFAULT NULL, \
                        `address` tinytext, \
                        `city` varchar(250) DEFAULT NULL, \
                        `state` varchar(250) DEFAULT NULL, \
                        `zip` varchar(100) DEFAULT NULL, \
                        `dcfDiff` varchar(50) DEFAULT NULL, \
                        `dcf` varchar(50) DEFAULT NULL, \
                        `image` text, \
                        `ipoDate` varchar(200), \
                        `defaultImage` tinyint(1) DEFAULT NULL, \
                        `isEtf` tinyint(1) DEFAULT NULL, \
                        `isActivelyTrading` tinyint(1) DEFAULT NULL, \
                        `isAdr` tinyint(1) DEFAULT NULL, \
                        `isFund` tinyint(1) DEFAULT NULL, \
                        PRIMARY KEY (`symbol`) \
                      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'


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

IS_DROP_TABLE = f"DROP TABLE IF EXISTS incomeStatement"
IS_CREATE_TABLE = f'CREATE TABLE `incomeStatement` (\
                      `id` int NOT NULL AUTO_INCREMENT,\
                      `date` datetime DEFAULT NULL,\
                      `symbol` varchar(25) NOT NULL,\
                      `reportedCurrency` text,\
                      `cik` bigint DEFAULT NULL,\
                      `fillingDate` text,\
                      `acceptedDate` text,\
                      `calendarYear` bigint DEFAULT NULL,\
                      `period` text,\
                      `revenue` bigint DEFAULT NULL,\
                      `costOfRevenue` bigint DEFAULT NULL,\
                      `grossProfit` bigint DEFAULT NULL,\
                      `grossProfitRatio` double DEFAULT NULL,\
                      `researchAndDevelopmentExpenses` bigint DEFAULT NULL,\
                      `generalAndAdministrativeExpenses` bigint DEFAULT NULL,\
                      `sellingAndMarketingExpenses` bigint DEFAULT NULL,\
                      `sellingGeneralAndAdministrativeExpenses` bigint DEFAULT NULL,\
                      `otherExpenses` bigint DEFAULT NULL,\
                      `operatingExpenses` bigint DEFAULT NULL,\
                      `costAndExpenses` bigint DEFAULT NULL,\
                      `interestIncome` bigint DEFAULT NULL,\
                      `interestExpense` bigint DEFAULT NULL,\
                      `depreciationAndAmortization` bigint DEFAULT NULL,\
                      `ebitda` bigint DEFAULT NULL,\
                      `ebitdaratio` double DEFAULT NULL,\
                      `operatingIncome` bigint DEFAULT NULL,\
                      `operatingIncomeRatio` double DEFAULT NULL,\
                      `totalOtherIncomeExpensesNet` bigint DEFAULT NULL,\
                      `incomeBeforeTax` bigint DEFAULT NULL,\
                      `incomeBeforeTaxRatio` double DEFAULT NULL,\
                      `incomeTaxExpense` bigint DEFAULT NULL,\
                      `netIncome` bigint DEFAULT NULL,\
                      `netIncomeRatio` double DEFAULT NULL,\
                      `eps` double DEFAULT NULL,\
                      `epsdiluted` double DEFAULT NULL,\
                      `weightedAverageShsOut` bigint DEFAULT NULL,\
                      `weightedAverageShsOutDil` bigint DEFAULT NULL,\
                      `link` text,\
                      `finalLink` text,\
                      PRIMARY KEY (`id`) \
                    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4'

IS_CHANGE_COLUMNS = f'ALTER TABLE `incomeStatement` \
              CHANGE COLUMN `link` `linkIncomeStatement` TEXT NULL DEFAULT NULL , \
              CHANGE COLUMN `finalLink` `finalLinkIncomeStatement` TEXT NULL DEFAULT NULL ;'

IS_DELETE_NO_SYMBOL = f'DELETE FROM incomeStatement where symbol is NULL;'

IS_FK = f'ALTER TABLE `incomeStatement` \
          ADD CONSTRAINT `fk_symbol_is` \
          FOREIGN KEY (`symbol`) \
          REFERENCES `profile` (`symbol`) \
          ON DELETE NO ACTION \
          ON UPDATE NO ACTION;'

IS_OPERATIONS = {
    "drop_table": IS_DROP_TABLE,
    "create_table": IS_CREATE_TABLE,
    "alter_table": IS_CHANGE_COLUMNS,
    "delete_null": IS_DELETE_NO_SYMBOL,
    "add_indexes": IS_FK

}

BS_DROP_TABLE = f"DROP TABLE IF EXISTS balanceSheet"
BS_CREATE_TABLE = f"CREATE TABLE `balanceSheet` ( \
                      `id` int NOT NULL AUTO_INCREMENT, \
                      `date` datetime DEFAULT NULL, \
                      `symbol` varchar(25) NOT NULL, \
                      `reportedCurrency` text, \
                      `cik` bigint DEFAULT NULL, \
                      `fillingDate` text, \
                      `acceptedDate` text, \
                      `calendarYear` bigint DEFAULT NULL, \
                      `period` text, \
                      `cashAndCashEquivalents` bigint DEFAULT NULL, \
                      `shortTermInvestments` bigint DEFAULT NULL, \
                      `cashAndShortTermInvestments` bigint DEFAULT NULL, \
                      `netReceivables` bigint DEFAULT NULL, \
                      `inventory` bigint DEFAULT NULL, \
                      `otherCurrentAssets` bigint DEFAULT NULL, \
                      `totalCurrentAssets` bigint DEFAULT NULL, \
                      `propertyPlantEquipmentNet` bigint DEFAULT NULL, \
                      `goodwill` bigint DEFAULT NULL, \
                      `intangibleAssets` bigint DEFAULT NULL, \
                      `goodwillAndIntangibleAssets` bigint DEFAULT NULL, \
                      `longTermInvestments` bigint DEFAULT NULL, \
                      `taxAssets` bigint DEFAULT NULL, \
                      `otherNonCurrentAssets` bigint DEFAULT NULL, \
                      `totalNonCurrentAssets` bigint DEFAULT NULL, \
                      `otherAssets` bigint DEFAULT NULL, \
                      `totalAssets` bigint DEFAULT NULL, \
                      `accountPayables` bigint DEFAULT NULL, \
                      `shortTermDebt` bigint DEFAULT NULL, \
                      `taxPayables` bigint DEFAULT NULL, \
                      `deferredRevenue` bigint DEFAULT NULL, \
                      `otherCurrentLiabilities` bigint DEFAULT NULL, \
                      `totalCurrentLiabilities` bigint DEFAULT NULL, \
                      `longTermDebt` bigint DEFAULT NULL, \
                      `deferredRevenueNonCurrent` bigint DEFAULT NULL, \
                      `deferredTaxLiabilitiesNonCurrent` bigint DEFAULT NULL, \
                      `otherNonCurrentLiabilities` bigint DEFAULT NULL, \
                      `totalNonCurrentLiabilities` bigint DEFAULT NULL, \
                      `otherLiabilities` bigint DEFAULT NULL, \
                      `capitalLeaseObligations` bigint DEFAULT NULL, \
                      `totalLiabilities` bigint DEFAULT NULL, \
                      `preferredStock` bigint DEFAULT NULL, \
                      `commonStock` bigint DEFAULT NULL, \
                      `retainedEarnings` bigint DEFAULT NULL, \
                      `accumulatedOtherComprehensiveIncomeLoss` bigint DEFAULT NULL, \
                      `othertotalStockholdersEquity` bigint DEFAULT NULL, \
                      `totalStockholdersEquity` bigint DEFAULT NULL, \
                      `totalLiabilitiesAndStockholdersEquity` bigint DEFAULT NULL, \
                      `minorityInterest` bigint DEFAULT NULL, \
                      `totalEquity` bigint DEFAULT NULL, \
                      `totalLiabilitiesAndTotalEquity` bigint DEFAULT NULL, \
                      `totalInvestments` bigint DEFAULT NULL, \
                      `totalDebt` bigint DEFAULT NULL, \
                      `netDebt` bigint DEFAULT NULL, \
                      `link` text, \
                      `finalLink` text, \
                      PRIMARY KEY (`id`) \
                    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4"


BS_CHANGE_COLUMNS = f'ALTER TABLE `balanceSheet` \
              CHANGE COLUMN `link` `linkBalanceSheet` TEXT NULL DEFAULT NULL , \
              CHANGE COLUMN `finalLink` `finalLinkBalanceSheet` TEXT NULL DEFAULT NULL ;'

BS_DELETE_NO_SYMBOL = f'DELETE FROM balanceSheet where symbol is NULL;'

BS_FK = f'ALTER TABLE `balanceSheet` \
          ADD CONSTRAINT `fk_symbol_bs` \
          FOREIGN KEY (`symbol`) \
          REFERENCES `profile` (`symbol`) \
          ON DELETE NO ACTION \
          ON UPDATE NO ACTION;'

BS_OPERATIONS = {
    "drop_table": BS_DROP_TABLE,
    "create_table": BS_CREATE_TABLE,
    "alter_table": BS_CHANGE_COLUMNS,
    "delete_null": BS_DELETE_NO_SYMBOL,
    "add_indexes": BS_FK
}

CF_DROP_TABLE = f"DROP TABLE IF EXISTS cashFlow"
CF_CREATE_TABLE = f'CREATE TABLE `cashFlow` (\
                      `id` int NOT NULL AUTO_INCREMENT,\
                      `date` datetime NOT NULL,\
                      `symbol` varchar(25) NOT NULL,\
                      `reportedCurrency` text,\
                      `cik` bigint DEFAULT NULL,\
                      `fillingDate` text,\
                      `acceptedDate` text,\
                      `calendarYear` bigint DEFAULT NULL,\
                      `period` text,\
                      `netIncome` bigint DEFAULT NULL,\
                      `depreciationAndAmortization` bigint DEFAULT NULL,\
                      `deferredIncomeTax` bigint DEFAULT NULL,\
                      `stockBasedCompensation` bigint DEFAULT NULL,\
                      `changeInWorkingCapital` bigint DEFAULT NULL,\
                      `accountsReceivables` bigint DEFAULT NULL,\
                      `inventory` bigint DEFAULT NULL,\
                      `accountsPayables` bigint DEFAULT NULL,\
                      `otherWorkingCapital` bigint DEFAULT NULL,\
                      `otherNonCashItems` bigint DEFAULT NULL,\
                      `netCashProvidedByOperatingActivities` bigint DEFAULT NULL,\
                      `investmentsInPropertyPlantAndEquipment` bigint DEFAULT NULL,\
                      `acquisitionsNet` bigint DEFAULT NULL,\
                      `purchasesOfInvestments` bigint DEFAULT NULL,\
                      `salesMaturitiesOfInvestments` bigint DEFAULT NULL,\
                      `otherInvestingActivites` bigint DEFAULT NULL,\
                      `netCashUsedForInvestingActivites` bigint DEFAULT NULL,\
                      `debtRepayment` bigint DEFAULT NULL,\
                      `commonStockIssued` bigint DEFAULT NULL,\
                      `commonStockRepurchased` bigint DEFAULT NULL,\
                      `dividendsPaid` bigint DEFAULT NULL,\
                      `otherFinancingActivites` bigint DEFAULT NULL,\
                      `netCashUsedProvidedByFinancingActivities` bigint DEFAULT NULL,\
                      `effectOfForexChangesOnCash` bigint DEFAULT NULL,\
                      `netChangeInCash` bigint DEFAULT NULL,\
                      `cashAtEndOfPeriod` bigint DEFAULT NULL,\
                      `cashAtBeginningOfPeriod` bigint DEFAULT NULL,\
                      `operatingCashFlow` bigint DEFAULT NULL,\
                      `capitalExpenditure` bigint DEFAULT NULL,\
                      `freeCashFlow` bigint DEFAULT NULL,\
                      `link` text,\
                      `finalLink` text,\
                      PRIMARY KEY (`id`)\
                    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4'

CF_CHANGE_COLUMNS = f'ALTER TABLE cashFlow \
              CHANGE COLUMN `link` `linkCashFlow` TEXT NULL DEFAULT NULL, \
              CHANGE COLUMN `finalLink` `finalLinkCashFlow` TEXT NULL DEFAULT NULL;'

CF_DELETE_NO_SYMBOL = f'DELETE FROM cashFlow where symbol is NULL;'

CF_FK = f'ALTER TABLE `cashFlow` \
                ADD CONSTRAINT `fk_symbol_cf` \
                FOREIGN KEY (`symbol`) \
                REFERENCES `profile` (`symbol`) \
                ON DELETE NO ACTION \
                ON UPDATE NO ACTION;'

CF_OPERATIONS = {
    "drop_table": CF_DROP_TABLE,
    "create_table": CF_CREATE_TABLE,
    "alter_table": CF_CHANGE_COLUMNS,
    "delete_null": CF_DELETE_NO_SYMBOL,
    "add_indexes": CF_FK
}
