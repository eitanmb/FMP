db.forex.aggregate([
    {
      $project: {
        _id: 0,
        Pair: 1,
        base: { $substrCP: ['$Pair', 0, 3] },
        quote: { $substrCP: ['$Pair', 3, { $strLenCP: '$Pair' }] }
      }
    }
])


db.forex.aggregate([
    {
      $group: { _id: {pair:"$Pair"}}
    },
    {
        $project: {
          _id:0,
          base: { $substrCP: ['$_id.pair', 0, 3] },
          quote: { $substrCP: ['$_id.pair', 3, { $strLenCP: '$_id.pair' }] }
        }
    },
    {
        $match: { base: 'USD' }
    },
    {
        $count:'total usd as base currency'
    }
])