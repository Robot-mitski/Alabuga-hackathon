import { Communicator } from './Communicator.js';
import { RegFormListener } from './RegFormListener.js';

class Main {
    CommunicatorInstance;
    RegFormListenerInstance;

    static main(){
        this.CommunicatorInstance = new Communicator();
        this.RegFormListenerInstance = new RegFormListener(this.CommunicatorInstance);
        var reg_form = document.getElementById("regForm");
        reg_form.addEventListener("submit", this.RegFormListenerInstance.OnSubmit.bind(this.RegFormListenerInstance));
    }
}

Main.main();