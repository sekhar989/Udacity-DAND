## Wrangling OpenStreetMap Data of Kolkata, West Bengal, India
- by Krishnendu S. Kar

**Area of study**: 
  **City**: [Kolkata](https://www.openstreetmap.org/node/245707150)

**Objective**: Audit and clean the data set, converting it from XML to JSON format and load it to MongoDB.

**References**:
- Lesson 6 from Udacity course, “Data Wrangling with MongoDB”
- [Python 're' - documentation](https://docs.python.org/2.6/library/re.html)
- [Python 'strip' - documentation](https://docs.python.org/2/library/stdtypes.html?highlight=strip#str.strip)
- [MongoDB data import from JSON file](https://docs.mongodb.com/manual/reference/program/mongoimport/)

### Getting the data

The data was extracted from the [Overpass API](http://overpass-api.de/query_form.html), by passing the below query:
```sql
(
   node(22.4678, 88.3309, 22.6039, 88.4035);
   <;
);
out meta;
```

### Tags

`iterparse.py` was used to count occurrences of each tag, with a result:

```json
{'member': 4437,
 'meta': 1,
 'nd': 861202,
 'node': 692730,
 'note': 1,
 'osm': 1,
 'relation': 763,
 'tag': 159164,
 'way': 148337}
```
Further modifications were made to `iterparse.py` to examine the keys stored in each `tag` element, in the `k` attribute. Few of the most :

```tuple
('building', 130748), ('highway', 13468), ('name', 3960), ('landuse', 1542), ('service', 1200), ('type', 762), ('railway', 708), ('natural', 561), ('amenity', 511), ('oneway', 342), ('leisure', 331), ('voltage', 267), ('electrified', 264), ('frequency', 262), ('gauge', 260), ('bridge', 241), ('layer', 212), ('addr:street', 204), ('addr:housenumber', 190), ('ref', 147), ('addr:postcode', 139), ('passenger_lines', 129), ('source', 128), ('name:en', 123), ('lanes', 112), ('addr:city', 106), ('public_transport', 106)
```
Further parsing was done through the 'tag'-data and a sample of 15 data points were taken for each tag(key, value).

Inconcistencies were noticed in:

### 1. Postcodes/Zip-Codes
Postcodes/Zip-codes were present under *`addr:postcode`* tag. Kolkata postcodes are of 6-digits and ranges from *`700001`* to *`700120`*.
While checking the data, several inconsistencies were noticed in the postcodes present in the raw dataset. e.g.: ***`7017`*** (less than 6-digits), ***`'700 073'`***, ***`'7000 026'`***.

### 2. Phone Numbers
Phone numbers were present under ***`phone`***. Issues viz. ***`+91906285598`***, ***`033 2227 2625`***.
***`+91`*** & gaps along with dash(-) should be removed from phone numbers


### 3. Street Names
There were inconsistencies with street name abbreviations.Issues in Streets viz. ***`Rameswar Shaw Rd`*** , ***`Karbala Tank Ln`***. Acronyms like ***`Rd`*** & ***`Ln`*** are used, which are actually ***`Road`*** & ***`Lane`***.

In depth studies related to isseues were made using the *`audit_db.py`* program.

### Special Tags
There were quite a number of `tag k-v pairs`, which are present only once. 
They are some special tags, which came into the picture just for a specific scenario.
e.g.: ***`toilets:disposal`***, ***`name:ml`***, ***`name:hr`*** etc.

As part of the cleaning process, a manual selection of `tag k-v pairs` was made based on the amount of occurence.
Tags which have occured less than equal to 4-times, were ignored.

### MongoDB
The json output file was loaded to a mongoDB database using the terminal command shown below.

```terminal
$: mongoimport --db cities --collection kolkata --type json --file ~/'Udacity DAND'/Calcutta.osm.json

2017-08-25T03:06:18.648+0530	connected to: localhost
2017-08-25T03:06:21.646+0530	[........................] cities.kolkata	6.34MB/173MB (3.7%)
2017-08-25T03:06:24.646+0530	[#.......................] cities.kolkata	13.9MB/173MB (8.0%)
2017-08-25T03:06:27.646+0530	[##......................] cities.kolkata	21.5MB/173MB (12.4%)
2017-08-25T03:06:30.646+0530	[####....................] cities.kolkata	29.2MB/173MB (16.9%)
2017-08-25T03:06:33.646+0530	[#####...................] cities.kolkata	36.3MB/173MB (21.0%)
2017-08-25T03:06:36.646+0530	[######..................] cities.kolkata	43.8MB/173MB (25.3%)
2017-08-25T03:06:39.646+0530	[#######.................] cities.kolkata	51.5MB/173MB (29.7%)
2017-08-25T03:06:42.646+0530	[########................] cities.kolkata	59.3MB/173MB (34.3%)
2017-08-25T03:06:45.646+0530	[#########...............] cities.kolkata	67.1MB/173MB (38.7%)
2017-08-25T03:06:48.646+0530	[##########..............] cities.kolkata	74.6MB/173MB (43.1%)
2017-08-25T03:06:51.646+0530	[###########.............] cities.kolkata	82.3MB/173MB (47.5%)
2017-08-25T03:06:54.646+0530	[############............] cities.kolkata	90.3MB/173MB (52.1%)
2017-08-25T03:06:57.646+0530	[#############...........] cities.kolkata	97.5MB/173MB (56.3%)
2017-08-25T03:07:00.646+0530	[##############..........] cities.kolkata	105MB/173MB (60.6%)
2017-08-25T03:07:03.646+0530	[###############.........] cities.kolkata	113MB/173MB (65.2%)
2017-08-25T03:07:06.646+0530	[################........] cities.kolkata	120MB/173MB (69.5%)
2017-08-25T03:07:09.646+0530	[#################.......] cities.kolkata	128MB/173MB (74.1%)
2017-08-25T03:07:12.646+0530	[##################......] cities.kolkata	137MB/173MB (78.9%)
2017-08-25T03:07:15.646+0530	[####################....] cities.kolkata	146MB/173MB (84.0%)
2017-08-25T03:07:18.646+0530	[#####################...] cities.kolkata	154MB/173MB (89.1%)
2017-08-25T03:07:21.646+0530	[######################..] cities.kolkata	161MB/173MB (92.7%)
2017-08-25T03:07:24.646+0530	[#######################.] cities.kolkata	169MB/173MB (97.7%)
2017-08-25T03:07:26.057+0530	[########################] cities.kolkata	173MB/173MB (100.0%)

2017-08-25T03:07:26.057+0530	imported 841067 documents
```

File sizes:
- `Calcutta.osm: 156.9 MB`
- `Calcutta.osm.json: 181.6 MB`

Checking total number of documents:

```python
> db.kolkata.find().count()
```
Output: 1682134

Total `"node"` count:
```python
> db.kolkata.find({"type":"node"}).count()
```
Output: 1385460

Total `"way"` count:
```python
> db.kolkata.find({"type":"way"}).count()
```
Output: 148337

Total number of unique users:
```python
> x = db.kolkata.distinct("created.user")
> print len(x)
```
Output: 314

Total entries having an address:
```python
> db.kolkata.find({"address" : {"$exists" : 1}}).count()
```
Output: 478

Some more queries were made, using the `mongodb_queries.py` program. The ouput are shown below:

Top 5 users with higherst contribution...
```json
{'$group': {'_id': '$created.user','count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 5}

```

Output:

```json
 {u'_id': u'Rondon237', u'count': 147882},
 {u'_id': u'pvprasad', u'count': 138692},
 {u'_id': u'hareesh11', u'count': 128650},
 {u'_id': u'rajureddyvudem', u'count': 127720},
 {u'_id': u'udaykanth', u'count': 109344}
 ```
 
 Number of users, who contributed the least... 
```json
{'$group': {'_id': '$created.user','count': {'$sum': 1}}}, {'$group': {'_id': '$count','num_users': {'$sum': 1}}}, {'$sort': {'_id': 1}}, {'$limit': 1}
```


Output:
```json
{u'_id': 2, u'num_users': 76}
```

### Conclusion

The queries were conducted mostly on the users. It is also noticed that there are very few nodes with actual address. The raw-data is extracted here only from one source, hence further raw-data collection from different sources are recommended.

I believe, there are still few opportunities for cleaning and validation of data, which is left unexplored. Keeping that in mind, I would like to state that the data set was well-cleaned for the purposes of this exercise.

#### Files
- `subset.py`: Creates data subset
- `iterparse.py`: Parsing through the dataset and getting an initial idea of the raw dataset
- `audit_db.py`: Auditing the identified issues
- `final_db_data.py`: Parsing, Editing & Cleaning the identified/considered flaws and dumping a <file>.json file.
- `mongodb_queries.py`: Creating basic queries over the database after moving the json data to mongodb database.
