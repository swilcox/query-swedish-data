# query-swedish-data
Very quick and dirty script to query Statistics Sweden names data.

## Background

I needed to grab Swedish name data to submit to as an enhancement to the Python [Faker Package](https://github.com/joke2k/faker). The [Statistics Sweden](https://www.scb.se/en/) web site offers fairly easy to download "top 100" names info for last names, and first names (by gender). However, I wanted to use data more like what was already in Faker. So I felt the top 200 was closer to what was already there. In order to do that, involved calling their [API](https://www.scb.se/en/About-us/open-data-api/api-for-the-statistical-database/).

## Notes

* This code is not particularly long term stable
* Not suitable for anything other than a reference to myself about how I did something.
* There may be a far more efficient way of querying the database for what was needed but it was not particularly obvious from their API documentation.
* I was in a hurry so it's probably not the greatest example of code.
* Output is currently formatted for easily copy/paste into the desired Faker library code.

## Running

* Use a virtualenv of some kind!
* Use Python 3.x (tested only with 3.6.x and 3.7.x)
* `pip install -r requirements.txt`

```
$ python get_names.py female female.txt
```

The above command will query the female first names and output the top 200 in the female.txt... sorted by name in code format with the percentage of total occurances among the top 200.

Other options would be:

Male first names:

```
$ python get_names.py male male.txt
```

Last names:

```
$ python get_names.py last last.txt
```

And yes, that last names query will take awhile.
