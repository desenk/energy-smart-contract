// This Smart Contract opens a negotiation place (Market Place): First, it will collect the bids from buyers and sellers. It will store the bids.
// Then, it will proceed to the paymen of the selected bids, where the selection is done outside the Smart Contract, by an external agent (DSO)

pragma solidity >=0.4.21 <0.7.0;

contract NegotiationMarketPlace {
    // The Market place stores the count of all the buyers, sellers who sent bids
    uint8 private buyerCount;
    uint8 private sellerCount;
    uint private operationalDeposit; // an amount of money used to pay all operation fees
    // The market place stores (with a hash) the bid (price and quantity, we also need the weights (or Beta) and other informations to be added), and the type of the agent (Buyer (1) or Seller (0))
    mapping (address => uint) private bidPrice;
    mapping (address => uint) private bidQuantity;
    mapping (address => uint) private bidWeight;
    mapping (address => uint) public agentType;
    mapping (address => uint) private depositAmount;

    //If we use state machine to coordinate all steps
    enum State { BID_DEPOSIT_OPEN, BID_DEPOSIT_OVER, AWAITING_DELIVERY, COMPLETE, FINISHED}
    State public currState;

    // The market place is owned by the DSO Agent:
    address payable public dsoAgent;
    // We also need to add a time: Times are either absolute unix timestamps (seconds since 1970-01-01) or time periods in seconds.
    uint public marketEndTime; // not used yet

    // Log the event about a bid being made by an address (Agent) and its amount
    event LogBidMade(address indexed accountAddress, uint price, uint quantity, uint Weight); // Notice that weights
    // are uint for now, as fixed point are not yet fully implemented (=> the DSO will divide by 10)
    
       // We need  a boolean to state the stage of the market place (open or not for receiving new offers/bids) Set to true at the end, disallows any change. By default initialized to `false`.
    bool ended;

    //  We create a modifier that could be used later to restrict some functions to only the operator. not needed for simple use
    modifier onlyOperator() {
        require(
            msg.sender == dsoAgent,
            "Only DSO/Operator can call this."
        );
        _;
    }

    // Constructor function to initialize the MarketPlace. It is "payable" so it can receive initial funding to cover up some mispayment
    constructor() public payable {
       // require(msg.value == 10 ether, "10 ether initial funding required");
        /* Set the owner to the creator of this contract */
        dsoAgent = msg.sender;
        // initialization of variables
        buyerCount = 0;
        sellerCount = 0;
    }


    // used to refill the amount of the operational deposit
    function operationaldeposit() public payable onlyOperator returns (uint) {
        operationalDeposit = operationalDeposit+msg.value;
         return 1;
    }

    ///  Creation of a bid from an agent return The type of the agent (1 or 0)
    function submitBid(uint _bidprice, uint _bidquantity, uint _bidweight, uint _agenttype) public payable  returns (uint) {
         // if we use state machine, require(currState == State.BID_DEPOSIT_OPEN, "Cannot confirm Bid deposit");
       if (_agenttype == 1) {
            buyerCount++;}
        else  {
            sellerCount++;
        }
        // We update all values of this agent
        bidPrice[msg.sender] = _bidprice;
        bidQuantity[msg.sender] = _bidquantity;
        bidWeight[msg.sender] = _bidweight;
        agentType[msg.sender] = _agenttype;
        depositAmount[msg.sender] = msg.value;
         // if (timesup ***** or agent count reached) currState = State.BID_DEPOSIT_OVER;

         return agentType[msg.sender];
    }

  function getbalance(address agentaddress) public view returns(uint) {
        uint out;
        out = depositAmount[agentaddress];
        return out;
    }
  function getrealbalance(address agentaddress) public view returns(uint) {
        uint out;
            if (agentaddress!=dsoAgent){
                out = agentaddress.balance;
            }
            else
            {
                out = dsoAgent.balance;
            }
        return out;
    }

// The operator or DSO wants to retrieve all the bids. However, mapping does not allow to do that. Hence, we can either store each bid/agent into an iterable mapping
// as shown here https://medium.com/rayonprotocol/creating-a-smart-contract-having-iterable-mapping-9b117a461115 or also the github (https://github.com/ethereum/dapp-bin/blob/master/library/iterable_mapping.sol)
// or the operator/DSO makes as many requests to this Smart Contract to retrieve all the bids from all the registered agents. And if an agent has not placed a bid, it returns 0
    function retrievebid(address agentaddress) public view returns(uint[5] memory) {  // we store the
    // return into memory, not storage, as we do not ned it outside of the function
        require(msg.sender == dsoAgent,"Only DSO/Operator can call this.");
        // if we use state machine, require(currState == State.BID_DEPOSIT_OVER, "Cannot confirm Bid deposit");
        uint[5] memory array;
        if (bidPrice[agentaddress] != 0){
            array = [bidPrice[agentaddress], bidQuantity[agentaddress],bidWeight[agentaddress],agentType[agentaddress],depositAmount[agentaddress]];
        }
            return array;
         //currState = State.AWAITING_DELIVERY;

    }

// After negotiations, the DSO/operator wants to activate payment between agents, while specifying the amount
  function settlement(address buyeraddress, address payable selleraddress, uint pricetopay) external onlyOperator {
        // if we use state machine, require(currState == State.AWAITING_DELIVERY, "Cannot confirm delivery");
        if (depositAmount[buyeraddress]>pricetopay){
            // selleraddress.transfer(pricetopay); // we transfer the money to the seller
            depositAmount[selleraddress] = depositAmount[selleraddress]+pricetopay; // we update the amounts in this SC
            depositAmount[buyeraddress] = depositAmount[buyeraddress] - pricetopay;// we update the amounts in this SC
        }
        //currState = State.COMPLETE;
    }

// Once everything is finished, the DSO/operator close the negotiation by redistributing the money that is in the accounts
  function close(address payable agentaddress) external payable onlyOperator {
        // if we use state machine, require(currState == State.COMPLETE, "Cannot confirm delivery");
            // selleraddress.transfer(depositAmount[selleraddress]); // we transfer the money to the seller
            if (agentaddress!=dsoAgent){
            agentaddress.transfer(depositAmount[agentaddress]); // we transfer the money to the seller
            }
            else
            {
                dsoAgent.transfer(operationalDeposit);
            }
        //currState = State.FINISHED;
    }

    // Once everything is finished, the DSO/operator close the negotiation by redistributing the money that is in the accounts
  function closecontract() external payable onlyOperator {
        // if we use state machine, require(currState == State.COMPLETE, "Cannot confirm delivery");
            // selleraddress.transfer(depositAmount[selleraddress]); // we transfer the money to the seller
            uint fee;
            fee = 1000000000000000000;  // we define is a fee of operational cost that should be removed...
                msg.sender.transfer(operationalDeposit-fee);
        //currState = State.FINISHED;
    }


}



/*     // The following comment is a so-called natspec comment, recognizable by the three slashes. It will be shown when the user is asked to confirm a transaction.
    /// Create a simple MarketPlace with `_marketEndTime` seconds bidding time 
    constructor(
        uint _marketEndTime,
   //     address payable _beneficiary
    ) public {
     //   beneficiary = _beneficiary;
        marketEndTime = now + _marketEndTime;
    } */
