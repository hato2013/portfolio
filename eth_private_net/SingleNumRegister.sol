contract SingleNumRegister {
    uint storedData;
    constructor set(uint x) public{
        storedData = x;
    }
    constructor get() public constant returns (uint retVal){
        return storedData;
    }
}