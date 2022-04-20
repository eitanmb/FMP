
TABLE_PROFILE_STRUCTURE = f'CREATE TABLE profile ( \
        `id` int(11) NOT NULL AUTO_INCREMENT, \
        `symbol` varchar(50) NOT NULL, \
        `price` varchar(50) DEFAULT NULL, \
        `beta`  varchar(50) DEFAULT NULL, \
        `volAvg` varchar(50) DEFAULT NULL, \
        `mktCap` varchar(50) DEFAULT NULL, \
        `lastDiv` varchar(50) DEFAULT NULL, \
        `range` text, \
        `changes` text DEFAULT NULL, \
        `companyName` text, \
        `currency` text, \
        `cik` varchar(100) DEFAULT NULL, \
        `isin` text, \
        `cusip` text DEFAULT NULL, \
        `exchange` text, \
        `exchangeShortName` text, \
        `industry` text, \
        `website` text, \
        `description` text, \
        `ceo` text, \
        `sector` text, \
        `country` text, \
        `fullTimeEmployees` varchar(20) DEFAULT NULL, \
        `phone` varchar(100) DEFAULT NULL, \
        `address` text, \
        `city` text, \
        `state` text, \
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