# NOLINE TELLER


## Get started

1. Clone the repo `git clone git@gitlab.com:michaelgao/noline.git`
2. Update remote `git remote update`
3. Switch to this branch `git checkout feature/teller-electron`
4. Install dependencies `npm install`
5. Also make sure that libconf2-4 dependency is installed `sudo apt install libgconf2-4`
6. Run in development mode `npm run dev`

## Environment Variables
1. `cd .electron-vue`
2. `touch env.js`

### Format
```
module.exports = {
	init: () => {
		// PROTOCOL://URL:PORT
		// NO TRAILING FORWARD SLASH
		process.env.API_URL = "http://url:port";
		process.env.WS_URL = "ws://url:port/ws";
	}
}
```
