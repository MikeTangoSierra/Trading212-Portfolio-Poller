# Trading212-Portfolio-Poller

A Python based application to reach out to the Trading212 API and grab a some statistics about your personal portfolio then expose them on a API endpoint using flask.
The data is also written to a MongoDB database, so that we don't have to keep hitting the Trading212 API as it's rate limited. This also allows us to keep a history of our portfolio statistics and do any analysis we want on the data.

## Statistics We Return 

We currently retrieve the following statistics and expose them on a flask endpoint:
- Overall Portfolio Value
- Currently Open Positions (JSON Array Of Objects)
- Currently Open Biggest Winning Position
- Currently Open Biggest Losing Position
- Overall Profit/Loss
- Biggest Winning Position (Daily, Weekly, Monthly, Quarterly, Yearly)
- Biggest Losing Position (Daily, Weekly, Monthly, Quarterly, Yearly)

## What We Write To MongoDB
- Overall Portfolio Value
- Overall Profit/Loss
- Currently Open Positions (JSON Array Of Objects)

## Usage

- COMING SOON

## Local Devlopment
The bringing up and down of the local has been abstracted to a Makefile.

`make up` will bring the whole environment up without needing to switch folders.

`make down` will kill and remove the containers.


## Contributing

- COMING SOON

## License

[MIT](https://choosealicense.com/licenses/mit/)
