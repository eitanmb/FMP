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
          base: { $substrCP: ['$_id.pair', 0, 3] },
          quote: { $substrCP: ['$_id.pair', 3, { $strLenCP: '$_id.pair' }] }
        }
    }
])


db.forex.aggregate([
  {
      $project: {
        _id:0,
        Pair: 1,
        Date: {$toDate:"$Date"},
        Price: 1,
      }
  }
])


db.forex.aggregate([
  {
      $addFields: {
        Date: {$toDate:"$Date"},
        Month: { "$month": "$Date" },
      }
  },
])

db.forex.aggregate([
  {
    $addFields: {
      Date: {
        $dateFromString: {
            dateString: '$Date',
            format: "%Y-%m-%d"
        }
     }
    }
  }
])



db.forex.aggregate(
  [
    {
      $project:
        {
          _id:0,
          Pair:1,
          Date: {$toDate:"$Date"},
          Price:1
         
        }
    },
    {
      $project: {
        Pair:1,
        Date: 1,
        Price:1,
        year: { $year: "$Date" },
        month: { $month: "$Date" },
        day: { $dayOfMonth: "$Date" },
      }
    },
    {
      $match: { $and: [{ month: 12 },{ day:31}]}
    },
    {
      $project: {
        Pair:1,
        Date: 1,
        Price:1,
      }
    },

  ]
)

db.forex.aggregate(
[
  {
    $project:
      {
        _id:0,
        Pair:1,
        Date:1,
        formatedDate: {$toDate:"$Date"},
        Price:{ $replaceOne: { input: "$Price", find: ",", replacement: "" } }
       
      }
  },
  {
    $project: {
      Pair:1,
      Base: { $substrCP: ['$Pair', 0, 3] },
      Quote: { $substrCP: ['$Pair', 3, { $strLenCP: '$Pair' }]},
      Date: 1,
      Price:1,
      Year: { $year: "$formatedDate" },
      Month: { $month: "$formatedDate" },
      Day: { $dayOfMonth: "$formatedDate" },
    }
  },
  {
    $match: { Month: 12, Day:{$gte:25,$lte:31}}
  },
  {
    $project: {
      Pair:1,
      Base:1,
      Quote:1,
      Price:1,
      Date: 1,
      Year:{$toString:"$Year"},
      Month:1,
      Day:1

    }
  },
  {
    $sort: {Pair:1, Date:-1}
  },
  {
    $out:"fx_last_exrate"
  }
 ])



 db.forex.aggregate(
  [
    {
      $project:
        {
          _id:0,
          Pair:1,
          Date:1,
          formatedDate: {$toDate:"$Date"},
          Price:1
         
        }
    },
    {
      $project: {
        Pair:1,
        Base: { $substrCP: ['$Pair', 0, 3] },
        Quote: { $substrCP: ['$Pair', 3, { $strLenCP: '$Pair' }]},
        Date: 1,
        Price:1,
        Year: { $year: "$formatedDate" },
        Month: { $month: "$formatedDate" },
        Day: { $dayOfMonth: "$formatedDate" },
      }
    },
    {
      $match: { Month: 12}
    },
    {
      $project: {
        Pair:1,
        Base:1,
        Quote:1,
        Price:1,
        Date: 1,
        Year:{$toString:"$Year"},
        Month:1,
        Day:1
  
      }
    },
    {
      $sort: {Pair:1, Day:-1}
    },
    {
      $group: {
        _id:{"Pair":"$Pair", "Year":"$Year", "Month":"$Month","Day":"$Day"},
        last_ex: {$max:"$Day"}
      }
    },
    {
      $sort: {"_id.Pair":1, "_id.Year":-1}
    },
    
   ])