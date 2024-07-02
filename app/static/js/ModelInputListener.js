export class ModelInputListener {
    #CommunicatorInstance;
    constructor(CommunicatorInstance){
        this.#CommunicatorInstance = CommunicatorInstance;
    }

    async OnSubmit(event){
        event.preventDefault();
        var form = document.getElementById("modelForm");
		var error = document.getElementById("modelError");
        var input = form.modelInput.value;
        var output = document.getElementById("modelOutput");
        if (input === ""){
            error.innerHTML = "Заполните все поля";
            return false; }
        var resp = await this.#CommunicatorInstance.SendResponse(event.currentTarget.page, {
            "url": input
        }).then((json)=> {return json});
        var resp = JSON.parse(JSON.stringify(resp));
        if (resp.status !== "ok") {
            error.innerHTML = resp.message;
            return false;
        }
        output.innerHTML = resp.output;
        return true;
    }
}