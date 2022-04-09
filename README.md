
# Backend for Consumer Complaint Database

## Instructions for running project as a whole:

1. Download the [elasticsearch binaries](https://www.elastic.co/downloads/elasticsearch) and place them somewhere easy to get with a terminal.
2. Open a terminal (Powershell, ZSH, BASH, etc) and 'cd' your way to the 'bin' folder of the elasticsearch binaries
3. run elasticsearch (./elasticsearch in the terminal) and let it run for a minute until we can connect
4. go into this project folder, run python main.py (this will start the backend up)
5. download the [frontend project repository](https://github.com/LukeTarr/INFSCI-1560-Client)
6. go into the folder where you downloaded the frontend, type 'npm install' and let that finish running
7. type 'npm start' to launch a web browser running the front-end and use it to query with a term or filter

## Instructions for editing the Result cards

1. Result.js and Result.css are the files relating to the result cards
2. At the end of Search.js we have a map function running for every result and rendering a result card with data
3. If you want to change the data that gets passed into the card, use h._source.whatever attribute you want from the original json
4. To make it actually appear in the card, you need Result.js to render some html (probably a p tag) with {props.attribute} that you're passing from the h._source
5. if you have trouble use [this](https://www.robinwieruch.de/react-pass-props-to-component/) or just search how to use props in React