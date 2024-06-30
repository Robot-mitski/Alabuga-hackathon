export class LogFormListener {
    #CommunicatorInstance;
    constructor(CommunicatorInstance){
        this.#CommunicatorInstance = CommunicatorInstance;
    }

    async OnSubmit(event){
        event.preventDefault();
        var form = document.getElementById("logForm");
		var error = document.getElementById("logError");
		var email = form.logEmailField.value;
		var pass = form.logPassField.value;
        const EMAIL_RE = /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/iu;
        if (email === "" || pass === ""){
            error.innerHTML = "Заполните все поля";
            return false; }
        if (!EMAIL_RE.test(email)){
            error.innerHTML = "Неверный формат почтового адреса";
            return false; }
        var resp = await this.#CommunicatorInstance.SendResponse("login", {
            "email": email,
            "pass": pass
        }).then((json)=> {return json});
        console.log("smth");
        var resp = JSON.parse(JSON.stringify(resp));
        if (resp.status !== "ok") {
            error.innerHTML = resp.message;
            return false;
        }
        window.location.href = "http://127.0.0.1:5000/user"
        return true;
    }
}