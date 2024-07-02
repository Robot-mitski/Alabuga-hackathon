import { Communicator } from './Communicator.js';
import { ModelInputListener } from './ModelInputListener.js';

class GuestPage {
    CommunicatorInstance;
    ModelInputListenerInstance;

    static main(){
        this.CommunicatorInstance = new Communicator();
        this.ModelInputListenerInstance = new ModelInputListener(this.CommunicatorInstance);
        var model_form = document.getElementById("modelForm");
        model_form.addEventListener("submit", this.ModelInputListenerInstance.OnSubmit.bind(this.ModelInputListenerInstance));
        model_form.page = "guest"
    }
}

GuestPage.main();