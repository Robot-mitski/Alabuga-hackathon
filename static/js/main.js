import { Communicator } from './Communicator.js';
import { RegFormListener } from './RegFormListener.js';
import { LogFormListener } from './LogFormListener.js';

class Main {
    CommunicatorInstance;
    RegFormListenerInstance;
    LogFormListenerInstance;

    static main(){
        this.CommunicatorInstance = new Communicator();
        this.RegFormListenerInstance = new RegFormListener(this.CommunicatorInstance);
        this.LogFormListenerInstance = new LogFormListener(this.CommunicatorInstance);
        var reg_form = document.getElementById("regForm");
        var log_form = document.getElementById("logForm");
        reg_form.addEventListener("submit", this.RegFormListenerInstance.OnSubmit.bind(this.RegFormListenerInstance));
        log_form.addEventListener("submit", this.LogFormListenerInstance.OnSubmit.bind(this.LogFormListenerInstance));
        // console.log(this.CommunicatorInstance.SendResponse("post", {name: "Nate Higgers",
        //         sex: "never"}));
    }
}

Main.main();