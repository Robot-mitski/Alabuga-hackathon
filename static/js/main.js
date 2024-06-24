import {Communicator} from './Communicator.js';

class Main {
    CommunicatorInstance;

    static main(){
        this.CommunicatorInstance = new Communicator();
        console.log(this.CommunicatorInstance.SendResponse("post", {name: "Nate Higgers",
                sex: "never"}));
    }
}

Main.main();