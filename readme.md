### TODO

#### gateway
- [x] user me auth only
- [x] wb_layer implement
  - [x] init
  - [x] create report
  - [ ] get brands
  - ~~get report~~ (without background task)
- ~~validate api_key~~ (no add invalid)
  - ~~api keys inited flag~~ (no add invalid)
  - ~~endpoint for set inited~~ (no add invalid)


#### wb_layer
- [x] post report
  - [x] aggregation
  - [x] merge storage
  - [x] return ~~*.xlsx ... *.csv~~ json
  - [ ] return brands
- [ ] refactor post report
- ~~get report~~ (without background task)
- ~~notify api key first collect inited~~ (return 400 for invalid api key)
- [ ] ??? check exists row_ids while parse (without useless work)


#### front-end
- [ ] pages text
  - [ ] translate
  - [ ] home
  - [ ] contacts
  - [ ] fbs
- [x] auth
  - [x] login
  - [x] signup
- [x] api-keys
  - [x] c
  - [x] r
  - [x] u
  - [x] d
  - [x] list
- [ ] generate report
  - [x] dates
  - [x] brands
- [ ] bugs
  - [ ] header active link
  - [ ] sales report out of range | no rows
  - [ ] shop duplicates
