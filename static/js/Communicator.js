export class Communicator {
    url;
    constructor(url="http://127.0.0.1:5000/"){
        this.url = url;
    }

    async GetResponse(page) {
        let req = await fetch(this.url+page, data);
        if (req.ok){
            let resp = await req.json();
            return resp;
        }
        console.log(Error("Error in GetResponse was occured. Can't receive data from server"));
        return null;
    }

    async SendResponse(page, data) {
        let req = await fetch(this.url+page, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(data),
        });
        if (req.ok){
            let resp = await req.json();
            return resp;
        }
        console.log(Error("Error in SendResponse was occured. Can't receive data from server"));
        return null;
    }
}