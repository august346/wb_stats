### TODO

#### gateway
- [ ] user me auth only
- [ ] wb_layer implement
  - [x] init
  - [ ] create report
  - ~~get report~~ (without background task)
- ~~validate api_key~~ (no add invalid)
  - ~~api keys inited flag~~ (no add invalid)
  - ~~endpoint for set inited~~ (no add invalid)


#### wb_layer
- [ ] post report
  - [x] aggregation
  - [ ] merge storage
  - [ ] return *.xlsx
- ~~get report~~ (without background task)
- ~~notify api key first collect inited~~ (return 400 for invalid api key)
- [ ] check exists row_ids while parse (without useless work)