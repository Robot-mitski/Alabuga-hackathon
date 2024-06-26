import { Communicator } from './Communicator.js';
import { LogFormListener } from './LogFormListener.js';

class Login {
    CommunicatorInstance;
    LogFormListenerInstance;

    static main(){
        this.CommunicatorInstance = new Communicator();
        this.LogFormListenerInstance = new LogFormListener(this.CommunicatorInstance);
        var log_form = document.getElementById("logForm");
        log_form.addEventListener("submit", this.LogFormListenerInstance.OnSubmit.bind(this.LogFormListenerInstance));
    }
}

Login.main();