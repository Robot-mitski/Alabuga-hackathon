class Communicator {
    url;
    constructor(url="http://127.0.0.1:5000/"){
        this.url = url;
    }

    async GetResponse(page, data) {
        let req = await fetch(this.url+page, data);
        console.log(this.url+page);
        if (req.ok){
            let resp = await req.json();
            return resp
        }
        return Error("Error in GetResponse was occured. Can't receive data from server")
    }
}

var com = new Communicator();
console.log(com.GetResponse("get", {}));