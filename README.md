# Data that can be obtained by CL-EA-Stock-Data

currency 
exchange 
exchangeTimezoneName 
fiftyTwoWeekHigh 
fiftyTwoWeekHighChange 
fiftyTwoWeekHighChangePercent
fiftyTwoWeekLow 
fiftyTwoWeekLowChange
fiftyTwoWeekLowChangePercent
fiftyTwoWeekRange
ExchangeName 
market 
marketCap
marketState
quoteType
region
regularMarketChange 
regularMarketChangePercent 
regularMarketDayHigh
regularMarketDayLow
regularMarketDayRange 
MarketOpen
MarketPreviousClose
MarketPrice
MarketVolume
sharesOutstanding          

# How to obtain data

You only need to change to the desired stock symbol e.g. "TSLA" request.add("station_id", "TSLA");
The current jobId = "7ff89e0ae0344d29b69a12977feeacd2"; is set for a job the gets you the current market price
You can change both oracle and jobId if you prefer

See below an example ATestnetConsumer.sol

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

/**
 * Request testnet LINK and ETH here: https://faucets.chain.link/
 * Find information on LINK Tokåen Contracts and get the latest ETH and LINK faucets here: https://docs.chain.link/docs/link-token-contracts/
 */

/**
 * THIS IS AN EXAMPLE CONTRACT WHICH USES HARDCODED VALUES FOR CLARITY.
 * PLEASE DO NOT USE THIS CODE IN PRODUCTION.
 */
contract APIConsumer is ChainlinkClient {
    using Chainlink for Chainlink.Request;
  
    uint256 public price;
    
    address private oracle;
    bytes32 private jobId;
    uint256 private fee;
    
    /**
     * Network: Kovan
     * Oracle: 0xc57B33452b4F7BB189bB5AfaE9cc4aBa1f7a4FD8 (Chainlink Devrel   
     * Node)
     * Job ID: d5270d1c311941d0b08bead21fea7747
     * Fee: 0.1 LINK
     */
    constructor() {
        setPublicChainlinkToken();
        oracle = 0x4c12849d6bAFae264abF873A2Cc0f2CC850528A9;
        jobId = "7ff89e0ae0344d29b69a12977feeacd2";
        fee = 0.1 * 10 ** 18; // (Varies by network and job)
    }
    
    /**
     * Create a Chainlink request to retrieve API response, find the target
     * data, then multiply by 1000000000000000000 (to remove decimal places from data).
     */
    function requestPriceData() public returns (bytes32 requestId) 
    {
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        
        // Set the URL to perform the GET request on
 
        
        // Set the path to find the desired data in the API response, where the response format is:
        // {"RAW":
        //   {"ETH":
        //    {"USD":
        //     {
        //      "VOLUME24HOUR": xxx.xxx,
        //     }
        //    }
        //   }
        //  }
        request.add("station_id", "TSLA");
        
        // Multiply the result by 1000000000000000000 to remove decimals

        
        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }
    
    /**
     * Receive the response in the form of uint256
     */ 
    function fulfill(bytes32 _requestId, uint256 _price) public recordChainlinkFulfillment(_requestId)
    {
        price = _price;
    }

    // function withdrawLink() external {} - Implement a withdraw function to avoid locking your LINK in the contract
}

## Install

```
pipenv --python /usr/local/bin/python3
```

## Test

```
pipenv run pytest
```

## Run with Docker

Build the image

```
docker build . -t cl-ea-stock_data
```

Run the container

```
docker run -it -p 8080:8080 cl-ea-stock_data
```

## Run with Serverless

### Create the zip

```bash
pipenv lock -r > requirements.txt
pipenv run pip install -r requirements.txt -t ./package
pipenv run python -m zipfile -c cl-ea.zip main.py adapter.py bridge.py ./package/*
```

### Install to AWS Lambda

- In Lambda Functions, create function
- On the Create function page:
  - Give the function a name
  - Use Python 3.7 for the runtime
  - Choose an existing role or create a new one
  - Click Create Function
- Under Function code, select "Upload a .zip file" from the Code entry type drop-down
- Click Upload and select the `cl-ea.zip` file
- Change the Handler to `main.lambda_handler`
- Save

#### To Set Up an API Gateway

An API Gateway is necessary for the function to be called by external services.

- Click Add Trigger
- Select API Gateway in Trigger configuration
- Under API, click Create an API
- Choose REST API
- Select the security for the API
- Click Add
- Click the API Gateway trigger
- Click the name of the trigger (this is a link, a new window opens)
- Click Integration Request
- Uncheck Use Lamba Proxy integration
- Click OK on the two dialogs
- Return to your function
- Remove the API Gateway and Save
- Click Add Trigger and use the same API Gateway
- Select the deployment stage and security
- Click Add


### Install to Google Cloud Funcions

- In Functions, create a new function
- Use HTTP for the Trigger
- Optionally check the box to allow unauthenticated invocations
- Choose ZIP upload under Source Code
- Use Python 3.7 for the runtime
- Click Browse and select the `cl-ea.zip` file
- Select a Storage Bucket to keep the zip in
- Function to execute: `gcs_handler`
- Click Create
