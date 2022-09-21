CREATE DEFINER = `eitan` @`localhost` PROCEDURE `proc_create_base_query_data`() BEGIN DECLARE fieldExist INT;
CALL fieldExists(
    @_exists,
    'incomeStatement',
    'calendarYear',
    NULL
);
DROP TABLE IF EXISTS base_query_data;
IF (
    select
        @_exists = 0
) THEN CREATE TABLE base_query_data AS
SELECT
    t0.companyName as `Company Name`,
    t0.symbol as Symbol,
    t0.exchangeShortName as `Exchange Short Name`,
    t0.industry as `Industry`,
    t0.website as `Website`,
    t0.description as `Description`,
    t0.sector as `Sector`,
    t0.country as `Country`,
    t0.fullTimeEmployees as `Full Time Employees`,
    t1.date as Date,
    t1.reportedCurrency as `Reported Currency`,
    t1.period as `Period`,
    t1.revenue as `Revenue`,
    t1.costOfRevenue as `Cost Of Revenue`,
    t1.grossProfit as `Gross Profit`,
    t1.researchAndDevelopmentExpenses as `Research And Development Expenses`,
    t1.generalAndAdministrativeExpenses as `General And Administrative Expenses`,
    t1.sellingAndMarketingExpenses as `Selling And Marketing Expenses`,
    t1.otherExpenses as `Other Expenses`,
    t1.operatingExpenses as `Operating Expenses`,
    t1.costAndExpenses as `Cost And Expenses`,
    t1.InterestExpense as `Interest Expense`,
    t1.depreciationAndAmortization as `Depreciation And Amortization`,
    t1.operatingIncome as `Operating Income`,
    t1.linkIncomestatement as `Link Incomestatement`,
    t1.finalLinkIncomestatement as `Final Link Incomestatement`,
    t2.cashAndCashEquivalents as `Cash And Cash Equivalents`,
    t2.netReceivables as `Net Receivables`,
    t2.inventory as `Inventory`,
    t2.totalCurrentAssets as `Total Current Assets`,
    t2.totalNonCurrentAssets as `Total Non Current Assets`,
    t2.totalAssets as `Total Assets`,
    t2.accountPayables as `Account Payables`,
    t2.totalCurrentLiabilities as `Total Current Liabilities`,
    t2.totalNonCurrentLiabilities as `Total Non Current Liabilities`,
    t2.totalLiabilities as `Total Liabilities`,
    t2.linkBalancesheet as `Link Balancesheet`,
    t2.finalLinkBalancesheet as `Final Link Balancesheet`,
    Year(t1.date) as `Year`
from
    profile t0
    INNER JOIN incomeStatement t1 on t0.symbol = t1.symbol
    INNER JOIN balanceSheet t2 ON t2.symbol = t1.symbol
WHERE
    t0.companyName <> ""
    and (YEAR(t1.date) = YEAR(t2.date))
    and YEAR(t1.date) >= 2008
    and t0.isEtf = 0
    and (
        t1.reportedCurrency is not Null
        and t1.reportedCurrency <> 'unknown'
    );
ELSE CREATE TABLE base_query_data AS
SELECT
    t0.companyName as `Company Name`,
    t0.symbol as Symbol,
    t0.exchangeShortName as `Exchange Short Name`,
    t0.industry as `Industry`,
    t0.website as `Website`,
    t0.description as `Description`,
    t0.sector as `Sector`,
    t0.country as `Country`,
    t0.fullTimeEmployees as `Full Time Employees`,
    t1.date as Date,
    t1.reportedCurrency as `Reported Currency`,
    t1.period as `Period`,
    t1.revenue as `Revenue`,
    t1.costOfRevenue as `Cost Of Revenue`,
    t1.grossProfit as `Gross Profit`,
    t1.researchAndDevelopmentExpenses as `Research And Development Expenses`,
    t1.generalAndAdministrativeExpenses as `General And Administrative Expenses`,
    t1.sellingAndMarketingExpenses as `Selling And Marketing Expenses`,
    t1.otherExpenses as `Other Expenses`,
    t1.operatingExpenses as `Operating Expenses`,
    t1.costAndExpenses as `Cost And Expenses`,
    t1.InterestExpense as `Interest Expense`,
    t1.depreciationAndAmortization as `Depreciation And Amortization`,
    t1.operatingIncome as `Operating Income`,
    t1.linkIncomestatement as `Link Incomestatement`,
    t1.finalLinkIncomestatement as `Final Link Incomestatement`,
    t2.cashAndCashEquivalents as `Cash And Cash Equivalents`,
    t2.netReceivables as `Net Receivables`,
    t2.inventory as `Inventory`,
    t2.totalCurrentAssets as `Total Current Assets`,
    t2.totalNonCurrentAssets as `Total Non Current Assets`,
    t2.totalAssets as `Total Assets`,
    t2.accountPayables as `Account Payables`,
    t2.totalCurrentLiabilities as `Total Current Liabilities`,
    t2.totalNonCurrentLiabilities as `Total Non Current Liabilities`,
    t2.totalLiabilities as `Total Liabilities`,
    t2.linkBalancesheet as `Link Balancesheet`,
    t2.finalLinkBalancesheet as `Final Link Balancesheet`,
    t1.calendarYear as `Year`
from
    profile t0
    INNER JOIN incomeStatement t1 on t0.symbol = t1.symbol
    INNER JOIN balanceSheet t2 ON t2.symbol = t1.symbol
WHERE
    t0.companyName <> ""
    and (t1.calendarYear = t2.calemdarYear)
    and t1.calendarYear >= 2008
    and t0.isEtf = 0
    and (
        t1.reportedCurrency is not Null
        and t1.reportedCurrency <> 'unknown'
    );
END IF;
ALTER TABLE
    `base_query_data`
ADD
    FULLTEXT INDEX `Search` (`Description`),
ADD
    INDEX `ISector` (`Sector` ASC),
ADD
    INDEX `IIndustry` (`Industry` ASC),
ADD
    INDEX `IYear` (`Year` DESC),
ADD
    INDEX `ICompany` (`Company Name` ASC);
END